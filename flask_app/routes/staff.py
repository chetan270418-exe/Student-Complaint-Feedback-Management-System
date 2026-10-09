"""
Staff Routes
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from models.models import Complaint, TimelineEvent, Notification

staff_bp = Blueprint('staff', __name__)


def staff_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'staff':
            flash('Access denied.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@staff_bp.route('/dashboard')
@login_required
@staff_required
def dashboard():
    assigned = Complaint.query.filter_by(assigned_to=current_user.id)\
                              .order_by(Complaint.updated_at.desc()).all()
    pending  = [c for c in assigned if c.status not in ('resolved', 'closed')]
    stats = {
        'total':      len(assigned),
        'pending':    len(pending),
        'inprogress': sum(1 for c in assigned if c.status == 'inprogress'),
        'resolved':   sum(1 for c in assigned if c.status in ('resolved', 'closed')),
    }
    notif_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('staff/dashboard.html',
                           assigned=assigned, stats=stats,
                           pending=pending, notif_count=notif_count)


@staff_bp.route('/complaint/<int:cid>')
@login_required
@staff_required
def complaint_detail(cid):
    c = Complaint.query.get_or_404(cid)
    timeline    = c.timeline.order_by(TimelineEvent.created_at).all()
    notif_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('staff/detail.html', complaint=c,
                           timeline=timeline, notif_count=notif_count)


@staff_bp.route('/update/<int:cid>', methods=['POST'])
@login_required
@staff_required
def update_status(cid):
    c = Complaint.query.get_or_404(cid)
    if c.assigned_to != current_user.id:
        flash('You are not assigned to this complaint.', 'danger')
        return redirect(url_for('staff.dashboard'))

    new_status = request.form.get('status')
    note       = request.form.get('note', '').strip() or f'Status updated to {new_status} by {current_user.name}.'

    c.status     = new_status
    c.updated_at = datetime.utcnow()
    ev = TimelineEvent(complaint_id=cid, status=new_status, note=note,
                       created_at=datetime.utcnow())
    db.session.add(ev)

    # Notify student
    notif = Notification(
        user_id=c.student_id,
        title='Complaint Status Updated',
        message=f'Your complaint "{c.title}" is now: {new_status.upper()}.'
    )
    db.session.add(notif)
    db.session.commit()

    flash(f'Status updated to "{new_status}" successfully.', 'success')
    return redirect(url_for('staff.complaint_detail', cid=cid))


@staff_bp.route('/all')
@login_required
@staff_required
def all_complaints():
    complaints  = Complaint.query.order_by(Complaint.created_at.desc()).all()
    notif_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('staff/all_complaints.html',
                           complaints=complaints, notif_count=notif_count)
