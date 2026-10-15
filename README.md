# 🎓 Student Complaint & Feedback Management System (SCFMS)

**Pillai HOC College of Engineering and Technology, Rasayani (Institute Code: 1148)**  
**Academic Year: 2026-27 | Subject: Software Engineering (315323) | Semester: 5, K-Scheme**  
**Guide Teacher:** Prof. Priyanka Kale  

---

## 👥 Group Members

| Sr. No. | Student Name | Enrollment No. | Seat No. |
|:---:|---|:---:|:---:|
| 1 | **Chetan Amit Sonawane** | 25112270317 | *(To be allotted)* |
| 2 | **Gawand Shubham Naresh** | 25112270309 | *(To be allotted)* |
| 3 | **Kavya Rajendra Patil** | 25112270322 | *(To be allotted)* |

---

## 🚀 Running the Flask Application

### Method 1 (Quick Double-Click):
Double-click [`run.bat`](file:///d:/Student%20Complaint%20&%20Feedback%20Management%20System/run.bat).

### Method 2 (Terminal):
```powershell
python run.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 🔐 User Logins (Stored in SQLite Database)

*(Note: Passwords are encrypted with PBKDF2/SHA-256 and removed from the public UI on the login page as requested)*

| Role | Name | Email | Password |
|---|---|---|---|
| **Student** | Chetan Amit Sonawane | `student@pillai.edu` | `student123` |
| **Student** | Gawand Shubham Naresh | `shubham@pillai.edu` | `shubham123` |
| **Student** | Kavya Rajendra Patil | `kavya@pillai.edu` | `kavya123` |
| **Staff / HOD** | Prof. Priyanka Kale | `staff@pillai.edu` | `staff123` |
| **Staff / Warden** | Mr. Rajesh Warden | `warden@pillai.edu` | `warden123` |
| **Admin** | System Administrator | `admin@pillai.edu` | `admin123` |

---

## 📋 Pre-Seeded Realistic Complaints (12 Samples)

1. **#1 (Hostel, High - Resolved):** *No water supply in Hostel Block B for 3 days* (with full timeline & 4-star feedback)
2. **#2 (Mess, Medium - In Progress):** *Mess food quality is very poor and unhygienic* (hygiene meeting scheduled)
3. **#3 (Lab, High - Assigned):** *8 computers non-functional in Computer Lab No. 2* (RAM/booting issues)
4. **#4 (Library, Low - Submitted):** *Reference books not available – issued but not returned*
5. **#5 (Faculty, Medium - Closed):** *Syllabus not covered on time – Fluid Mechanics (Unit 4)* (Extra lectures scheduled & 5-star feedback)
6. **#6 (Hostel, Medium - Resolved):** *Hostel room lights and fan not working in Room 214* (Wiring/MCB repair)
7. **#7 (Other, High - Submitted):** *Campus WiFi not working in academic building since Monday*
8. **#8 (Mess, High - In Progress):** *Food poisoning incident – 10 students affected after dinner* (Urgent health inspection)
9. **#9 (Lab, Medium - Submitted):** *Projector in Lecture Hall 3 is broken – no display*
10. **#10 (Library, Low - Closed):** *Library timings too short – closes at 5 PM* (Extended to 7 PM with student confirmation)
11. **#11 (Faculty, High - Assigned):** *Faculty using abusive language in class – very unprofessional* (Escalated to HOD)
12. **#12 (Other, Low - Resolved):** *Canteen price list outdated – being overcharged* (Revised price board installed)

---

## 📊 Software Engineering Metrics Included in App & Report

- **Process Model:** Agile Scrum & Incremental
- **COCOMO Estimation (Organic Mode):**
  - Project Size: **~3.0 KLOC**
  - Effort = $2.4 \times (3)^{1.05} \approx \mathbf{7.6\text{ Person-Months}}$
  - Time = $2.5 \times (7.6)^{0.38} \approx \mathbf{5.4\text{ Months}}$
  - Team Size = $7.6 / 5.4 \approx \mathbf{3\text{ Developers}}$
- **Function Point (FP):** $111\text{ UFP}$
- **SQA Plan:** Quality attributes, peer review checkpoints, validation test cases.
