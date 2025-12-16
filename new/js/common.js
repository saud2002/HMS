/* ============================================
   HMS Dashboard - Common UI Components
   js/common.js
   ============================================ */

// SVG Icons
const ICONS = {
    dashboard: '<path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>',
    patients: '<path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>',
    doctors: '<path d="M19 3H5c-1.1 0-1.99.9-1.99 2L3 19c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z"/>',
    appointments: '<path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>',
    reports: '<path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4"/>',
    hospital: '<path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-1 11h-4v4h-4v-4H6v-4h4V6h4v4h4v4z"/>',
    addPatient: '<path d="M15 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm-9-2V7H4v3H1v2h3v3h2v-3h3v-2H6zm9 4c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>',
    money: '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1.41 16.09V20h-2.67v-1.93c-1.71-.36-3.16-1.46-3.27-3.4h1.96c.1 1.05.82 1.87 2.65 1.87 1.96 0 2.4-.98 2.4-1.59 0-.83-.44-1.61-2.67-2.14-2.48-.6-4.18-1.62-4.18-3.67 0-1.72 1.39-2.84 3.11-3.21V4h2.67v1.95c1.86.45 2.79 1.86 2.85 3.39H14.3c-.05-1.11-.64-1.87-2.22-1.87-1.5 0-2.4.68-2.4 1.64 0 .84.65 1.39 2.67 1.91s4.18 1.39 4.18 3.91c-.01 1.83-1.38 2.83-3.12 3.16z"/>',
    check: '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>'
};

// Page titles
const PAGE_TITLES = {
    'index.html': 'Dashboard',
    'patients.html': 'Patient Management',
    'doctors.html': 'Doctor Management',
    'appointments.html': 'Appointments & Billing',
    'reports.html': 'Reports & Analytics'
};

// Get current page name
function getCurrentPage() {
    const path = window.location.pathname;
    const page = path.substring(path.lastIndexOf('/') + 1) || 'index.html';
    return page;
}

// Render Sidebar
function renderSidebar() {
    const currentPage = getCurrentPage();
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;
    
    sidebar.innerHTML = `
        <div class="logo-section">
            <div class="logo-icon">
                <svg viewBox="0 0 24 24">${ICONS.hospital}</svg>
            </div>
            <div class="logo-text">HMS Portal</div>
        </div>
        <div class="menu">
            <a class="menu-item ${currentPage === 'index.html' ? 'active' : ''}" href="index.html">
                <svg viewBox="0 0 24 24">${ICONS.dashboard}</svg>
                <span>Dashboard</span>
            </a>
            <a class="menu-item ${currentPage === 'patients.html' ? 'active' : ''}" href="patients.html">
                <svg viewBox="0 0 24 24">${ICONS.patients}</svg>
                <span>Patients</span>
            </a>
            <a class="menu-item ${currentPage === 'doctors.html' ? 'active' : ''}" href="doctors.html">
                <svg viewBox="0 0 24 24">${ICONS.doctors}</svg>
                <span>Doctors</span>
            </a>
            <a class="menu-item ${currentPage === 'appointments.html' ? 'active' : ''}" href="appointments.html">
                <svg viewBox="0 0 24 24">${ICONS.appointments}</svg>
                <span>Appointments</span>
            </a>
            <a class="menu-item ${currentPage === 'reports.html' ? 'active' : ''}" href="reports.html">
                <svg viewBox="0 0 24 24">${ICONS.reports}</svg>
                <span>Reports</span>
            </a>
        </div>
    `;
}

// Render Topbar
function renderTopbar() {
    const currentPage = getCurrentPage();
    const topbar = document.getElementById('topbar');
    if (!topbar) return;
    
    topbar.innerHTML = `
        <div class="topbar-left">
            <button class="toggle-btn" id="toggleSidebar">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="2">
                    <line x1="3" y1="12" x2="21" y2="12"></line>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
            </button>
            <h1 class="page-title">${PAGE_TITLES[currentPage] || 'Dashboard'}</h1>
        </div>
        <div class="topbar-right">
            <div class="date-time" id="dateTime"></div>
            <div class="user-profile">
                <div class="user-avatar">A</div>
                <div class="user-info">
                    <div class="user-name">Admin User</div>
                    <div class="user-role">System Administrator</div>
                </div>
            </div>
        </div>
    `;
    
    // Toggle sidebar
    document.getElementById('toggleSidebar').addEventListener('click', function() {
        document.getElementById('sidebar').classList.toggle('collapsed');
    });
    
    // Update date/time
    updateDateTime();
    setInterval(updateDateTime, 60000);
}

// Update DateTime display
function updateDateTime() {
    const el = document.getElementById('dateTime');
    if (el) {
        el.textContent = new Date().toLocaleDateString('en-US', {
            weekday: 'short', year: 'numeric', month: 'short',
            day: 'numeric', hour: '2-digit', minute: '2-digit'
        });
    }
}

// Get time ago string
function getTimeAgo(dateString) {
    const date = new Date(dateString);
    const seconds = Math.floor((new Date() - date) / 1000);
    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return Math.floor(seconds / 60) + ' minutes ago';
    if (seconds < 86400) return Math.floor(seconds / 3600) + ' hours ago';
    return Math.floor(seconds / 86400) + ' days ago';
}

// Initialize common components
function initCommon() {
    renderSidebar();
    renderTopbar();
}

// Modal helpers
function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Generate Bill HTML
function generateBillHTML(appt) {
    const additionalList = appt.additionalServices.map(s => 
        `<div class="bill-row"><span>${s.name}</span><span>$${s.amount}</span></div>`
    ).join('');
    
    return `
        <div class="bill-section">
            <div class="bill-header">
                <h2 style="color:#1e40af;">🏥 HMS Medical Center</h2>
                <p style="color:#64748b;">Invoice / Receipt</p>
            </div>
            <div class="token-display">
                <div style="font-size:14px;">Token Number</div>
                <div class="token-number">${appt.token}</div>
            </div>
            <div style="margin: 15px 0; padding: 15px; background: #f8fafc; border-radius: 8px;">
                <strong>Patient:</strong> ${appt.patientName} (Age: ${appt.patientAge})<br>
                <strong>NIC:</strong> ${appt.patientNIC} | <strong>Phone:</strong> ${appt.patientPhone}<br>
                <strong>Doctor:</strong> ${appt.doctorName} (${appt.doctorSpecialization})<br>
                <strong>Date:</strong> ${appt.date} | <strong>Time:</strong> ${appt.time}
            </div>
            <h4 style="margin: 15px 0 10px;">Charges Breakdown</h4>
            <div class="bill-row"><span>Doctor Consultation Fee</span><span>$${appt.doctorFee}</span></div>
            <div class="bill-row"><span>Hospital Charges</span><span>$${appt.hospitalCharges}</span></div>
            ${additionalList}
            <div class="bill-row bill-total"><span>TOTAL AMOUNT</span><span>$${appt.total}</span></div>
        </div>
    `;
}

// Call initCommon when DOM is ready
document.addEventListener('DOMContentLoaded', initCommon);