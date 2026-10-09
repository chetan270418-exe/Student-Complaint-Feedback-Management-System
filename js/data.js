/**
 * DATA LAYER - Student Complaint & Feedback Management System
 * Handles localStorage persistence for all application data.
 * Pillai HOC Polytechnic | STE Course 315323 | Sem 5 K-Scheme
 * Team: Chetan Amit Sonawane, Gawand Shubham Naresh, Kavya Rajendra Patil
 */

// ─── INITIAL SEED DATA ────────────────────────────────────────────────
const SEED_USERS = [
  // Students
  { id: 'u1', role: 'student', name: 'Rahul Sharma',      email: 'student@pillai.edu',  password: 'student123', rollNo: '2511001', branch: 'Computer Engineering',    semester: 5 },
  { id: 'u2', role: 'student', name: 'Priya Desai',       email: 'priya@pillai.edu',    password: 'priya123',   rollNo: '2511002', branch: 'Mechanical Engineering',  semester: 3 },
  { id: 'u3', role: 'student', name: 'Arjun Mehta',       email: 'arjun@pillai.edu',    password: 'arjun123',   rollNo: '2511003', branch: 'Civil Engineering',       semester: 1 },
  // Staff
  { id: 'u4', role: 'staff',   name: 'Prof. Amit Kumar',  email: 'staff@pillai.edu',    password: 'staff123',   department: 'Computer Engineering', designation: 'HOD' },
  { id: 'u5', role: 'staff',   name: 'Prof. Sunita Rao',  email: 'sunita@pillai.edu',   password: 'sunita123',  department: 'Hostel Management',    designation: 'Warden' },
  // Admin
  { id: 'u6', role: 'admin',   name: 'Admin User',        email: 'admin@pillai.edu',    password: 'admin123',   department: 'Administration' }
];

const SEED_COMPLAINTS = [
  {
    id: 'c1', studentId: 'u1', studentName: 'Rahul Sharma', rollNo: '2511001',
    title: 'Water supply issue in Hostel Block B',
    description: 'There is no water supply in Block B from past 3 days. Students are facing severe inconvenience.',
    category: 'hostel', priority: 'high', status: 'resolved',
    assignedTo: 'u5', assignedName: 'Prof. Sunita Rao',
    createdAt: '2025-10-01T09:00:00', updatedAt: '2025-10-03T14:00:00',
    timeline: [
      { status: 'submitted',   date: '2025-10-01T09:00:00', note: 'Complaint submitted by student.' },
      { status: 'assigned',    date: '2025-10-01T10:30:00', note: 'Assigned to Warden Sunita Rao.' },
      { status: 'inprogress',  date: '2025-10-02T08:00:00', note: 'Plumber called, pipe repair in progress.' },
      { status: 'resolved',    date: '2025-10-03T14:00:00', note: 'Water supply restored. Issue fixed.' }
    ],
    feedback: { rating: 4, comment: 'Good response time!' }
  },
  {
    id: 'c2', studentId: 'u1', studentName: 'Rahul Sharma', rollNo: '2511001',
    title: 'Mess food quality is very poor',
    description: 'The food served in mess for the past 2 weeks has been of very poor quality. Undercooked rice and stale vegetables.',
    category: 'mess', priority: 'medium', status: 'inprogress',
    assignedTo: 'u4', assignedName: 'Prof. Amit Kumar',
    createdAt: '2025-10-05T11:00:00', updatedAt: '2025-10-06T09:00:00',
    timeline: [
      { status: 'submitted',  date: '2025-10-05T11:00:00', note: 'Complaint submitted.' },
      { status: 'assigned',   date: '2025-10-05T13:00:00', note: 'Assigned to HOD Amit Kumar.' },
      { status: 'inprogress', date: '2025-10-06T09:00:00', note: 'Meeting with mess contractor scheduled.' }
    ],
    feedback: null
  },
  {
    id: 'c3', studentId: 'u2', studentName: 'Priya Desai', rollNo: '2511002',
    title: 'Lab computers not working in Lab 2',
    description: '8 out of 20 computers in Lab 2 are not working. System crashes frequently during practicals.',
    category: 'lab', priority: 'high', status: 'assigned',
    assignedTo: 'u4', assignedName: 'Prof. Amit Kumar',
    createdAt: '2025-10-07T08:30:00', updatedAt: '2025-10-07T10:00:00',
    timeline: [
      { status: 'submitted', date: '2025-10-07T08:30:00', note: 'Complaint submitted.' },
      { status: 'assigned',  date: '2025-10-07T10:00:00', note: 'Assigned to HOD for action.' }
    ],
    feedback: null
  },
  {
    id: 'c4', studentId: 'u3', studentName: 'Arjun Mehta', rollNo: '2511003',
    title: 'Library books not returned by students',
    description: 'Many reference books are not available as students have not returned them. Library needs strict policy.',
    category: 'library', priority: 'low', status: 'submitted',
    assignedTo: null, assignedName: null,
    createdAt: '2025-10-08T15:00:00', updatedAt: '2025-10-08T15:00:00',
    timeline: [
      { status: 'submitted', date: '2025-10-08T15:00:00', note: 'Complaint submitted by student.' }
    ],
    feedback: null
  },
  {
    id: 'c5', studentId: 'u2', studentName: 'Priya Desai', rollNo: '2511002',
    title: 'Faculty not covering syllabus on time',
    description: 'The fluid mechanics faculty has only covered 30% syllabus and we are already in Unit 4.',
    category: 'faculty', priority: 'medium', status: 'closed',
    assignedTo: 'u4', assignedName: 'Prof. Amit Kumar',
    createdAt: '2025-09-20T10:00:00', updatedAt: '2025-09-28T16:00:00',
    timeline: [
      { status: 'submitted',  date: '2025-09-20T10:00:00', note: 'Complaint submitted.' },
      { status: 'assigned',   date: '2025-09-20T12:00:00', note: 'Forwarded to HOD.' },
      { status: 'inprogress', date: '2025-09-22T09:00:00', note: 'Faculty counselled and extra lectures planned.' },
      { status: 'resolved',   date: '2025-09-26T16:00:00', note: 'Extra classes started. Syllabus back on track.' },
      { status: 'closed',     date: '2025-09-28T16:00:00', note: 'Complaint closed. Student satisfied.' }
    ],
    feedback: { rating: 5, comment: 'Excellent resolution!' }
  }
];

const SEED_NOTIFICATIONS = [
  { id: 'n1', userId: 'u1', title: 'Complaint Resolved', message: 'Your complaint "Water supply issue" has been resolved.', read: false, date: '2025-10-03T14:00:00' },
  { id: 'n2', userId: 'u1', title: 'Status Update',      message: 'Your complaint "Mess food quality" is now in progress.', read: false, date: '2025-10-06T09:00:00' },
  { id: 'n3', userId: 'u4', title: 'New Complaint Assigned', message: 'Complaint "Lab computers not working" has been assigned to you.', read: false, date: '2025-10-07T10:00:00' },
  { id: 'n4', userId: 'u5', title: 'Complaint Assigned', message: 'Complaint "Water supply issue" has been assigned to you.', read: true,  date: '2025-10-01T10:30:00' }
];

// ─── INIT DATABASE ────────────────────────────────────────────────────
function initDB() {
  if (!localStorage.getItem('scfms_users')) {
    localStorage.setItem('scfms_users', JSON.stringify(SEED_USERS));
  }
  if (!localStorage.getItem('scfms_complaints')) {
    localStorage.setItem('scfms_complaints', JSON.stringify(SEED_COMPLAINTS));
  }
  if (!localStorage.getItem('scfms_notifications')) {
    localStorage.setItem('scfms_notifications', JSON.stringify(SEED_NOTIFICATIONS));
  }
}

// ─── CRUD HELPERS ─────────────────────────────────────────────────────
function getDB(key)           { return JSON.parse(localStorage.getItem(key) || '[]'); }
function setDB(key, data)     { localStorage.setItem(key, JSON.stringify(data)); }

function getUsers()       { return getDB('scfms_users'); }
function getComplaints()  { return getDB('scfms_complaints'); }
function setComplaints(d) { setDB('scfms_complaints', d); }
function getNotifications() { return getDB('scfms_notifications'); }
function setNotifications(d){ setDB('scfms_notifications', d); }

// ─── USER OPERATIONS ──────────────────────────────────────────────────
function getUserById(id)    { return getUsers().find(u => u.id === id) || null; }
function addUser(user)      { const u = getUsers(); u.push(user); setDB('scfms_users', u); }

function generateId(prefix) {
  return prefix + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

// ─── COMPLAINT OPERATIONS ─────────────────────────────────────────────
function getComplaintById(id) { return getComplaints().find(c => c.id === id); }

function addComplaint(data) {
  const complaints = getComplaints();
  const user = getCurrentUser();
  const newComplaint = {
    id: generateId('c'),
    studentId: user.id,
    studentName: user.name,
    rollNo: user.rollNo || 'N/A',
    title: data.title,
    description: data.description,
    category: data.category,
    priority: data.priority,
    status: 'submitted',
    assignedTo: null,
    assignedName: null,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    timeline: [{ status: 'submitted', date: new Date().toISOString(), note: 'Complaint submitted by student.' }],
    feedback: null
  };
  complaints.push(newComplaint);
  setComplaints(complaints);
  addNotification('u6', 'New Complaint Received', `New complaint "${data.title}" submitted by ${user.name}.`);
  return newComplaint;
}

function updateComplaintStatus(complaintId, status, note, assignedTo) {
  const complaints = getComplaints();
  const idx = complaints.findIndex(c => c.id === complaintId);
  if (idx === -1) return false;
  const c = complaints[idx];
  c.status = status;
  c.updatedAt = new Date().toISOString();
  if (assignedTo) {
    const staff = getUserById(assignedTo);
    c.assignedTo = assignedTo;
    c.assignedName = staff ? staff.name : assignedTo;
  }
  c.timeline.push({ status, date: new Date().toISOString(), note: note || `Status changed to ${status}.` });
  complaints[idx] = c;
  setComplaints(complaints);
  addNotification(c.studentId, 'Complaint Status Updated', `Your complaint "${c.title}" status is now: ${status}.`);
  return true;
}

function addFeedback(complaintId, rating, comment) {
  const complaints = getComplaints();
  const idx = complaints.findIndex(c => c.id === complaintId);
  if (idx === -1) return false;
  complaints[idx].feedback = { rating, comment };
  setComplaints(complaints);
  return true;
}

function deleteComplaint(id) {
  const complaints = getComplaints().filter(c => c.id !== id);
  setComplaints(complaints);
}

// ─── NOTIFICATION OPERATIONS ──────────────────────────────────────────
function addNotification(userId, title, message) {
  const notifications = getNotifications();
  notifications.unshift({ id: generateId('n'), userId, title, message, read: false, date: new Date().toISOString() });
  setNotifications(notifications);
}

function markAllRead(userId) {
  const notifications = getNotifications().map(n => n.userId === userId ? { ...n, read: true } : n);
  setNotifications(notifications);
}

function getUserNotifications(userId) {
  return getNotifications().filter(n => n.userId === userId);
}

// ─── STATS ────────────────────────────────────────────────────────────
function getComplaintStats(userId, role) {
  let complaints = getComplaints();
  if (role === 'student')      complaints = complaints.filter(c => c.studentId === userId);
  else if (role === 'staff')   complaints = complaints.filter(c => c.assignedTo === userId);
  const total      = complaints.length;
  const submitted  = complaints.filter(c => c.status === 'submitted').length;
  const inprogress = complaints.filter(c => ['assigned','inprogress'].includes(c.status)).length;
  const resolved   = complaints.filter(c => c.status === 'resolved').length;
  const closed     = complaints.filter(c => c.status === 'closed').length;
  return { total, submitted, inprogress, resolved, closed };
}

// Initialize DB on load
initDB();
