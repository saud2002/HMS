/* ============================================
   HMS Dashboard - Data Management
   js/data.js
   Uses localStorage for data persistence across pages
   ============================================ */

// Initialize data from localStorage or use defaults
const HMS = {
    // Get data from localStorage
    getData: function(key) {
        const data = localStorage.getItem('hms_' + key);
        return data ? JSON.parse(data) : null;
    },

    // Save data to localStorage
    saveData: function(key, data) {
        localStorage.setItem('hms_' + key, JSON.stringify(data));
    },

    // Initialize with sample data if empty
    init: function() {
        if (!this.getData('initialized')) {
            // Sample Doctors
            const doctors = [
                { id: 'DR001', name: 'Dr. John Smith', specialization: 'General Medicine', fee: 100, status: 'Active' },
                { id: 'DR002', name: 'Dr. Sarah Wilson', specialization: 'Pediatrics', fee: 120, status: 'Active' },
                { id: 'DR003', name: 'Dr. Michael Brown', specialization: 'Cardiology', fee: 150, status: 'Active' }
            ];
            
            // Sample Patients
            const patients = [
                { id: 'PAT001', name: 'Alice Johnson', age: 35, gender: 'Female', phone: '0771234567', nic: '901234567V', regDate: '2024-01-15' },
                { id: 'PAT002', name: 'Bob Williams', age: 45, gender: 'Male', phone: '0779876543', nic: '791234567V', regDate: '2024-01-16' }
            ];
            
            this.saveData('doctors', doctors);
            this.saveData('patients', patients);
            this.saveData('appointments', []);
            this.saveData('activities', [{ text: 'System initialized with sample data', time: new Date().toISOString() }]);
            this.saveData('tokenCounters', {});
            this.saveData('initialized', true);
        }
    },

    // Patients CRUD
    patients: {
        getAll: function() {
            return HMS.getData('patients') || [];
        },
        getById: function(id) {
            return this.getAll().find(p => p.id === id);
        },
        add: function(patient) {
            const patients = this.getAll();
            patient.id = 'PAT' + String(patients.length + 1).padStart(3, '0');
            patient.regDate = new Date().toISOString().split('T')[0];
            patients.push(patient);
            HMS.saveData('patients', patients);
            HMS.activities.add('New patient registered: ' + patient.name);
            return patient;
        },
        update: function(id, data) {
            const patients = this.getAll();
            const idx = patients.findIndex(p => p.id === id);
            if (idx !== -1) {
                patients[idx] = { ...patients[idx], ...data };
                HMS.saveData('patients', patients);
                HMS.activities.add('Patient updated: ' + data.name);
                return patients[idx];
            }
            return null;
        },
        delete: function(id) {
            let patients = this.getAll();
            const patient = patients.find(p => p.id === id);
            patients = patients.filter(p => p.id !== id);
            HMS.saveData('patients', patients);
            if (patient) HMS.activities.add('Patient deleted: ' + patient.name);
        },
        exists: function(nic, excludeId = null) {
            return this.getAll().some(p => p.nic === nic && p.id !== excludeId);
        }
    },

    // Doctors CRUD
    doctors: {
        getAll: function() {
            return HMS.getData('doctors') || [];
        },
        getActive: function() {
            return this.getAll().filter(d => d.status === 'Active');
        },
        getById: function(id) {
            return this.getAll().find(d => d.id === id);
        },
        add: function(doctor) {
            const doctors = this.getAll();
            doctors.push(doctor);
            HMS.saveData('doctors', doctors);
            HMS.activities.add('New doctor added: ' + doctor.name);
            return doctor;
        },
        update: function(id, data) {
            const doctors = this.getAll();
            const idx = doctors.findIndex(d => d.id === id);
            if (idx !== -1) {
                doctors[idx] = { ...doctors[idx], ...data };
                HMS.saveData('doctors', doctors);
                HMS.activities.add('Doctor profile updated: ' + data.name);
                return doctors[idx];
            }
            return null;
        },
        toggleStatus: function(id) {
            const doctors = this.getAll();
            const doctor = doctors.find(d => d.id === id);
            if (doctor) {
                doctor.status = doctor.status === 'Active' ? 'Inactive' : 'Active';
                HMS.saveData('doctors', doctors);
                HMS.activities.add('Doctor ' + doctor.name + ' status changed to ' + doctor.status);
            }
        },
        exists: function(id) {
            return this.getAll().some(d => d.id === id);
        }
    },

    // Appointments
    appointments: {
        getAll: function() {
            return HMS.getData('appointments') || [];
        },
        getToday: function() {
            const today = new Date().toISOString().split('T')[0];
            return this.getAll().filter(a => a.date === today);
        },
        getByDate: function(date) {
            return this.getAll().filter(a => a.date === date);
        },
        getByDoctor: function(doctorId, date = null) {
            let appts = this.getAll().filter(a => a.doctorId === doctorId);
            if (date) appts = appts.filter(a => a.date === date);
            return appts;
        },
        add: function(appointment) {
            const appointments = this.getAll();
            appointment.token = this.generateToken(appointment.doctorId);
            appointments.push(appointment);
            HMS.saveData('appointments', appointments);
            HMS.activities.add('Appointment created: ' + appointment.patientName + ' with ' + appointment.doctorName + ' - Token: ' + appointment.token);
            return appointment;
        },
        generateToken: function(doctorId) {
            const counters = HMS.getData('tokenCounters') || {};
            const today = new Date().toISOString().split('T')[0].replace(/-/g, '');
            const key = doctorId + '-' + today;
            counters[key] = (counters[key] || 0) + 1;
            HMS.saveData('tokenCounters', counters);
            return doctorId + '-' + today + '-' + String(counters[key]).padStart(3, '0');
        },
        getTodayRevenue: function() {
            return this.getToday().reduce((sum, a) => sum + a.total, 0);
        }
    },

    // Activities
    activities: {
        getAll: function() {
            return HMS.getData('activities') || [];
        },
        add: function(text) {
            const activities = this.getAll();
            activities.unshift({ text: text, time: new Date().toISOString() });
            if (activities.length > 20) activities.pop();
            HMS.saveData('activities', activities);
        }
    },

    // Stats
    getStats: function() {
        return {
            totalPatients: this.patients.getAll().length,
            activeDoctors: this.doctors.getActive().length,
            todayAppointments: this.appointments.getToday().length,
            todayRevenue: this.appointments.getTodayRevenue()
        };
    },

    // Clear all data (for testing)
    clearAll: function() {
        localStorage.removeItem('hms_doctors');
        localStorage.removeItem('hms_patients');
        localStorage.removeItem('hms_appointments');
        localStorage.removeItem('hms_activities');
        localStorage.removeItem('hms_tokenCounters');
        localStorage.removeItem('hms_initialized');
    }
};

// Initialize on load
HMS.init();