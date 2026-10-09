"""
Models – SQLAlchemy ORM definitions
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


# ─── USER ─────────────────────────────────────────────────────────────
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    password    = db.Column(db.String(256), nullable=False)
    role        = db.Column(db.String(20), nullable=False)   # student / staff / admin

    # Student-specific
    roll_no     = db.Column(db.String(30))
    branch      = db.Column(db.String(100))
    semester    = db.Column(db.Integer)

    # Staff-specific
    department  = db.Column(db.String(100))
    designation = db.Column(db.String(100))

    # Relationships
    complaints_submitted = db.relationship('Complaint', foreign_keys='Complaint.student_id',
                                           back_populates='student', lazy='dynamic')
    complaints_assigned  = db.relationship('Complaint', foreign_keys='Complaint.assigned_to',
                                           back_populates='assignee', lazy='dynamic')
    notifications = db.relationship('Notification', back_populates='user', lazy='dynamic',
                                    cascade='all, delete-orphan')
    feedbacks     = db.relationship('Feedback', back_populates='student', lazy='dynamic')

    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    def __repr__(self):
        return f'<User {self.email} [{self.role}]>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─── COMPLAINT ─────────────────────────────────────────────────────────
class Complaint(db.Model):
    __tablename__ = 'complaints'

    id          = db.Column(db.Integer, primary_key=True)
    student_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category    = db.Column(db.String(50), nullable=False)   # hostel/mess/lab/faculty/library/other
    priority    = db.Column(db.String(20), nullable=False)   # high/medium/low
    status      = db.Column(db.String(30), default='submitted')  # submitted/assigned/inprogress/resolved/closed

    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student     = db.relationship('User', foreign_keys=[student_id], back_populates='complaints_submitted')
    assignee    = db.relationship('User', foreign_keys=[assigned_to], back_populates='complaints_assigned')
    timeline    = db.relationship('TimelineEvent', back_populates='complaint',
                                  lazy='dynamic', cascade='all, delete-orphan',
                                  order_by='TimelineEvent.created_at')
    feedback    = db.relationship('Feedback', back_populates='complaint',
                                  uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Complaint #{self.id}: {self.title[:40]}>'


# ─── TIMELINE EVENT ────────────────────────────────────────────────────
class TimelineEvent(db.Model):
    __tablename__ = 'timeline_events'

    id           = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)
    status       = db.Column(db.String(30), nullable=False)
    note         = db.Column(db.Text)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    complaint    = db.relationship('Complaint', back_populates='timeline')


# ─── FEEDBACK ──────────────────────────────────────────────────────────
class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id           = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)
    student_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating       = db.Column(db.Integer, nullable=False)   # 1-5
    comment      = db.Column(db.Text)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    complaint    = db.relationship('Complaint', back_populates='feedback')
    student      = db.relationship('User', back_populates='feedbacks')


# ─── NOTIFICATION ──────────────────────────────────────────────────────
class Notification(db.Model):
    __tablename__ = 'notifications'

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title      = db.Column(db.String(200))
    message    = db.Column(db.Text)
    is_read    = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user       = db.relationship('User', back_populates='notifications')
