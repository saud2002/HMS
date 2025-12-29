// Voucher Management JavaScript

let currentVouchers = [];
let doctors = [];

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Set default date to today
    document.getElementById('voucherDate').value = new Date().toISOString().split('T')[0];
    
    // Load initial data
    loadDoctors();
    loadVoucherSummary();
    loadVouchers();
});

// Load doctors for dropdown
async function loadDoctors() {
    try {
        const response = await fetch('/api/doctors');
        if (response.ok) {
            doctors = await response.json();
            
            // Populate doctor dropdowns
            const doctorSelects = ['doctorId', 'filterDoctor'];
            doctorSelects.forEach(selectId => {
                const select = document.getElementById(selectId);
                if (select) {
                    // Clear existing options (except first one for filter)
                    if (selectId === 'filterDoctor') {
                        select.innerHTML = '<option value="">All Doctors</option>';
                    } else {
                        select.innerHTML = '<option value="">Select Doctor</option>';
                    }
                    
                    // Add doctor options
                    doctors.forEach(doctor => {
                        const option = document.createElement('option');
                        option.value = doctor.doctor_id;
                        option.textContent = `${doctor.doctor_name} (${doctor.specialization})`;
                        select.appendChild(option);
                    });
                }
            });
        }
    } catch (error) {
        console.error('Error loading doctors:', error);
        showAlert('Error loading doctors', 'danger');
    }
}

// Load voucher summary
async function loadVoucherSummary() {
    try {
        const response = await fetch('/api/vouchers/summary');
        if (response.ok) {
            const summary = await response.json();
            
            document.getElementById('totalVouchers').textContent = summary.total_vouchers;
            document.getElementById('pendingApproval').textContent = summary.pending_approval_count;
            document.getElementById('approvedCount').textContent = summary.approved_count;
            document.getElementById('totalAmount').textContent = `LKR ${parseFloat(summary.total_amount).toLocaleString()}`;
        }
    } catch (error) {
        console.error('Error loading voucher summary:', error);
    }
}

// Load vouchers with filters
async function loadVouchers() {
    try {
        const filters = new URLSearchParams();
        
        const type = document.getElementById('filterType').value;
        const status = document.getElementById('filterStatus').value;
        const doctorId = document.getElementById('filterDoctor').value;
        const dateFrom = document.getElementById('filterDateFrom').value;
        
        if (type) filters.append('voucher_type', type);
        if (status) filters.append('status', status);
        if (doctorId) filters.append('doctor_id', doctorId);
        if (dateFrom) filters.append('date_from', dateFrom);
        
        const response = await fetch(`/api/vouchers?${filters.toString()}`);
        if (response.ok) {
            currentVouchers = await response.json();
            displayVouchers(currentVouchers);
        } else {
            throw new Error('Failed to load vouchers');
        }
    } catch (error) {
        console.error('Error loading vouchers:', error);
        document.getElementById('vouchersTableBody').innerHTML = 
            '<tr><td colspan="7" class="text-center text-danger">Error loading vouchers</td></tr>';
    }
}

// Display vouchers in table
function displayVouchers(vouchers) {
    const tbody = document.getElementById('vouchersTableBody');
    
    if (vouchers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No vouchers found</td></tr>';
        return;
    }
    
    tbody.innerHTML = vouchers.map(voucher => `
        <tr>
            <td>${voucher.voucher_number}</td>
            <td>${formatVoucherType(voucher.voucher_type)}</td>
            <td>${voucher.doctor_name || 'N/A'}</td>
            <td>LKR ${parseFloat(voucher.amount).toLocaleString()}</td>
            <td>${formatDate(voucher.voucher_date)}</td>
            <td><span class="badge ${getVoucherTypeClass(voucher.status)}">${formatStatus(voucher.status)}</span></td>
            <td>
                <div class="btn-group">
                    <button class="btn btn-sm btn-primary" onclick="viewVoucher(${voucher.voucher_id})">View</button>
                    ${getActionButton(voucher)}
                </div>
            </td>
        </tr>
    `).join('');
}

// Format voucher type for display
function formatVoucherType(type) {
    switch (type) {
        case 'DOCTOR_PAYMENT': return 'Doctor Payment';
        case 'HOSPITAL_EXPENSE': return 'Hospital Expense';
        case 'ADJUSTMENT': return 'Adjustment';
        default: return type;
    }
}

// Format status for display
function formatStatus(status) {
    switch (status) {
        case 'DRAFT': return 'Draft';
        case 'PENDING_APPROVAL': return 'Pending Approval';
        case 'APPROVED': return 'Approved';
        case 'PAID': return 'Paid';
        case 'REJECTED': return 'Rejected';
        default: return status;
    }
}

// Get CSS class for voucher status
function getVoucherTypeClass(status) {
    switch (status) {
        case 'DRAFT': return 'bg-secondary';
        case 'PENDING_APPROVAL': return 'bg-warning';
        case 'APPROVED': return 'bg-success';
        case 'PAID': return 'bg-info';
        case 'REJECTED': return 'bg-danger';
        default: return 'bg-secondary';
    }
}

// Get action button based on voucher status
function getActionButton(voucher) {
    switch (voucher.status) {
        case 'DRAFT':
            return `<button class="btn btn-sm btn-warning" onclick="submitForApproval(${voucher.voucher_id})">Submit</button>`;
        case 'PENDING_APPROVAL':
            return `
                <button class="btn btn-sm btn-success" onclick="approveVoucher(${voucher.voucher_id})">Approve</button>
                <button class="btn btn-sm btn-danger" onclick="rejectVoucher(${voucher.voucher_id})">Reject</button>
            `;
        case 'APPROVED':
            return `<button class="btn btn-sm btn-info" onclick="markAsPaid(${voucher.voucher_id})">Mark Paid</button>`;
        default:
            return '';
    }
}

// Show create voucher modal
function showCreateVoucherModal(type) {
    document.getElementById('voucherType').value = type;
    document.getElementById('createVoucherModalTitle').textContent = `Create ${formatVoucherType(type)}`;
    
    // Show/hide relevant sections
    const doctorSection = document.getElementById('doctorSection');
    const paymentPeriodSection = document.getElementById('paymentPeriodSection');
    
    if (type === 'DOCTOR_PAYMENT') {
        doctorSection.style.display = 'block';
        paymentPeriodSection.style.display = 'block';
        document.getElementById('doctorId').required = true;
    } else {
        doctorSection.style.display = 'none';
        paymentPeriodSection.style.display = 'none';
        document.getElementById('doctorId').required = false;
    }
    
    // Reset form
    document.getElementById('createVoucherForm').reset();
    document.getElementById('voucherDate').value = new Date().toISOString().split('T')[0];
    
    openModal('createVoucherModal');
}

// Create voucher
async function createVoucher() {
    try {
        const form = document.getElementById('createVoucherForm');
        const formData = new FormData(form);
        
        const voucherData = {
            voucher_type: formData.get('voucher_type'),
            amount: parseFloat(formData.get('amount')),
            voucher_date: formData.get('voucher_date'),
            description: formData.get('description') || null
        };
        
        // Add doctor-specific fields if applicable
        if (voucherData.voucher_type === 'DOCTOR_PAYMENT') {
            voucherData.doctor_id = formData.get('doctor_id') || null;
            voucherData.payment_period_start = formData.get('payment_period_start') || null;
            voucherData.payment_period_end = formData.get('payment_period_end') || null;
        }
        
        const response = await fetch('/api/vouchers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(voucherData)
        });
        
        if (response.ok) {
            const result = await response.json();
            showAlert(`Voucher ${result.voucher_number} created successfully`, 'success');
            closeModal('createVoucherModal');
            loadVouchers();
            loadVoucherSummary();
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create voucher');
        }
    } catch (error) {
        console.error('Error creating voucher:', error);
        showAlert(error.message, 'danger');
    }
}

// View voucher details
async function viewVoucher(voucherId) {
    try {
        const response = await fetch(`/api/vouchers/${voucherId}`);
        if (response.ok) {
            const voucher = await response.json();
            displayVoucherDetails(voucher);
            openModal('viewVoucherModal');
        } else {
            throw new Error('Failed to load voucher details');
        }
    } catch (error) {
        console.error('Error loading voucher details:', error);
        showAlert('Error loading voucher details', 'danger');
    }
}

// Display voucher details in modal
function displayVoucherDetails(voucher) {
    const content = document.getElementById('voucherDetailsContent');
    content.innerHTML = `
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 20px;">
            <div>
                <h4 style="color: #1e40af; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">Voucher Information</h4>
                <div style="background: #f8fafc; padding: 15px; border-radius: 8px;">
                    <div style="margin-bottom: 10px;"><strong>Voucher Number:</strong> <span style="color: #2563eb;">${voucher.voucher_number}</span></div>
                    <div style="margin-bottom: 10px;"><strong>Type:</strong> ${formatVoucherType(voucher.voucher_type)}</div>
                    <div style="margin-bottom: 10px;"><strong>Status:</strong> <span class="badge ${getVoucherTypeClass(voucher.status)}">${formatStatus(voucher.status)}</span></div>
                    <div style="margin-bottom: 10px;"><strong>Amount:</strong> <span style="color: #059669; font-weight: 600;">LKR ${parseFloat(voucher.amount).toLocaleString()}</span></div>
                    <div><strong>Date:</strong> ${formatDate(voucher.voucher_date)}</div>
                </div>
            </div>
            <div>
                <h4 style="color: #1e40af; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">Additional Details</h4>
                <div style="background: #f8fafc; padding: 15px; border-radius: 8px;">
                    ${voucher.doctor_name ? `<div style="margin-bottom: 10px;"><strong>Doctor:</strong> ${voucher.doctor_name}</div>` : ''}
                    ${voucher.payment_period_start ? `<div style="margin-bottom: 10px;"><strong>Period Start:</strong> ${formatDate(voucher.payment_period_start)}</div>` : ''}
                    ${voucher.payment_period_end ? `<div style="margin-bottom: 10px;"><strong>Period End:</strong> ${formatDate(voucher.payment_period_end)}</div>` : ''}
                    <div style="margin-bottom: 10px;"><strong>Created:</strong> ${formatDateTime(voucher.created_at)}</div>
                    ${voucher.approved_at ? `<div style="margin-bottom: 10px;"><strong>Approved:</strong> ${formatDateTime(voucher.approved_at)}</div>` : ''}
                    ${voucher.paid_at ? `<div><strong>Paid:</strong> ${formatDateTime(voucher.paid_at)}</div>` : ''}
                </div>
            </div>
        </div>
        ${voucher.description ? `
            <div>
                <h4 style="color: #1e40af; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">Description</h4>
                <div style="background: #f8fafc; padding: 15px; border-radius: 8px; border-left: 4px solid #2563eb;">
                    ${voucher.description}
                </div>
            </div>
        ` : ''}
    `;
}

// Submit voucher for approval
async function submitForApproval(voucherId) {
    if (!confirm('Are you sure you want to submit this voucher for approval?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/vouchers/${voucherId}/submit`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const result = await response.json();
            showAlert(result.message, 'success');
            loadVouchers();
            loadVoucherSummary();
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to submit voucher');
        }
    } catch (error) {
        console.error('Error submitting voucher:', error);
        showAlert(error.message, 'danger');
    }
}

// Approve voucher
async function approveVoucher(voucherId) {
    if (!confirm('Are you sure you want to approve this voucher?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/vouchers/${voucherId}/approve`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const result = await response.json();
            showAlert(result.message, 'success');
            loadVouchers();
            loadVoucherSummary();
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to approve voucher');
        }
    } catch (error) {
        console.error('Error approving voucher:', error);
        showAlert(error.message, 'danger');
    }
}

// Reject voucher
async function rejectVoucher(voucherId) {
    if (!confirm('Are you sure you want to reject this voucher?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/vouchers/${voucherId}/reject`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const result = await response.json();
            showAlert(result.message, 'success');
            loadVouchers();
            loadVoucherSummary();
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to reject voucher');
        }
    } catch (error) {
        console.error('Error rejecting voucher:', error);
        showAlert(error.message, 'danger');
    }
}

// Mark voucher as paid
async function markAsPaid(voucherId) {
    if (!confirm('Are you sure you want to mark this voucher as paid?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/vouchers/${voucherId}/pay`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const result = await response.json();
            showAlert(result.message, 'success');
            loadVouchers();
            loadVoucherSummary();
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to mark voucher as paid');
        }
    } catch (error) {
        console.error('Error marking voucher as paid:', error);
        showAlert(error.message, 'danger');
    }
}

// Utility functions
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
}

function formatDateTime(dateTimeString) {
    if (!dateTimeString) return 'N/A';
    return new Date(dateTimeString).toLocaleString();
}

function showAlert(message, type) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        max-width: 400px;
        animation: slideIn 0.3s ease-out;
    `;
    
    // Set colors based on type
    if (type === 'success') {
        alertDiv.style.background = 'linear-gradient(135deg, #10b981, #059669)';
        alertDiv.style.color = 'white';
    } else if (type === 'danger') {
        alertDiv.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
        alertDiv.style.color = 'white';
    } else if (type === 'warning') {
        alertDiv.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
        alertDiv.style.color = 'white';
    } else {
        alertDiv.style.background = 'linear-gradient(135deg, #06b6d4, #0891b2)';
        alertDiv.style.color = 'white';
    }
    
    alertDiv.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: inherit; font-size: 18px; cursor: pointer; margin-left: 10px;">&times;</button>
        </div>
    `;
    
    // Add CSS animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    // Insert into body
    document.body.appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.style.animation = 'slideIn 0.3s ease-out reverse';
            setTimeout(() => alertDiv.remove(), 300);
        }
    }, 5000);
}