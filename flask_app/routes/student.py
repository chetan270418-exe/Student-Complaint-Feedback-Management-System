"""
Student Routes
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from models.models import Complaint, TimelineEvent, Feedback, Notification

student_bp = Blueprint('student', __name__)


def student_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'student':
            flash('Access denied.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    complaints = Complaint.query.filter_by(student_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    stats = {
        'total':      len(complaints),
        'submitted':  sum(1 for c in complaints if c.status == 'submitted'),
        'inprogress': sum(1 for c in complaints if c.status in ('assigned', 'inprogress')),
        'resolved':   sum(1 for c in complaints if c.status in ('resolved', 'closed')),
    }
    recent     = complaints[:5]
    notif_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('student/dashboard.html',
                           complaints=complaints, stats=stats,
                           recent=recent, notif_count=notif_count)


@student_bp.route('/submit', methods=['GET', 'POST'])
@login_required
@student_required
def submit():
    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category    = request.form.get('category')
        priority    = request.form.get('priority')

        if not all([title, description, category, priority]):
            flash('All fields are required.', 'danger')
            return render_template('student/submit.html')

        c = Complaint(student_id=current_user.id, title=title,
                      description=description, category=category,
                      priority=priority, status='submitted')
        db.session.add(c)
        db.session.flush()

        ev = TimelineEvent(complaint_id=c.id, status='submitted',
                           note='Complaint submitted by student.',
                           created_at=datetime.utcnow())
        db.session.add(ev)

        # Notify admin
        admin_notif = Notification(
            user_id=1,  # admin id=1
            title='New Complaint Received',
            message=f'New complaint "{title}" submitted by {current_user.name}.'
        )
        db.session.add(admin_notif)
        db.session.commit()

        flash(f'Complaint submitted successfully! ID: #{c.id}', 'success')
        return redirect(url_for('student.my_complaints'))

    notif_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('student/submit.html', notif_count=notif_count)


@student_bp.route('/complaints')
@login_required
@student_required
def my_complaints():
    status_f   = request.args.get('status', '')
    category_f = request.args.get('category', '')
    search     = request.args.get('search', '')

    q = Complaint.query.filter_by(student_id=current_user.id)
    if status_f:   q = q.filter_by(status=status_f)
    if category_f: q = q.filter_by(category=category_f)
    if search:     q = q.filter(Complaint.title.ilike(f'%{search}%'))

    complaints  = q.order_by(Complaint.created_at.desc()).all()
    notif_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('student/complaints.html',
                           complaints=complaints, notif_count=notif_count,
                           status_f=status_f, category_f=category_f, search=search)


@student_bp.route('/complaint/<int:cid>')
@login_required
@student_required
def complaint_detail(cid):
    c = Complaint.query.get_or_404(cid)
    if c.student_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('student.my_complaints'))
    timeline    = c.timeline.order_by(TimelineEvent.created_at).all()
    notif_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('student/detail.html', complaint=c,
                           timeline=timeline, notif_count=notif_count)


@student_bp.route('/feedback/<int:cid>', methods=['POST'])
@login_required
@student_required
def submit_feedback(cid):
    c = Complaint.query.get_or_404(cid)
    if c.student_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('student.my_complaints'))
    if c.feedback:
        flash('Feedback already submitted.', 'warning')
        return redirect(url_for('student.complaint_detail', cid=cid))

    rating  = int(request.form.get('rating', 0))
    comment = request.form.get('comment', '').strip()
    if not 1 <= rating <= 5:
        flash('Please select a valid rating (1–5).', 'danger')
        return redirect(url_for('student.complaint_detail', cid=cid))

    fb = Feedback(complaint_id=cid, student_id=current_user.id,
                  rating=rating, comment=comment)
    db.session.add(fb)
    db.session.commit()
    flash('Thank you for your feedback!', 'success')
    return redirect(url_for('student.complaint_detail', cid=cid))


@student_bp.route('/notifications')
@login_required
@student_required
def notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id)\
                               .order_by(Notification.created_at.desc()).all()
    # Mark all read
    Notification.query.filter_by(user_id=current_user.id, is_read=False)\
                      .update({'is_read': True})
    db.session.commit()
    return render_template('student/notifications.html',
                           notifications=notifs, notif_count=0)
