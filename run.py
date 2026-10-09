"""
Root launcher for Student Complaint & Feedback Management System (SCFMS)
Flask Web Application

Institute  : Pillai HOC Polytechnic, Rasayani (Code: 1148)
Guide      : Prof. Priyanka Kale
Academic Year: 2026-27
"""

import sys
import os

# Add flask_app to path
base_dir = os.path.dirname(os.path.abspath(__file__))
flask_dir = os.path.join(base_dir, 'flask_app')
sys.path.insert(0, flask_dir)

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n" + "=" * 65)
    print("  STUDENT COMPLAINT & FEEDBACK MANAGEMENT SYSTEM (SCFMS)")
    print("  Pillai HOC Polytechnic, Rasayani | Code: 1148")
    print("  Guide: Prof. Priyanka Kale | Academic Year: 2026-27")
    print("  Team: Chetan Sonawane | Gawand Shubham | Kavya Patil")
    print("=" * 65)
    print("  Server running at: http://127.0.0.1:5000")
    print("=" * 65 + "\n")
    app.run(debug=True, port=5000)
