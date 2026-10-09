"""
Admin Routes
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from models.models import User, Complaint, TimelineEvent, Notification, Feedback

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    complaints  = Complaint.query.order_by(Complaint.created_at.desc()).all()
    unassigned  = [c for c in complaints if not c.assigned_to and c.status == 'submitted']
    high_priority = [c for c in complaints if c.priority == 'high' and c.status not in ('resolved','closed')]
    stats = {
        'total':      len(complaints),
        'unassigned': len(unassigned),
        'inprogress': sum(1 for c in complaints if c.status in ('assigned','inprogress')),
        'resolved':   sum(1 for c in complaints if c.status in ('resolved','closed')),
        'students':   User.query.filter_by(role='student').count(),
    }
    cat_stats = {}
    for cat in ('hostel','mess','lab','faculty','library','other'):
        cat_stats[cat] = sum(1 for c in complaints if c.category == cat)

    notif_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('admin/dashboard.html',
                           stats=stats, unassigned=unassigned,
                           high_priority=high_priority,
                           cat_stats=cat_stats, notif_count=notif_count)


@admin_bp.route('/complaints')
@login_required
@admin_required
def complaints():
    status_f   = request.args.get('status', '')
    priority_f = request.args.get('priority', '')
    category_f = request.args.get('category', '')
    search     = request.args.get('search', '')

    q = Complaint.query
    if status_f:   q = q.filter_by(status=status_f)
    if priority_f: q = q.filter_by(priority=priority_f)
    if category_f: q = q.filter_by(category=category_f)
    if search:     q = q.filter(Complaint.title.ilike(f'%{search}%'))

    complaints  = q.order_by(Complaint.created_at.desc()).all()
    notif_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('admin/complaints.html',
                           complaints=complaints, notif_count=notif_count,
                           status_f=status_f, priority_f=priority_f,
                           category_f=category_f, search=search)


@admin_bp.route('/complaint/<int:cid>')
@login_required
@admin_required
def complaint_detail(cid):
    c           = Complaint.query.get_or_404(cid)
    timeline    = c.timeline.order_by(TimelineEvent.created_at).all()
    staff_list  = User.query.filter_by(role='staff').all()
    notif_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('admin/detail.html', complaint=c,
                           timeline=timeline, staff_list=staff_list,
                           notif_count=notif_count)


@admin_bp.route('/assign/<int:cid>', methods=['POST'])
@login_required
@admin_required
def assign(cid):
    c        = Complaint.query.get_or_404(cid)
    staff_id = request.form.get('staff_id', type=int)
    note     = request.form.get('note', '').strip() or 'Assigned by Admin.'

    staff = User.query.get(staff_id)
    if not staff or staff.role != 'staff':
        flash('Invalid staff member selected.', 'danger')
        return redirect(url_for('admin.complaint_detail', cid=cid))

    c.assigned_to = staff_id
    c.status      = 'assigned'
    c.updated_at  = datetime.utcnow()

    ev = TimelineEvent(complaint_id=cid, status='assigned',
                       note=f'{note} → {staff.name}', created_at=datetime.utcnow())
    db.session.add(ev)

    # Notify student
    db.session.add(Notification(
        user_id=c.student_id,
        title='Complaint Assigned',
        message=f'Your complaint "{c.title}" has been assigned to {staff.name}.'
    ))
    # Notify staff
    db.session.add(Notification(
        user_id=staff_id,
        title='New Complaint Assigned to You',
        message=f'Complaint "{c.title}" has been assigned to you. Please take action.'
    ))
    db.session.commit()
    flash(f'Complaint assigned to {staff.name} successfully.', 'success')
    return redirect(url_for('admin.complaint_detail', cid=cid))


@admin_bp.route('/update/<int:cid>', methods=['POST'])
@login_required
@admin_required
def update_status(cid):
    c          = Complaint.query.get_or_404(cid)
    new_status = request.form.get('status')
    note       = request.form.get('note', '').strip() or f'Status changed to {new_status} by Admin.'

    c.status     = new_status
    c.updated_at = datetime.utcnow()
    ev = TimelineEvent(complaint_id=cid, status=new_status,
                       note=note, created_at=datetime.utcnow())
    db.session.add(ev)

    db.session.add(Notification(
        user_id=c.student_id,
        title='Complaint Status Updated',
        message=f'Your complaint "{c.title}" status is now: {new_status.upper()}.'
    ))
    db.session.commit()
    flash(f'Status updated to "{new_status}".', 'success')
    return redirect(url_for('admin.complaint_detail', cid=cid))


@admin_bp.route('/delete/<int:cid>', methods=['POST'])
@login_required
@admin_required
def delete_complaint(cid):
    c = Complaint.query.get_or_404(cid)
    db.session.delete(c)
    db.session.commit()
    flash('Complaint deleted successfully.', 'info')
    return redirect(url_for('admin.complaints'))


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_users   = User.query.order_by(User.role, User.name).all()
    notif_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    stats = {
        'students': sum(1 for u in all_users if u.role == 'student'),
        'staff':    sum(1 for u in all_users if u.role == 'staff'),
        'admins':   sum(1 for u in all_users if u.role == 'admin'),
    }
    return render_template('admin/users.html', users=all_users,
                           stats=stats, notif_count=notif_count)


@admin_bp.route('/users/delete/<int:uid>', methods=['POST'])
@login_required
@admin_required
def delete_user(uid):
    u = User.query.get_or_404(uid)
    if u.role == 'admin':
        flash('Cannot delete admin accounts.', 'danger')
    else:
        db.session.delete(u)
        db.session.commit()
        flash(f'User {u.name} deleted.', 'info')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/add', methods=['POST'])
@login_required
@admin_required
def add_user():
    name     = request.form.get('name', '').strip()
    email    = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    role     = request.form.get('role', 'student')
    roll_no  = request.form.get('roll_no', '').strip()
    branch   = request.form.get('branch', '')
    semester = request.form.get('semester', 1)
    dept     = request.form.get('department', '')
    desig    = request.form.get('designation', '')

    if User.query.filter_by(email=email).first():
        flash('Email already exists.', 'danger')
        return redirect(url_for('admin.users'))

    u = User(name=name, email=email, role=role, roll_no=roll_no,
             branch=branch, semester=int(semester) if semester else None,
             department=dept, designation=desig)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    flash(f'User {name} added successfully.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    complaints  = Complaint.query.all()
    feedbacks   = Feedback.query.all()
    total       = len(complaints)
    resolved    = sum(1 for c in complaints if c.status in ('resolved','closed'))
    res_rate    = round(resolved / total * 100, 1) if total else 0
    avg_rating  = round(sum(f.rating for f in feedbacks) / len(feedbacks), 1) if feedbacks else 0

    cat_stats   = {}
    for cat in ('hostel','mess','lab','faculty','library','other'):
        cat_stats[cat] = sum(1 for c in complaints if c.category == cat)

    status_stats = {}
    for st in ('submitted','assigned','inprogress','resolved','closed'):
        status_stats[st] = sum(1 for c in complaints if c.status == st)

    priority_stats = {p: sum(1 for c in complaints if c.priority == p) for p in ('high','medium','low')}

    notif_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('admin/reports.html',
                           total=total, resolved=resolved, res_rate=res_rate,
                           avg_rating=avg_rating, cat_stats=cat_stats,
                           status_stats=status_stats, priority_stats=priority_stats,
                           notif_count=notif_count)
