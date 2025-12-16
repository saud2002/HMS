// js/api.js - API Service for connecting frontend to FastAPI backend

const API_BASE_URL = 'http://localhost:8000/api';

// Generic fetch wrapper with error handling
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: { 'Content-Type': 'application/json', ...options.headers },
        ...options
    };
    
    // Add auth token if available
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(url, config);
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
            throw new Error(error.detail || `HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`API Error [${endpoint}]:`, error);
        throw error;
    }
}

// ==================== DASHBOARD ====================
const DashboardAPI = {
    getStats: () => apiRequest('/dashboard/stats'),
    healthCheck: () => apiRequest('/health')
};

// ==================== PATIENTS ====================
const PatientsAPI = {
    getAll: (params = {}) => {
        const query = new URLSearchParams(params).toString();
        return apiRequest(`/patients/${query ? '?' + query : ''}`);
    },
    getById: (id) => apiRequest(`/patients/${id}`),
    create: (data) => apiRequest('/patients/', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => apiRequest(`/patients/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id) => apiRequest(`/patients/${id}`, { method: 'DELETE' }),
    search: (query) => apiRequest(`/patients/?search=${encodeURIComponent(query)}`)
};

// ==================== DOCTORS ====================
const DoctorsAPI = {
    getAll: (params = {}) => {
        const query = new URLSearchParams(params).toString();
        return apiRequest(`/doctors/${query ? '?' + query : ''}`);
    },
    getById: (id) => apiRequest(`/doctors/${id}`),
    create: (data) => apiRequest('/doctors/', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => apiRequest(`/doctors/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id) => apiRequest(`/doctors/${id}`, { method: 'DELETE' }),
    getSpecializations: () => apiRequest('/doctors/specializations')
};

// ==================== APPOINTMENTS ====================
const AppointmentsAPI = {
    getAll: (params = {}) => {
        const query = new URLSearchParams(params).toString();
        return apiRequest(`/appointments/${query ? '?' + query : ''}`);
    },
    getById: (id) => apiRequest(`/appointments/${id}`),
    getToday: () => apiRequest('/appointments/today'),
    create: (data) => apiRequest('/appointments/', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => apiRequest(`/appointments/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    updateStatus: (id, status) => apiRequest(`/appointments/${id}/status?status=${status}`, { method: 'PATCH' }),
    delete: (id) => apiRequest(`/appointments/${id}`, { method: 'DELETE' })
};

// ==================== REPORTS ====================
const ReportsAPI = {
    getSummary: (startDate, endDate) => {
        const params = new URLSearchParams();
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        return apiRequest(`/reports/summary?${params}`);
    },
    getByDoctor: (startDate, endDate) => {
        const params = new URLSearchParams();
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        return apiRequest(`/reports/appointments-by-doctor?${params}`);
    },
    getByDate: (startDate, endDate) => {
        const params = new URLSearchParams();
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        return apiRequest(`/reports/appointments-by-date?${params}`);
    }
};

// ==================== AUTH ====================
const AuthAPI = {
    login: async (username, password) => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
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

// ==================== UTILITY FUNCTIONS ====================
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `position:fixed;top:20px;right:20px;padding:15px 25px;border-radius:8px;color:white;z-index:9999;
        background:${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'}`;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

function formatTime(timeStr) {
    const [h, m] = timeStr.split(':');
    const hour = parseInt(h);
    return `${hour > 12 ? hour - 12 : hour}:${m} ${hour >= 12 ? 'PM' : 'AM'}`;
}

// Export for use in other files
window.API = { Dashboard: DashboardAPI, Patients: PatientsAPI, Doctors: DoctorsAPI, 
               Appointments: AppointmentsAPI, Reports: ReportsAPI, Auth: AuthAPI };
window.showToast = showToast;
window.formatDate = formatDate;
window.formatTime = formatTime;