/**
 * AUTH MODULE - Student Complaint & Feedback Management System
 * Handles login, registration, session management.
 */

const SESSION_KEY = 'scfms_session';

// ─── LOGIN ────────────────────────────────────────────────────────────
function loginUser(email, password, role) {
  const users = getDB('scfms_users');
  const user = users.find(u => u.email === email && u.password === password && u.role === role);
  if (!user) {
    return { success: false, message: 'Invalid credentials or wrong role selected.' };
  }
  // Save session
  sessionStorage.setItem(SESSION_KEY, JSON.stringify({ id: user.id, role: user.role, name: user.name }));
  const redirectMap = { student: 'pages/student-dashboard.html', staff: 'pages/staff-dashboard.html', admin: 'pages/admin-dashboard.html' };
  return { success: true, redirect: redirectMap[role] };
}

// ─── REGISTER ─────────────────────────────────────────────────────────
function registerStudent(data) {
  const users = getDB('scfms_users');
  if (users.find(u => u.email === data.email)) {
    return { success: false, message: 'Email already registered.' };
  }
  const newUser = {
    id: 'u' + Date.now(),
    role: 'student',
    name: data.name,
    email: data.email,
    password: data.password,
    rollNo: data.rollNo,
    branch: data.branch,
    semester: parseInt(data.semester)
  };
  users.push(newUser);
  setDB('scfms_users', users);
  return { success: true };
}

// ─── SESSION ──────────────────────────────────────────────────────────
function getCurrentUser() {
  const session = sessionStorage.getItem(SESSION_KEY);
  if (!session) return null;
  const s = JSON.parse(session);
  return getUserById(s.id);
}

function requireAuth(expectedRole) {
  const user = getCurrentUser();
  if (!user) { window.location.href = '/index.html'; return null; }
  // Navigate relative to pages/ directory
  const base = window.location.pathname.includes('/pages/') ? '../index.html' : 'index.html';
  if (expectedRole && user.role !== expectedRole) { window.location.href = base; return null; }
  return user;
}

function logout() {
  sessionStorage.removeItem(SESSION_KEY);
  const base = window.location.pathname.includes('/pages/') ? '../index.html' : 'index.html';
  window.location.href = base;
}
