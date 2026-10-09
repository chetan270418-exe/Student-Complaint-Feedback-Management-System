"""
Seed Database – fills initial users and realistic fake complaints.
Runs only once (checks if admin already exists).
"""

from datetime import datetime, timedelta


def seed_database():
    from app import db
    from models.models import User, Complaint, TimelineEvent, Feedback, Notification

    # Already seeded?
    if User.query.filter_by(email='admin@pillai.edu').first():
        return

    # ─── USERS ───────────────────────────────────────────────────────
    def make_user(**kwargs):
        u = User(**{k: v for k, v in kwargs.items() if k != 'password'})
        u.set_password(kwargs['password'])
        db.session.add(u)
        return u

    # Admin
    admin = make_user(name='Admin User', email='admin@pillai.edu',
                      password='admin123', role='admin', department='Administration')

    # Staff
    staff1 = make_user(name='Prof. Priyanka Kale',   email='staff@pillai.edu',
                       password='staff123', role='staff',
                       department='Computer Engineering', designation='HOD')
    staff2 = make_user(name='Mr. Rajesh Warden',     email='warden@pillai.edu',
                       password='warden123', role='staff',
                       department='Hostel Management', designation='Warden')
    staff3 = make_user(name='Prof. Neha Sharma',     email='neha@pillai.edu',
                       password='neha123', role='staff',
                       department='Library', designation='Librarian')

    # Students
    s1 = make_user(name='Chetan Amit Sonawane',   email='student@pillai.edu',
                   password='student123', role='student',
                   roll_no='25112270317', branch='Computer Engineering', semester=5)
    s2 = make_user(name='Gawand Shubham Naresh',  email='shubham@pillai.edu',
                   password='shubham123', role='student',
                   roll_no='25112270309', branch='Computer Engineering', semester=5)
    s3 = make_user(name='Kavya Rajendra Patil',   email='kavya@pillai.edu',
                   password='kavya123', role='student',
                   roll_no='25112270322', branch='Computer Engineering', semester=5)
    s4 = make_user(name='Rohit Deshmukh',         email='rohit@pillai.edu',
                   password='rohit123', role='student',
                   roll_no='25112270301', branch='Mechanical Engineering', semester=3)
    s5 = make_user(name='Priya Nair',             email='priya@pillai.edu',
                   password='priya123', role='student',
                   roll_no='25112270345', branch='Civil Engineering', semester=1)
    s6 = make_user(name='Aakash More',            email='aakash@pillai.edu',
                   password='aakash123', role='student',
                   roll_no='25112270298', branch='Electronics Engineering', semester=4)

    db.session.flush()   # get IDs

    # ─── HELPER ──────────────────────────────────────────────────────
    def ago(days=0, hours=0):
        return datetime.utcnow() - timedelta(days=days, hours=hours)

    def add_complaint(student, title, desc, category, priority,
                      status, assignee=None, created_days_ago=7,
                      events=None, fb_rating=None, fb_comment=None):
        c = Complaint(
            student_id  = student.id,
            assigned_to = assignee.id if assignee else None,
            title       = title,
            description = desc,
            category    = category,
            priority    = priority,
            status      = status,
            created_at  = ago(created_days_ago),
            updated_at  = ago(0)
        )
        db.session.add(c)
        db.session.flush()

        # Timeline
        for ev in (events or []):
            t = TimelineEvent(complaint_id=c.id, status=ev['status'],
                              note=ev['note'],
                              created_at=ago(ev.get('days_ago', 1), ev.get('hours_ago', 0)))
            db.session.add(t)

        # Feedback
        if fb_rating:
            fb = Feedback(complaint_id=c.id, student_id=student.id,
                          rating=fb_rating, comment=fb_comment or '')
            db.session.add(fb)

        return c

    # ─── COMPLAINTS ───────────────────────────────────────────────────

    # 1 – RESOLVED (Hostel, High)
    add_complaint(
        student=s1, category='hostel', priority='high', status='resolved',
        title='No water supply in Hostel Block B for 3 days',
        desc='There is absolutely no water supply in Block B from the past 3 days. Students cannot bathe, wash utensils or use washrooms properly. This is a severe health and hygiene issue affecting around 60 students.',
        assignee=staff2, created_days_ago=10,
        events=[
            {'status':'submitted',  'note':'Complaint submitted by student.', 'days_ago':10},
            {'status':'assigned',   'note':'Assigned to Warden Rajesh for urgent action.', 'days_ago':9, 'hours_ago':18},
            {'status':'inprogress', 'note':'Plumber team deployed. Pipe leakage identified in main supply line.', 'days_ago':9},
            {'status':'resolved',   'note':'Main supply pipe repaired. Water flow restored to all rooms in Block B.', 'days_ago':7},
        ],
        fb_rating=4, fb_comment='Good response time! Fixed within 3 days.'
    )

    # 2 – IN PROGRESS (Mess, Medium)
    add_complaint(
        student=s1, category='mess', priority='medium', status='inprogress',
        title='Mess food quality is very poor and unhygienic',
        desc='The food served in the college mess for the past 2 weeks has been of very poor quality. Rice is undercooked, dal is watery, and vegetables appear stale and smell odd. At least 15 students reported stomach issues last week. We request immediate inspection of the mess kitchen and contractor.',
        assignee=staff1, created_days_ago=5,
        events=[
            {'status':'submitted',  'note':'Complaint submitted.', 'days_ago':5},
            {'status':'assigned',   'note':'Assigned to HOD Prof. Priyanka Kale.', 'days_ago':4, 'hours_ago':20},
            {'status':'inprogress', 'note':'Meeting with mess contractor scheduled for Friday. Hygiene inspection arranged.', 'days_ago':3},
        ]
    )

    # 3 – ASSIGNED (Lab, High)
    add_complaint(
        student=s2, category='lab', priority='high', status='assigned',
        title='8 computers non-functional in Computer Lab No. 2',
        desc='Out of 20 computers in Lab No. 2 (ground floor), 8 systems are completely non-functional. They crash within 5 minutes of booting. This is causing major disruption during practical sessions and students are sharing systems, losing marks in viva due to incomplete practicals. RAM or HDD issue suspected.',
        assignee=staff1, created_days_ago=3,
        events=[
            {'status':'submitted', 'note':'Complaint submitted by student.', 'days_ago':3},
            {'status':'assigned',  'note':'Assigned to HOD for hardware inspection and repair.', 'days_ago':2, 'hours_ago':20},
        ]
    )

    # 4 – SUBMITTED (Library, Low)
    add_complaint(
        student=s3, category='library', priority='low', status='submitted',
        title='Reference books not available – issued but not returned',
        desc='Many important reference books (especially Roger Pressman\'s Software Engineering and DBMS by Korth) are always shown as "Issued" in the library system but never available on the shelf. It appears students have held them for months without returning. We request the library to enforce a strict return policy and impose fines.',
        created_days_ago=1,
        events=[
            {'status':'submitted', 'note':'Complaint submitted by student.', 'days_ago':1},
        ]
    )

    # 5 – CLOSED (Faculty, Medium)
    add_complaint(
        student=s2, category='faculty', priority='medium', status='closed',
        title='Syllabus not covered on time – Fluid Mechanics (Unit 4)',
        desc='The faculty for Fluid Mechanics has only covered 2.5 out of 5 units as of Week 10. We are already nearing the end-semester exam and the pace is too slow. No extra lectures have been arranged. Students are extremely worried about exams.',
        assignee=staff1, created_days_ago=20,
        events=[
            {'status':'submitted',  'note':'Complaint submitted.', 'days_ago':20},
            {'status':'assigned',   'note':'Forwarded to HOD for review.', 'days_ago':19, 'hours_ago':18},
            {'status':'inprogress', 'note':'Faculty counselled. Schedule of extra Saturday lectures prepared.', 'days_ago':17},
            {'status':'resolved',   'note':'Extra lectures started from Saturday. Syllabus is back on track.', 'days_ago':10},
            {'status':'closed',     'note':'Student confirmed satisfaction. Complaint officially closed.', 'days_ago':7},
        ],
        fb_rating=5, fb_comment='Very happy! Extra classes helped a lot. Thank you Prof. Kale!'
    )

    # 6 – RESOLVED (Hostel, Medium)
    add_complaint(
        student=s4, category='hostel', priority='medium', status='resolved',
        title='Hostel room lights and fan not working in Room 214',
        desc='Room 214 in Block A hostel has had non-functional lights and ceiling fan for the past 5 days. An electrician was called once but did not fix it properly. The problem is recurring. Students in this room are suffering, especially during the hot weather.',
        assignee=staff2, created_days_ago=8,
        events=[
            {'status':'submitted',  'note':'Complaint submitted.', 'days_ago':8},
            {'status':'assigned',   'note':'Assigned to Warden. Electrician called.', 'days_ago':7, 'hours_ago':20},
            {'status':'inprogress', 'note':'Wiring fault found in MCB board. Replacement parts ordered.', 'days_ago':6},
            {'status':'resolved',   'note':'New MCB installed. All electrical points in room 214 working normally.', 'days_ago':4},
        ],
        fb_rating=3, fb_comment='Took a bit long but resolved eventually.'
    )

    # 7 – SUBMITTED (Other, High)
    add_complaint(
        student=s5, category='other', priority='high', status='submitted',
        title='Campus WiFi not working in academic building since Monday',
        desc='The WiFi network in the main academic building (floors 1-3) has been completely down since Monday morning. Students cannot access online resources, submit assignments, or attend online sessions for supplementary courses (Infosys Springboard etc.). The IT department has not responded despite multiple complaints at the helpdesk.',
        created_days_ago=2,
        events=[
            {'status':'submitted', 'note':'Complaint submitted by student.', 'days_ago':2},
        ]
    )

    # 8 – IN PROGRESS (Mess, High)
    add_complaint(
        student=s6, category='mess', priority='high', status='inprogress',
        title='Food poisoning incident – 10 students affected after dinner',
        desc='On the evening of 7th October, approximately 10 students fell ill after consuming dinner from the college mess. Symptoms include vomiting, diarrhoea, and severe stomach cramps. Three students were taken to the college dispensary. This is a critical food safety issue. We request immediate suspension of the current mess contractor pending a health inspection.',
        assignee=staff1, created_days_ago=2,
        events=[
            {'status':'submitted',  'note':'Complaint submitted. URGENT – food poisoning incident.', 'days_ago':2},
            {'status':'assigned',   'note':'Assigned to HOD on emergency basis. Principal informed.', 'days_ago':2, 'hours_ago':16},
            {'status':'inprogress', 'note':'College doctor visited affected students. Mess temporarily closed. Health authority inspection scheduled for tomorrow.', 'days_ago':1},
        ]
    )

    # 9 – SUBMITTED (Lab, Medium)
    add_complaint(
        student=s3, category='lab', priority='medium', status='submitted',
        title='Projector in Lecture Hall 3 is broken – no display',
        desc='The projector in Lecture Hall No. 3 has not been working for over a week. Faculty are unable to show presentations, diagrams or online resources during lectures. This is affecting teaching quality for 4 different subjects that use this hall. A portable projector or immediate repair is needed.',
        created_days_ago=4,
        events=[
            {'status':'submitted', 'note':'Complaint submitted.', 'days_ago':4},
        ]
    )

    # 10 – CLOSED (Library, Low)
    add_complaint(
        student=s4, category='library', priority='low', status='closed',
        title='Library timings too short – closes at 5 PM',
        desc='The library closes at 5:00 PM every day which is insufficient for students who have practicals till 4:30 PM. We request extension of library hours till at least 7:00 PM on weekdays and 6:00 PM on Saturdays to allow students enough time to study and access resources.',
        assignee=staff3, created_days_ago=15,
        events=[
            {'status':'submitted',  'note':'Complaint submitted.', 'days_ago':15},
            {'status':'assigned',   'note':'Assigned to Librarian Mrs. Neha Sharma.', 'days_ago':14},
            {'status':'inprogress', 'note':'Proposal sent to Principal for extended library hours.', 'days_ago':12},
            {'status':'resolved',   'note':'Principal approved extended hours. Library now open till 7 PM on weekdays.', 'days_ago':5},
            {'status':'closed',     'note':'Student confirmed. Complaint closed successfully.', 'days_ago':3},
        ],
        fb_rating=5, fb_comment='Amazing! Library extended to 7 PM. Very helpful for us!'
    )

    # 11 – ASSIGNED (Faculty, High)
    add_complaint(
        student=s5, category='faculty', priority='high', status='assigned',
        title='Faculty using abusive language in class – very unprofessional',
        desc='A faculty member in the Mechanical department uses humiliating and sometimes abusive language toward students who do not answer correctly. Several students are mentally stressed and afraid to attend those classes. We request strict action as per the college code of conduct. We are ready to provide a written statement with signatures from 20+ students.',
        assignee=staff1, created_days_ago=1,
        events=[
            {'status':'submitted', 'note':'Complaint submitted.', 'days_ago':1},
            {'status':'assigned',  'note':'Escalated to HOD. Confidential inquiry to be initiated.', 'days_ago':0, 'hours_ago':8},
        ]
    )

    # 12 – RESOLVED (Other, Low)
    add_complaint(
        student=s6, category='other', priority='low', status='resolved',
        title='Canteen price list outdated – being overcharged',
        desc='The price list displayed at the college canteen is from 2023 but the canteen owner is charging 2025 rates without any official notification or revised price board. Students are paying Rs 5-10 more per item than the displayed price. We request the admin to issue an updated official price list and display it prominently.',
        assignee=admin, created_days_ago=12,
        events=[
            {'status':'submitted',  'note':'Complaint submitted.', 'days_ago':12},
            {'status':'assigned',   'note':'Assigned to Admin office for verification.', 'days_ago':11},
            {'status':'inprogress', 'note':'Canteen owner asked to submit revised price list. Verification in progress.', 'days_ago':9},
            {'status':'resolved',   'note':'New official price list printed and displayed at canteen. Canteen owner warned.', 'days_ago':5},
        ],
        fb_rating=4, fb_comment='Issue resolved. Prices are fair now.'
    )

    # ─── NOTIFICATIONS ────────────────────────────────────────────────
    def notify(user, title, msg):
        n = Notification(user_id=user.id, title=title, message=msg, is_read=False,
                         created_at=ago(0))
        db.session.add(n)

    notify(s1, 'Complaint Resolved', 'Your complaint "No water supply in Hostel Block B" has been resolved.')
    notify(s2, 'Complaint Closed',   'Your complaint "Syllabus not covered on time" has been closed. Please give feedback.')
    notify(s3, 'Complaint Submitted','Your complaint "Reference books not available" has been received. Complaint ID: 4')
    notify(staff1, 'New Complaint Assigned', '3 new complaints have been assigned to you. Please take action.')
    notify(admin,  'New Complaint Received', 'Complaint "Campus WiFi not working" submitted by Priya Nair. Unassigned.')

    db.session.commit()
    print("  [DB] Database seeded with users + 12 realistic complaints.")
