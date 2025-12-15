-- ================================================
-- HOSPITAL MANAGEMENT SYSTEM - DATABASE SCHEMA
-- ================================================
-- Database: hospital_management_system
-- Version: 1.0
-- Date: December 10, 2025
-- ================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS hospital_management_system;
USE hospital_management_system;

-- ================================================
-- TABLE 1: ADMIN TABLE
-- Purpose: Store admin login credentials
-- ================================================
CREATE TABLE admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- ================================================
-- TABLE 2: PATIENTS TABLE
-- Purpose: Store patient registration information
-- ================================================
CREATE TABLE patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    phone_no VARCHAR(15) NOT NULL,
    nic VARCHAR(20) NOT NULL UNIQUE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    registered_by INT,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (registered_by) REFERENCES admin(admin_id),
    INDEX idx_nic (nic),
    INDEX idx_phone (phone_no),
    INDEX idx_name (patient_name)
);

-- ================================================
-- TABLE 3: DOCTORS TABLE
-- Purpose: Store doctor information and specializations
-- ================================================
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_code VARCHAR(20) NOT NULL UNIQUE,
    doctor_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    consultation_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    phone_no VARCHAR(15),
    email VARCHAR(100),
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    added_by INT,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (added_by) REFERENCES admin(admin_id),
    INDEX idx_doctor_code (doctor_code),
    INDEX idx_specialization (specialization)
);

-- ================================================
-- TABLE 4: APPOINTMENTS TABLE
-- Purpose: Store appointment details and token numbers
-- ================================================
CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    token_number VARCHAR(20) NOT NULL,
    
    -- Charges breakdown
    doctor_consultation_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    hospital_charges DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    
    -- Status
    status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (created_by) REFERENCES admin(admin_id),
    
    INDEX idx_appointment_date (appointment_date),
    INDEX idx_token (token_number),
    INDEX idx_patient (patient_id),
    INDEX idx_doctor (doctor_id),
    INDEX idx_status (status)
);

-- ================================================
-- TABLE 5: ADDITIONAL EXPENSES TABLE
-- Purpose: Store additional medical expenses for appointments
-- ================================================
CREATE TABLE additional_expenses (
    expense_id INT PRIMARY KEY AUTO_INCREMENT,
    appointment_id INT NOT NULL,
    expense_type VARCHAR(50) NOT NULL,
    expense_description VARCHAR(200),
    amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE CASCADE,
    INDEX idx_appointment (appointment_id),
    INDEX idx_expense_type (expense_type)
);

-- ================================================
-- TABLE 6: BILLS TABLE
-- Purpose: Store billing information for appointments
-- ================================================
CREATE TABLE bills (
    bill_id INT PRIMARY KEY AUTO_INCREMENT,
    appointment_id INT NOT NULL UNIQUE,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    bill_date DATE NOT NULL,
    bill_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Charges summary
    doctor_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    hospital_charges DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    additional_expenses_total DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    
    -- Payment details
    payment_status ENUM('Pending', 'Paid', 'Partial') DEFAULT 'Paid',
    payment_method VARCHAR(50),
    
    generated_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (generated_by) REFERENCES admin(admin_id),
    
    INDEX idx_bill_date (bill_date),
    INDEX idx_payment_status (payment_status)
);

-- ================================================
-- TABLE 7: DAILY REPORTS TABLE
-- Purpose: Store generated daily reports for archiving
-- ================================================
CREATE TABLE daily_reports (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    report_date DATE NOT NULL,
    report_type ENUM('Doctor', 'Hospital') NOT NULL,
    doctor_id INT NULL,
    
    -- Summary data
    total_patients INT DEFAULT 0,
    total_revenue DECIMAL(12, 2) DEFAULT 0.00,
    doctor_fees_total DECIMAL(12, 2) DEFAULT 0.00,
    hospital_charges_total DECIMAL(12, 2) DEFAULT 0.00,
    expenses_total DECIMAL(12, 2) DEFAULT 0.00,
    
    generated_by INT,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (generated_by) REFERENCES admin(admin_id),
    
    INDEX idx_report_date (report_date),
    INDEX idx_report_type (report_type)
);

-- ================================================
-- TABLE 8: EXPENSE TYPES TABLE (Reference/Lookup)
-- Purpose: Maintain standard expense types for consistency
-- ================================================
CREATE TABLE expense_types (
    expense_type_id INT PRIMARY KEY AUTO_INCREMENT,
    expense_name VARCHAR(50) NOT NULL UNIQUE,
    default_charge DECIMAL(10, 2) DEFAULT 0.00,
    description VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ================================================
-- TABLE 9: AUDIT LOG TABLE
-- Purpose: Track all system activities for security
-- ================================================
CREATE TABLE audit_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    admin_id INT,
    action_type VARCHAR(50) NOT NULL,
    table_name VARCHAR(50),
    record_id INT,
    action_description TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id),
    INDEX idx_action_type (action_type),
    INDEX idx_created_at (created_at)
);

-- ================================================
-- INSERT DEFAULT DATA
-- ================================================

-- Insert default admin user (password should be hashed in production)
INSERT INTO admin (username, password, full_name, email) 
VALUES ('admin', 'admin123', 'System Administrator', 'admin@hospital.com');

-- Insert default expense types
INSERT INTO expense_types (expense_name, default_charge, description) VALUES
('Dressing', 500.00, 'Medical dressing and bandaging'),
('Scanning', 2500.00, 'CT/MRI/X-Ray scanning services'),
('Blood Testing', 1500.00, 'Laboratory blood tests'),
('ECG', 1000.00, 'Electrocardiogram test'),
('Ultrasound', 2000.00, 'Ultrasound scanning'),
('Injection', 300.00, 'Medication injection'),
('Nebulization', 400.00, 'Respiratory nebulization treatment'),
('Minor Surgery', 5000.00, 'Minor surgical procedures'),
('Consultation Report', 200.00, 'Printed consultation report'),
('Medicine', 0.00, 'Prescribed medicines');

-- ================================================
-- VIEWS FOR REPORTING
-- ================================================

-- View: Daily Appointments Summary
CREATE VIEW view_daily_appointments AS
SELECT 
    a.appointment_date,
    a.appointment_id,
    a.token_number,
    p.patient_name,
    p.age,
    p.gender,
    p.phone_no,
    d.doctor_name,
    d.specialization,
    a.doctor_consultation_fee,
    a.hospital_charges,
    COALESCE(SUM(ae.amount), 0) AS additional_expenses,
    (a.doctor_consultation_fee + a.hospital_charges + COALESCE(SUM(ae.amount), 0)) AS total_amount,
    a.status
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id
LEFT JOIN additional_expenses ae ON a.appointment_id = ae.appointment_id
GROUP BY a.appointment_id;

-- View: Doctor Performance Report
CREATE VIEW view_doctor_performance AS
SELECT 
    d.doctor_id,
    d.doctor_name,
    d.specialization,
    DATE(a.appointment_date) AS report_date,
    COUNT(DISTINCT a.appointment_id) AS total_patients,
    SUM(a.doctor_consultation_fee) AS total_consultation_fees,
    AVG(a.doctor_consultation_fee) AS avg_consultation_fee
FROM doctors d
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
WHERE a.status != 'Cancelled'
GROUP BY d.doctor_id, DATE(a.appointment_date);

-- View: Hospital Revenue Report
CREATE VIEW view_hospital_revenue AS
SELECT 
    DATE(a.appointment_date) AS report_date,
    COUNT(DISTINCT a.appointment_id) AS total_appointments,
    COUNT(DISTINCT a.patient_id) AS total_patients,
    SUM(a.doctor_consultation_fee) AS total_doctor_fees,
    SUM(a.hospital_charges) AS total_hospital_charges,
    COALESCE(SUM(ae.amount), 0) AS total_additional_expenses,
    (SUM(a.doctor_consultation_fee) + SUM(a.hospital_charges) + COALESCE(SUM(ae.amount), 0)) AS total_revenue
FROM appointments a
LEFT JOIN additional_expenses ae ON a.appointment_id = ae.appointment_id
WHERE a.status != 'Cancelled'
GROUP BY DATE(a.appointment_date);

-- ================================================
-- STORED PROCEDURES
-- ================================================

-- Procedure: Generate Token Number for Doctor
DELIMITER //
CREATE PROCEDURE generate_token_number(
    IN p_doctor_id INT,
    IN p_appointment_date DATE,
    OUT p_token_number VARCHAR(20)
)
BEGIN
    DECLARE token_count INT;
    DECLARE doctor_code VARCHAR(20);
    
    -- Get doctor code
    SELECT d.doctor_code INTO doctor_code
    FROM doctors d
    WHERE d.doctor_id = p_doctor_id;
    
    -- Count existing tokens for the doctor on that date
    SELECT COUNT(*) + 1 INTO token_count
    FROM appointments
    WHERE doctor_id = p_doctor_id 
    AND DATE(appointment_date) = p_appointment_date;
    
    -- Generate token: DOCCODE-DATE-NUMBER (e.g., DR001-20251210-001)
    SET p_token_number = CONCAT(
        doctor_code, '-',
        DATE_FORMAT(p_appointment_date, '%Y%m%d'), '-',
        LPAD(token_count, 3, '0')
    );
END //
DELIMITER ;

-- Procedure: Calculate Total Bill Amount
DELIMITER //
CREATE PROCEDURE calculate_bill_total(
    IN p_appointment_id INT,
    OUT p_total_amount DECIMAL(10, 2)
)
BEGIN
    SELECT 
        (a.doctor_consultation_fee + a.hospital_charges + COALESCE(SUM(ae.amount), 0))
    INTO p_total_amount
    FROM appointments a
    LEFT JOIN additional_expenses ae ON a.appointment_id = ae.appointment_id
    WHERE a.appointment_id = p_appointment_id
    GROUP BY a.appointment_id;
END //
DELIMITER ;

-- ================================================
-- TRIGGERS
-- ================================================

-- Trigger: Update bill total when additional expense is added
DELIMITER //
CREATE TRIGGER after_expense_insert
AFTER INSERT ON additional_expenses
FOR EACH ROW
BEGIN
    UPDATE bills
    SET additional_expenses_total = (
        SELECT COALESCE(SUM(amount), 0)
        FROM additional_expenses
        WHERE appointment_id = NEW.appointment_id
    ),
    total_amount = doctor_fee + hospital_charges + (
        SELECT COALESCE(SUM(amount), 0)
        FROM additional_expenses
        WHERE appointment_id = NEW.appointment_id
    )
    WHERE appointment_id = NEW.appointment_id;
END //
DELIMITER ;

-- Trigger: Log all patient registrations
DELIMITER //
CREATE TRIGGER after_patient_insert
AFTER INSERT ON patients
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (admin_id, action_type, table_name, record_id, action_description)
    VALUES (NEW.registered_by, 'INSERT', 'patients', NEW.patient_id, 
            CONCAT('New patient registered: ', NEW.patient_name));
END //
DELIMITER ;

-- ================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ================================================

-- Additional composite indexes for common queries
CREATE INDEX idx_appointment_date_doctor ON appointments(appointment_date, doctor_id);
CREATE INDEX idx_bill_date_doctor ON bills(bill_date, doctor_id);
CREATE INDEX idx_patient_registration ON patients(registration_date, is_active);

-- ================================================
-- END OF DATABASE SCHEMA
-- ================================================