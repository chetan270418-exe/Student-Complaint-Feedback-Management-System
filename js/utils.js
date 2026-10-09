/**
 * SHARED UI UTILITIES - Student Complaint & Feedback Management System
 */

// ─── FORMAT HELPERS ───────────────────────────────────────────────────
function formatDate(isoString) {
  if (!isoString) return 'N/A';
  const d = new Date(isoString);
  return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}
function formatDateTime(isoString) {
  if (!isoString) return 'N/A';
  const d = new Date(isoString);
  return d.toLocaleString('en-IN', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
}
function timeAgo(isoString) {
  const diff = Date.now() - new Date(isoString).getTime();
  const mins  = Math.floor(diff/60000);
  const hours = Math.floor(diff/3600000);
  const days  = Math.floor(diff/86400000);
  if (mins < 1)  return 'just now';
  if (mins < 60) return `${mins}m ago`;
  if (hours < 24)return `${hours}h ago`;
  return `${days}d ago`;
}

// ─── STATUS BADGE ─────────────────────────────────────────────────────
function statusBadge(status) {
  const map = {
    submitted:  ['badge-submitted',  '<i class="fas fa-paper-plane"></i> Submitted'],
    assigned:   ['badge-assigned',   '<i class="fas fa-user-check"></i> Assigned'],
    inprogress: ['badge-inprogress', '<i class="fas fa-spinner"></i> In Progress'],
    resolved:   ['badge-resolved',   '<i class="fas fa-check-circle"></i> Resolved'],
    closed:     ['badge-closed',     '<i class="fas fa-lock"></i> Closed']
  };
  const [cls, label] = map[status] || ['badge-submitted', status];
  return `<span class="badge ${cls}">${label}</span>`;
}

// ─── PRIORITY BADGE ───────────────────────────────────────────────────
function priorityBadge(priority) {
  const map = { high: 'badge-high', medium: 'badge-medium', low: 'badge-low' };
  const icon = { high: 'fa-fire', medium: 'fa-minus', low: 'fa-arrow-down' };
  return `<span class="badge ${map[priority]||''}"><i class="fas ${icon[priority]||'fa-circle'}"></i> ${capitalize(priority)}</span>`;
}

// ─── CATEGORY PILL ────────────────────────────────────────────────────
function categoryPill(category) {
  const map = {
    hostel: ['cat-hostel',  'fa-building',   'Hostel'],
    mess:   ['cat-mess',    'fa-utensils',   'Mess'],
    lab:    ['cat-lab',     'fa-flask',      'Lab'],
    faculty:['cat-faculty', 'fa-chalkboard-teacher','Faculty'],
    library:['cat-library', 'fa-book',       'Library'],
    other:  ['cat-other',   'fa-ellipsis-h', 'Other']
  };
  const [cls, icon, label] = map[category] || ['cat-other','fa-circle','Other'];
  return `<span class="category-pill ${cls}"><i class="fas ${icon}"></i> ${label}</span>`;
}

// ─── STARS ────────────────────────────────────────────────────────────
function starsHtml(rating) {
  return Array.from({length:5}, (_,i) => `<i class="fas fa-star" style="color:${i < rating ? '#ffd166' : '#cbd5e1'}; font-size:14px;"></i>`).join('');
}

// ─── MISC ─────────────────────────────────────────────────────────────
function capitalize(str) { return str ? str.charAt(0).toUpperCase() + str.slice(1) : ''; }

function showToast(message, type = 'success') {
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<i class="fas ${type==='success'?'fa-check-circle':'fa-exclamation-circle'}"></i> ${message}`;
  toast.style.cssText = `
    position:fixed; bottom:24px; right:24px; z-index:9999;
    background:${type==='success'?'#06d6a0':'#ef233c'}; color:white;
    padding:12px 20px; border-radius:12px; font-size:13px; font-weight:600;
    display:flex; align-items:center; gap:8px;
    box-shadow:0 8px 24px rgba(0,0,0,0.2); animation:slideInRight 0.3s ease;
  `;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

// ─── SIDEBAR NAV HIGHLIGHT ────────────────────────────────────────────
function setActiveNav(pageId) {
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.dataset.page === pageId);
  });
}

// ─── NOTIFICATION BADGE ───────────────────────────────────────────────
function updateNotifBadge(userId) {
  const count = getUserNotifications(userId).filter(n => !n.read).length;
  const badge = document.getElementById('notifCount');
  if (badge) {
    badge.textContent = count;
    badge.style.display = count > 0 ? 'flex' : 'none';
  }
  const dot = document.querySelector('.notif-dot');
  if (dot) dot.style.display = count > 0 ? 'block' : 'none';
}

// ─── RENDER SIDEBAR NOTIFICATIONS ────────────────────────────────────
function renderNotifPanel(userId) {
  const notifs = getUserNotifications(userId).slice(0, 8);
  const container = document.getElementById('notifList');
  if (!container) return;
  if (notifs.length === 0) {
    container.innerHTML = '<div class="empty-state" style="padding:24px;"><i class="fas fa-bell-slash" style="font-size:32px;"></i><p style="margin-top:8px;">No notifications</p></div>';
    return;
  }
  container.innerHTML = notifs.map(n => `
    <div class="notif-item ${!n.read ? 'unread' : ''}">
      <div class="notif-title">${n.title}</div>
      <div class="notif-time">${n.message}</div>
      <div class="notif-time" style="margin-top:4px; color:#94a3b8;">${timeAgo(n.date)}</div>
    </div>
  `).join('');
}
