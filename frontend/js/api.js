// js/api.js - API Service for HMS Frontend
// Use relative URLs so frontend works on same server as backend
const API_BASE_URL = '/api';

// Generic fetch wrapper
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: { 'Content-Type': 'application/json', ...options.headers },
        ...options
    };
    
    const token = localStorage.getItem('access_token');
    if (token) config.headers['Authorization'] = `Bearer ${token}`;
    
    const response = await fetch(url, config);
    
    if (!response.ok) {
        let errorData;
        try {
            errorData = await response.json();
        } catch (parseError) {
            errorData = { detail: `HTTP ${response.status}: ${response.statusText}` };
        }
        
        const errorMessage = errorData.detail || errorData.message || `HTTP ${response.status}`;
        throw new Error(errorMessage);
    }
    
    return response.json();
}

// ==================== DASHBOARD ====================
const Dashboard = {
    getStats: () => apiRequest('/dashboard/stats')
};

// ==================== PATIENTS ====================
const Patients = {
    getAll: (search = '') => apiRequest(`/patients${search ? `?search=${encodeURIComponent(search)}` : ''}`),
    getById: (id) => apiRequest(`/patients/${id}`),
    getByNIC: (nic) => apiRequest(`/patients/nic/${nic}`),
    create: (data) => apiRequest('/patients', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => apiRequest(`/patients/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id) => apiRequest(`/patients/${id}`, { method: 'DELETE' })
};

// ==================== DOCTORS ====================
const Doctors = {
    getAll: (status = 'Active') => apiRequest(`/doctors?status=${status}`),
    getById: (id) => apiRequest(`/doctors/${id}`),
    getSpecializations: () => apiRequest('/doctors/specializations'),
    create: (data) => apiRequest('/doctors', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => apiRequest(`/doctors/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deactivate: (id) => apiRequest(`/doctors/${id}`, { method: 'DELETE' }),
    delete: (id) => apiRequest(`/doctors/${id}/delete`, { method: 'DELETE' })
};

// ==================== APPOINTMENTS ====================
const Appointments = {
    getAll: (params = {}) => {
        const query = new URLSearchParams(params).toString();
        return apiRequest(`/appointments${query ? '?' + query : ''}`);
    },
    getById: (id) => apiRequest(`/appointments/${id}`),
    getToday: () => apiRequest('/appointments/today'),
    getDoctorToday: (doctorId) => apiRequest(`/appointments/doctor/${doctorId}/today`),
    create: (data) => apiRequest('/appointments', { method: 'POST', body: JSON.stringify(data) }),
    updateStatus: (id, status) => apiRequest(`/appointments/${id}/status?status=${status}`, { method: 'PATCH' }),
    cancel: (id) => apiRequest(`/appointments/${id}`, { method: 'DELETE' })
};

// ==================== ADDITIONAL EXPENSES ====================
const Expenses = {
    getByAppointment: (appointmentId) => apiRequest(`/expenses/appointment/${appointmentId}`),
    add: (data) => apiRequest('/expenses', { method: 'POST', body: JSON.stringify(data) }),
    delete: (id) => apiRequest(`/expenses/${id}`, { method: 'DELETE' })
};

// ==================== BILLS ====================
const Bills = {
    getAll: (params = {}) => {
        const query = new URLSearchParams(params).toString();
        return apiRequest(`/bills${query ? '?' + query : ''}`);
    },
    getById: (id) => apiRequest(`/bills/${id}`),
    getByAppointment: (appointmentId) => apiRequest(`/bills/appointment/${appointmentId}`),
    updatePaymentStatus: (id, status) => {
        return apiRequest(`/bills/${id}/payment-status`, { 
            method: 'PATCH',
            body: JSON.stringify({ payment_status: status })
        });
    }
};

// ==================== REPORTS ====================
const Reports = {
    getSummary: (startDate, endDate) => {
        const params = new URLSearchParams();
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        return apiRequest(`/reports/summary?${params}`);
    },
    getDaily: (date) => apiRequest(`/reports/daily${date ? '?report_date=' + date : ''}`),
    getDoctorWise: (startDate, endDate) => {
        const params = new URLSearchParams();
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        return apiRequest(`/reports/doctor-wise?${params}`);
    },
    getServiceWise: (startDate, endDate) => {
        const params = new URLSearchParams();
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        return apiRequest(`/reports/service-wise?${params}`);
    },
    getAppointmentsByDate: (startDate, endDate) => {
        const params = new URLSearchParams();
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        return apiRequest(`/reports/appointments-by-date?${params}`);
    }
};

// ==================== AUTH ====================
const Auth = {
    login: async (username, password) => {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        if (!response.ok) throw new Error('Invalid credentials');
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        return data;
    },
    register: (data) => apiRequest('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
    logout: () => localStorage.removeItem('access_token'),
    isAuthenticated: () => !!localStorage.getItem('access_token')
};

// ==================== UTILITIES ====================
function showToast(message, type = 'success') {
    const colors = { success: '#10b981', error: '#ef4444', info: '#3b82f6', warning: '#f59e0b' };
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.cssText = `position:fixed;top:20px;right:20px;padding:15px 25px;border-radius:8px;
        color:white;z-index:9999;background:${colors[type] || colors.info};box-shadow:0 4px 12px rgba(0,0,0,0.15)`;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

function formatCurrency(amount) {
    return `Rs. ${parseFloat(amount).toLocaleString('en-LK', { minimumFractionDigits: 2 })}`;
}

// Export
window.API = { Dashboard, Patients, Doctors, Appointments, Expenses, Bills, Reports, Auth };
window.showToast = showToast;
window.formatDate = formatDate;
window.formatCurrency = formatCurrency;