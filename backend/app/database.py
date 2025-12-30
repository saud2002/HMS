"""
Database configuration and connection management for HMS
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from typing import Generator

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/hms")

# Determine database type
is_sqlite = DATABASE_URL.startswith("sqlite")
is_mysql = "mysql" in DATABASE_URL

# Create engine with proper configuration
if is_sqlite:
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # MySQL configuration
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Set to True for SQL debugging
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,    # Recycle connections every 5 minutes
        connect_args={
            "charset": "utf8mb4",
            "autocommit": False
        } if is_mysql else {}
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db() -> Generator:
    """
    Database dependency for FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_database_schema():
    """
    Create all tables and database objects
    """
    # Create tables from models
    Base.metadata.create_all(bind=engine)
    
    # Add hospital_charges column to doctors table if it doesn't exist
    with engine.connect() as conn:
        try:
            # Check if hospital_charges column exists
            result = conn.execute(text("SHOW COLUMNS FROM doctors LIKE 'hospital_charges'")).fetchone()
            if not result:
                print("🔧 Adding hospital_charges column to doctors table...")
                conn.execute(text("ALTER TABLE doctors ADD COLUMN hospital_charges DECIMAL(10,2) NOT NULL DEFAULT 0.00"))
                conn.commit()
                print("✅ hospital_charges column added successfully")
        except Exception as e:
            print(f"⚠️ Error adding hospital_charges column: {e}")
    
    # Create additional tables that are not in models
    with engine.connect() as conn:
        # Create doctor_schedules table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS doctor_schedules (
                schedule_id INT AUTO_INCREMENT PRIMARY KEY,
                doctor_id VARCHAR(20) NOT NULL,
                working_days VARCHAR(255) NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY unique_doctor_schedule (doctor_id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
            )
        """))
        conn.commit()
    
    # Execute additional SQL for views and procedures (MySQL only)
    if is_mysql:
        with engine.connect() as conn:
            # Create views
            create_views(conn)
            # Create stored procedures
            create_stored_procedures(conn)

def create_views(conn):
    """Create database views for reporting (MySQL only)"""
    
    # Drop existing views if they exist
    views_to_drop = [
        "view_daily_doctor_report",
        "view_daily_hospital_report", 
        "view_doctor_wise_summary",
        "view_appointment_details"
    ]
    
    for view in views_to_drop:
        try:
            conn.execute(text(f"DROP VIEW IF EXISTS {view}"))
        except:
            pass
    
    # View 1: Daily Doctor Report
    conn.execute(text("""
        CREATE VIEW view_daily_doctor_report AS
        SELECT 
            d.doctor_id,
            d.doctor_name,
            d.specialization,
            a.appointment_date,
            COUNT(a.appointment_id) AS total_appointments,
            SUM(a.doctor_charges) AS total_consultation_fees,
            GROUP_CONCAT(DISTINCT p.patient_name ORDER BY a.appointment_time SEPARATOR ', ') AS patient_names
        FROM doctors d
        LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
        LEFT JOIN patients p ON a.patient_id = p.patient_id
        GROUP BY d.doctor_id, d.doctor_name, d.specialization, a.appointment_date
    """))
    
    # View 2: Daily Hospital Report
    conn.execute(text("""
        CREATE VIEW view_daily_hospital_report AS
        SELECT 
            b.bill_date,
            COUNT(DISTINCT a.patient_id) AS total_patients,
            COUNT(a.appointment_id) AS total_appointments,
            SUM(b.doctor_charges) AS total_doctor_fees,
            SUM(b.hospital_charges) AS total_hospital_charges,
            SUM(b.additional_expenses_total) AS total_additional_expenses,
            SUM(b.total_amount) AS grand_total_revenue
        FROM bills b
        JOIN appointments a ON b.appointment_id = a.appointment_id
        GROUP BY b.bill_date
    """))
    
    # View 3: Doctor-wise Daily Summary
    conn.execute(text("""
        CREATE VIEW view_doctor_wise_summary AS
        SELECT 
            a.appointment_date,
            d.doctor_id,
            d.doctor_name,
            d.specialization,
            COUNT(a.appointment_id) AS appointment_count,
            SUM(a.doctor_charges) AS doctor_revenue
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.doctor_id
        GROUP BY a.appointment_date, d.doctor_id, d.doctor_name, d.specialization
    """))
    
    # View 4: Appointment Details with Bill Info
    conn.execute(text("""
        CREATE VIEW view_appointment_details AS
        SELECT 
            a.appointment_id,
            a.token_number,
            a.appointment_date,
            a.appointment_time,
            p.patient_id,
            p.patient_name,
            p.age,
            p.phone_number,
            p.nic,
            d.doctor_id,
            d.doctor_name,
            d.specialization,
            a.doctor_charges,
            a.hospital_charges,
            COALESCE(b.additional_expenses_total, 0) AS additional_expenses_total,
            COALESCE(b.total_amount, 0) AS total_amount,
            COALESCE(b.payment_status, 'Pending') AS payment_status,
            a.status AS appointment_status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        LEFT JOIN bills b ON a.appointment_id = b.appointment_id
    """))
    
    conn.commit()

def create_stored_procedures(conn):
    """Create stored procedures for business logic (MySQL only)"""
    
    # Drop existing procedures
    procedures_to_drop = [
        "sp_generate_token",
        "sp_create_appointment_with_bill",
        "sp_add_additional_expense"
    ]
    
    for proc in procedures_to_drop:
        try:
            conn.execute(text(f"DROP PROCEDURE IF EXISTS {proc}"))
        except:
            pass
    
    # Procedure 1: Generate Token Number
    conn.execute(text("""
        CREATE PROCEDURE sp_generate_token(
            IN p_doctor_id VARCHAR(20),
            IN p_appointment_date DATE,
            OUT p_token_number VARCHAR(50)
        )
        BEGIN
            DECLARE v_token_count INT;
            
            -- Get or create token counter for doctor and date
            INSERT INTO token_counter (doctor_id, token_date, last_token_number)
            VALUES (p_doctor_id, p_appointment_date, 0)
            ON DUPLICATE KEY UPDATE last_token_number = last_token_number + 1;
            
            -- Get the current token number
            SELECT last_token_number INTO v_token_count
            FROM token_counter
            WHERE doctor_id = p_doctor_id AND token_date = p_appointment_date;
            
            -- Generate token number format: DOCID-YYYYMMDD-NNN
            SET p_token_number = CONCAT(
                p_doctor_id, '-',
                DATE_FORMAT(p_appointment_date, '%Y%m%d'), '-',
                LPAD(v_token_count, 3, '0')
            );
        END
    """))
    
    # Procedure 2: Create Appointment with Bill
    conn.execute(text("""
        CREATE PROCEDURE sp_create_appointment_with_bill(
            IN p_patient_id INT,
            IN p_doctor_id VARCHAR(20),
            IN p_appointment_date DATE,
            IN p_hospital_charges DECIMAL(10,2),
            IN p_admin_id INT,
            OUT p_appointment_id INT,
            OUT p_bill_id INT,
            OUT p_token_number VARCHAR(50)
        )
        BEGIN
            DECLARE v_doctor_charges DECIMAL(10,2);
            DECLARE v_total_amount DECIMAL(10,2);
            
            -- Get doctor consultation charges
            SELECT consultation_charges INTO v_doctor_charges
            FROM doctors
            WHERE doctor_id = p_doctor_id AND status = 'Active';
            
            -- Generate token
            CALL sp_generate_token(p_doctor_id, p_appointment_date, p_token_number);
            
            -- Create appointment
            INSERT INTO appointments (
                patient_id, doctor_id, appointment_date, token_number, 
                doctor_charges, hospital_charges, created_by
            )
            VALUES (
                p_patient_id, p_doctor_id, p_appointment_date, p_token_number,
                v_doctor_charges, p_hospital_charges, p_admin_id
            );
            
            SET p_appointment_id = LAST_INSERT_ID();
            
            -- Calculate total
            SET v_total_amount = v_doctor_charges + p_hospital_charges;
            
            -- Create bill
            INSERT INTO bills (
                appointment_id, bill_date, doctor_charges, hospital_charges,
                additional_expenses_total, subtotal, total_amount, created_by
            )
            VALUES (
                p_appointment_id, p_appointment_date, v_doctor_charges, p_hospital_charges,
                0, v_total_amount, v_total_amount, p_admin_id
            );
            
            SET p_bill_id = LAST_INSERT_ID();
        END
    """))
    
    # Procedure 3: Add Additional Expense and Update Bill
    conn.execute(text("""
        CREATE PROCEDURE sp_add_additional_expense(
            IN p_appointment_id INT,
            IN p_service_type VARCHAR(50),
            IN p_service_description VARCHAR(255),
            IN p_amount DECIMAL(10,2)
        )
        BEGIN
            -- Add expense
            INSERT INTO additional_expenses (appointment_id, service_type, service_description, amount)
            VALUES (p_appointment_id, p_service_type, p_service_description, p_amount);
            
            -- Update bill totals
            UPDATE bills
            SET 
                additional_expenses_total = (
                    SELECT COALESCE(SUM(amount), 0)
                    FROM additional_expenses
                    WHERE appointment_id = p_appointment_id
                ),
                subtotal = doctor_charges + hospital_charges + (
                    SELECT COALESCE(SUM(amount), 0)
                    FROM additional_expenses
                    WHERE appointment_id = p_appointment_id
                ),
                total_amount = doctor_charges + hospital_charges + (
                    SELECT COALESCE(SUM(amount), 0)
                    FROM additional_expenses
                    WHERE appointment_id = p_appointment_id
                )
            WHERE appointment_id = p_appointment_id;
        END
    """))
    
    conn.commit()

def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False