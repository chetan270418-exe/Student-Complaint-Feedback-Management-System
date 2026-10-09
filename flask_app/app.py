"""
Student Complaint & Feedback Management System
Flask Application - Main Entry Point

Institute  : Pillai HOC Polytechnic, Rasayani (Code: 1148)
Course     : Software Engineering (315323), Sem 5, K-Scheme
Guide      : Prof. Priyanka Kale
Academic Year: 2026-27

Team Members:
  1. Chetan Amit Sonawane   (25112270317)
  2. Gawand Shubham Naresh  (25112270309)
  3. Kavya Rajendra Patil   (25112270322)
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# ── Extensions (created before app) ──────────────────────────────────
db           = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # ── Config ───────────────────────────────────────────────────────
    app.config['SECRET_KEY'] = 'scfms-pillai-hoc-2026-27'
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'scfms.db')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ── Init Extensions ───────────────────────────────────────────────
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view      = 'auth.login'
    login_manager.login_message   = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    # ── Register Blueprints ───────────────────────────────────────────
    from routes.auth     import auth_bp
    from routes.student  import student_bp
    from routes.staff    import staff_bp
    from routes.admin    import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp,  url_prefix='/student')
    app.register_blueprint(staff_bp,    url_prefix='/staff')
    app.register_blueprint(admin_bp,    url_prefix='/admin')

    # ── Create DB + Seed ──────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        from utils.seed import seed_database
        seed_database()

    return app


if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*55)
    print("  SCFMS - Student Complaint & Feedback Management System")
    print("  Pillai HOC Polytechnic, Rasayani | Code: 1148")
    print("  Guide: Prof. Priyanka Kale | AY: 2026-27")
    print("="*55)
    print("  Open in browser: http://127.0.0.1:5000")
    print("="*55 + "\n")
    app.run(debug=True, port=5000)
