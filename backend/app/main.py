# main.py - Hospital Management System FastAPI Backend
# Run: uvicorn main:app --reload --port 8000

from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import Optional, List
from datetime import date, datetime, timedelta
import os
from pathlib import Path

# Import our modules
from .database import get_db, create_database_schema, test_connection
from .config import settings
from .models import *
from .schemas import *
from .schemas.bill import PaymentStatusUpdate
from .models.voucher import Voucher, VoucherType, VoucherStatus
from .schemas.voucher import VoucherCreate, VoucherUpdate, VoucherResponse, VoucherSummary, DoctorPaymentSummary

# Import JWT only
from jose import jwt

# =====================================================
# FASTAPI APP
# =====================================================
app = FastAPI(
    title=settings.app_name,
    description="Complete Hospital Management System with Patient Registration, Appointments, Billing & Reports",
    version=settings.app_version,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (frontend)
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and check connection"""
    if not test_connection():
        raise Exception("Failed to connect to database")
    
    try:
        create_database_schema()
        print("✅ Database schema initialized successfully")
    except Exception as e:
        print(f"⚠️ Database schema initialization warning: {e}")
        # Continue anyway as tables might already exist

# =====================================================
# UTILITY FUNCTIONS
# =====================================================
def generate_token_number(db: Session, doctor_id: str, appointment_date: date) -> str:
    """Generate token number using database procedure or fallback method"""
    # Skip stored procedure for now to use our custom logic
    # try:
    #     # Try to use stored procedure first
    #     result = db.execute(
    #         text("CALL sp_generate_token(:doctor_id, :appointment_date, @token_number)"),
    #         {"doctor_id": doctor_id, "appointment_date": appointment_date}
    #     )
    #     token_result = db.execute(text("SELECT @token_number")).fetchone()
    #     if token_result and token_result[0]:
    #         return token_result[0]
    # except Exception as e:
    #     print(f"Stored procedure failed, using fallback: {e}")
    
    print(f"🔍 Generating token for doctor {doctor_id} on {appointment_date}")
    
    # Fallback method
    counter = db.query(TokenCounter).filter(
        TokenCounter.doctor_id == doctor_id,
        TokenCounter.token_date == appointment_date
    ).first()
    
    print(f"🔍 Looking for existing counter for doctor {doctor_id} on {appointment_date}")
    
    if counter:
        print(f"🔍 Found existing counter with last_token_number: {counter.last_token_number}")
        
        # Fix any counter that has 0 or negative value
        if counter.last_token_number <= 0:
            print(f"🔍 WARNING: Counter had invalid value {counter.last_token_number}, resetting to 0")
            counter.last_token_number = 0
        
        # Increment the counter for existing record
        counter.last_token_number += 1
        token_num = counter.last_token_number
        print(f"🔍 Existing counter found, incremented to: {token_num}")
    else:
        print(f"🔍 No existing counter found, creating new one")
        # Create new counter starting from 1 (not 0)
        counter = TokenCounter(
            doctor_id=doctor_id,
            token_date=appointment_date,
            last_token_number=1
        )
        db.add(counter)
        token_num = 1
        print(f"🔍 New counter created, starting at: {token_num}")
    
    # Final safety check - ensure token number is never 0
    if token_num <= 0:
        print(f"🔍 CRITICAL: Token number was {token_num}, forcing to 1")
        token_num = 1
        counter.last_token_number = 1
    
    db.commit()
    date_str = appointment_date.strftime("%Y%m%d")
    token_string = f"{doctor_id}-{date_str}-{token_num:03d}"
    print(f"🔍 Generated token: {token_string}")
    return token_string

# Debug endpoint to reset token counters
@app.post("/api/debug/reset-token-counters")
def reset_token_counters(db: Session = Depends(get_db)):
    """Reset all token counters to start from 1"""
    try:
        # Delete all existing token counters
        db.query(TokenCounter).delete()
        db.commit()
        return {"message": "All token counters reset successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error resetting counters: {str(e)}")

def log_action(db: Session, admin_id: int, action: str, table: str = None, record_id: int = None, desc: str = None):
    """Log system action for audit trail"""
    SystemLog.log_action(db, admin_id, action, table, record_id, desc)

def get_current_user(authorization: str = None):
    """Get current user from JWT token (optional for frontend routes)"""
    if not authorization:
        return None
    
    try:
        if not authorization.startswith("Bearer "):
            return None
        
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        admin_id = payload.get("admin_id")
        
        if username and admin_id:
            return {"username": username, "admin_id": admin_id}
    except Exception:
        pass
    
    return None

def check_frontend_auth(request: Request):
    """Check authentication for frontend routes"""
    # Check for authentication token in cookies or headers
    auth_token = request.cookies.get("access_token") or request.headers.get("authorization")
    
    # Debug: Print token status (remove in production)
    print(f"🔍 Auth check - Token found: {bool(auth_token)}")
    
    # If no token, redirect to login
    if not auth_token:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/login.html", status_code=302)
    
    # Validate token
    user = get_current_user(auth_token if auth_token.startswith("Bearer ") else f"Bearer {auth_token}")
    if not user:
        print(f"🔍 Auth check - Token invalid")
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/login.html", status_code=302)
    
    print(f"🔍 Auth check - User authenticated: {user.get('username')}")
    return None  # Authentication successful

# =====================================================
# API ENDPOINTS
# =====================================================

# --- Root Endpoint - Serve Frontend ---
@app.get("/")
def serve_frontend(request: Request):
    """Serve the main frontend page or redirect to login"""
    # Check authentication
    auth_redirect = check_frontend_auth(request)
    if auth_redirect:
        return auth_redirect
    
    # Serve dashboard if authenticated
    frontend_path = Path(__file__).parent.parent.parent / "frontend" / "index.html"
    if frontend_path.exists():
        return FileResponse(str(frontend_path))
    else:
        return {
            "message": "🏥 Hospital Management System API",
            "version": settings.app_version,
            "status": "running",
            "docs": "/docs",
            "health": "/api/health",
            "login": "/login.html",
            "timestamp": datetime.now().isoformat()
        }

# --- Login Route ---
@app.get("/login.html")
def serve_login():
    frontend_path = Path(__file__).parent.parent.parent / "frontend" / "login.html"
    return FileResponse(str(frontend_path))

@app.get("/login")
def redirect_to_login():
    frontend_path = Path(__file__).parent.parent.parent / "frontend" / "login.html"
    return FileResponse(str(frontend_path))

@app.get("/index.html")
def serve_index(request: Request):
    """Serve dashboard/index page with authentication check"""
    # Check authentication
    auth_redirect = check_frontend_auth(request)
    if auth_redirect:
        return auth_redirect
    
    frontend_path = Path(__file__).parent.parent.parent / "frontend" / "index.html"
    return FileResponse(str(frontend_path))

@app.get("/test_navigation.html")
def serve_test_navigation():
    """Serve navigation test page (no auth required for testing)"""
    frontend_path = Path(__file__).parent.parent.parent / "frontend" / "test_navigation.html"
    return FileResponse(str(frontend_path))

# --- Frontend Routes ---
@app.get("/patients.html")
def serve_patients(request: Request):
    # Check authentication
    auth_redirect = check_frontend_auth(request)
    if auth_redirect:
        return auth_redirect
    
    frontend_path = Path(__file__).parent.parent.parent / "frontend" / "patients.html"
    return FileResponse(str(frontend_path))

@app.get("/doctors.html") 
def serve_doctors(request: Request):
    # Check authentication
    auth_redirect = check_frontend_auth(request)
    if auth_redirect:
        return auth_redirect
    
    frontend_path = Path(__file__).parent.parent.parent / "frontend" / "doctors.html"
    return FileResponse(str(frontend_path))

@app.get("/appointments.html")
def serve_appointments(request: Request):
    # Check authentication
    auth_redirect = check_frontend_auth(request)
    if auth_redirect:
        return auth_redirect
    
    frontend_path = Path(__file__).parent.parent.parent / "frontend" / "appointments.html"
    return FileResponse(str(frontend_path))

@app.get("/reports.html")
def serve_reports(request: Request):
    # Check authentication
    auth_redirect = check_frontend_auth(request)
    if auth_redirect:
        return auth_redirect
    
    frontend_path = Path(__file__).parent.parent.parent / "frontend" / "reports.html"
    return FileResponse(str(frontend_path))

@app.get("/settings.html")
def serve_settings(request: Request):
    # Check authentication
    auth_redirect = check_frontend_auth(request)
    if auth_redirect:
        return auth_redirect
    
    frontend_path = Path(__file__).parent.parent.parent / "frontend" / "settings.html"
    return FileResponse(str(frontend_path))

@app.get("/vouchers.html")
def serve_vouchers(request: Request):
    # Check authentication
    auth_redirect = check_frontend_auth(request)
    if auth_redirect:
        return auth_redirect
    
    frontend_path = Path(__file__).parent.parent.parent / "frontend" / "vouchers.html"
    return FileResponse(str(frontend_path))

# --- API Info Endpoint ---
@app.get("/api")
def api_info():
    return {
        "message": "🏥 Hospital Management System API",
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "health": "/api/health",
        "frontend": "Available at root URL (/)",
        "timestamp": datetime.now().isoformat()
    }

# --- Health Check ---
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "HMS API is running", "timestamp": datetime.now().isoformat()}

# --- Dashboard Stats ---
@app.get("/api/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    today = date.today()
    return {
        "total_patients": db.query(Patient).count(),
        "total_doctors": db.query(Doctor).filter(Doctor.status == "Active").count(),
        "today_appointments": db.query(Appointment).filter(Appointment.appointment_date == today).count(),
        "pending_bills": db.query(Bill).filter(Bill.payment_status == "Pending").count(),
        "today_revenue": float(db.query(func.sum(Bill.total_amount)).filter(
            Bill.bill_date == today, Bill.payment_status == "Paid"
        ).scalar() or 0)
    }

# =====================================================
# PATIENTS ENDPOINTS
# =====================================================
@app.get("/api/patients")
def get_patients(
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Patient)
        if search:
            query = query.filter(
                (Patient.patient_name.ilike(f"%{search}%")) |
                (Patient.nic.ilike(f"%{search}%")) |
                (Patient.phone_number.ilike(f"%{search}%"))
            )
        patients = query.order_by(Patient.patient_id.desc()).offset(skip).limit(limit).all()
        
        # Convert to dict to avoid enum serialization issues
        result = []
        for p in patients:
            result.append({
                "patient_id": p.patient_id,
                "patient_name": p.patient_name,
                "age": p.age,
                "phone_number": p.phone_number,
                "gender": p.gender.value if hasattr(p.gender, 'value') else str(p.gender),
                "nic": p.nic,
                "registration_date": p.registration_date.isoformat(),
                "created_at": p.created_at.isoformat(),
                "updated_at": p.updated_at.isoformat()
            })
        return result
    except Exception as e:
        print(f"Error in get_patients: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/patients/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.get("/api/patients/nic/{nic}")
def get_patient_by_nic(nic: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.nic == nic).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/api/patients")
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    try:
        # Check if NIC already exists
        existing = db.query(Patient).filter(Patient.nic == patient.nic).first()
        if existing:
            raise HTTPException(status_code=400, detail="Patient with this NIC already exists")
        
        db_patient = Patient(
            patient_name=patient.patient_name,
            age=patient.age,
            phone_number=patient.phone_number,
            gender=patient.gender,  # Now using string directly
            nic=patient.nic,
            registration_date=patient.registration_date or date.today()
        )
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        
        # Return as dict to avoid serialization issues
        return {
            "patient_id": db_patient.patient_id,
            "patient_name": db_patient.patient_name,
            "age": db_patient.age,
            "phone_number": db_patient.phone_number,
            "gender": db_patient.gender,  # Now string directly
            "nic": db_patient.nic,
            "registration_date": db_patient.registration_date.isoformat(),
            "created_at": db_patient.created_at.isoformat(),
            "updated_at": db_patient.updated_at.isoformat(),
            "message": "Patient created successfully"
        }
    except Exception as e:
        print(f"Error creating patient: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create patient: {str(e)}")

@app.put("/api/patients/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_data = patient.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_patient, key, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.delete("/api/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Check if patient has appointments
    if db.query(Appointment).filter(Appointment.patient_id == patient_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete patient with existing appointments")
    
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully"}

# =====================================================
# DOCTORS ENDPOINTS (Add to main.py)
# =====================================================
@app.get("/api/doctors")
def get_doctors(
    specialization: Optional[str] = None,
    status: Optional[str] = "Active",
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Doctor)
        if status:
            query = query.filter(Doctor.status == status)
        if specialization:
            query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
        doctors = query.all()
        
        # Convert to dict to avoid serialization issues
        result = []
        for d in doctors:
            result.append({
                "doctor_id": d.doctor_id,
                "doctor_name": d.doctor_name,
                "specialization": d.specialization,
                "consultation_charges": float(d.consultation_charges),
                "hospital_charges": float(d.hospital_charges),
                "status": d.status,
                "created_at": d.created_at.isoformat(),
                "updated_at": d.updated_at.isoformat()
            })
        return result
    except Exception as e:
        print(f"Error in get_doctors: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/doctors/specializations")
def get_specializations(db: Session = Depends(get_db)):
    specs = db.query(Doctor.specialization).distinct().all()
    return [s[0] for s in specs if s[0]]

# =====================================================
# DOCTOR SCHEDULES ENDPOINTS (moved before parameterized routes)
# =====================================================
@app.get("/api/doctors/schedules")
def get_all_doctor_schedules(db: Session = Depends(get_db)):
    try:
        print("🔍 Getting all doctor schedules...")
        # Get all doctor schedules with doctor information
        schedules = db.execute(text("""
            SELECT 
                ds.doctor_id,
                d.doctor_name,
                d.specialization,
                ds.working_days,
                ds.start_time,
                ds.end_time,
                ds.notes,
                ds.created_at
            FROM doctor_schedules ds
            JOIN doctors d ON ds.doctor_id = d.doctor_id
            WHERE d.status = 'Active'
            ORDER BY d.doctor_name
        """)).fetchall()
        
        print(f"🔍 Found {len(schedules)} schedules")
        
        result = []
        for schedule in schedules:
            # Convert timedelta to string format (HH:MM)
            start_time = str(schedule.start_time) if schedule.start_time else "00:00:00"
            end_time = str(schedule.end_time) if schedule.end_time else "00:00:00"
            
            # Remove seconds if present (e.g., "15:00:00" -> "15:00")
            if start_time.count(':') == 2:
                start_time = start_time.rsplit(':', 1)[0]
            if end_time.count(':') == 2:
                end_time = end_time.rsplit(':', 1)[0]
            
            result.append({
                "doctor_id": schedule.doctor_id,
                "doctor_name": schedule.doctor_name,
                "specialization": schedule.specialization,
                "working_days": schedule.working_days,
                "start_time": start_time,
                "end_time": end_time,
                "notes": schedule.notes or "",
                "created_at": schedule.created_at.isoformat() if schedule.created_at else None
            })
        
        print(f"🔍 Returning: {result}")
        return result
        
    except Exception as e:
        print(f"❌ Error in get_all_doctor_schedules: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/doctors/schedule")
def save_doctor_schedule(schedule_data: dict, db: Session = Depends(get_db)):
    try:
        print(f"🔍 Received schedule data: {schedule_data}")
        
        doctor_id = schedule_data.get("doctor_id")
        working_days = schedule_data.get("working_days")
        start_time = schedule_data.get("start_time")
        end_time = schedule_data.get("end_time")
        notes = schedule_data.get("notes", "")
        
        print(f"🔍 Parsed data: doctor_id={doctor_id}, working_days={working_days}, start_time={start_time}, end_time={end_time}")
        
        if not all([doctor_id, working_days, start_time, end_time]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Check if doctor exists
        doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        
        print(f"🔍 Doctor found: {doctor.doctor_name}")
        
        # Check if schedule already exists
        existing_schedule = db.execute(text("""
            SELECT * FROM doctor_schedules WHERE doctor_id = :doctor_id
        """), {"doctor_id": doctor_id}).fetchone()
        
        if existing_schedule:
            print("🔍 Updating existing schedule")
            # Update existing schedule
            db.execute(text("""
                UPDATE doctor_schedules 
                SET working_days = :working_days, start_time = :start_time, 
                    end_time = :end_time, notes = :notes, updated_at = NOW()
                WHERE doctor_id = :doctor_id
            """), {
                "doctor_id": doctor_id,
                "working_days": working_days,
                "start_time": start_time,
                "end_time": end_time,
                "notes": notes
            })
            message = "Schedule updated successfully"
        else:
            print("🔍 Creating new schedule")
            # Create new schedule
            db.execute(text("""
                INSERT INTO doctor_schedules (doctor_id, working_days, start_time, end_time, notes, created_at)
                VALUES (:doctor_id, :working_days, :start_time, :end_time, :notes, NOW())
            """), {
                "doctor_id": doctor_id,
                "working_days": working_days,
                "start_time": start_time,
                "end_time": end_time,
                "notes": notes
            })
            message = "Schedule created successfully"
        
        db.commit()
        print(f"✅ {message}")
        return {"message": message}
        
    except Exception as e:
        print(f"❌ Error in save_doctor_schedule: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/doctors/{doctor_id}/schedule")
def get_doctor_schedule(doctor_id: str, db: Session = Depends(get_db)):
    schedule = db.execute(text("""
        SELECT * FROM doctor_schedules WHERE doctor_id = :doctor_id
    """), {"doctor_id": doctor_id}).fetchone()
    
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # Convert timedelta to string format
    start_time = str(schedule.start_time) if schedule.start_time else "00:00:00"
    end_time = str(schedule.end_time) if schedule.end_time else "00:00:00"
    
    # Remove seconds if present
    if start_time.count(':') == 2:
        start_time = start_time.rsplit(':', 1)[0]
    if end_time.count(':') == 2:
        end_time = end_time.rsplit(':', 1)[0]
    
    return {
        "doctor_id": schedule.doctor_id,
        "working_days": schedule.working_days,
        "start_time": start_time,
        "end_time": end_time,
        "notes": schedule.notes or ""
    }

@app.delete("/api/doctors/{doctor_id}/schedule")
def delete_doctor_schedule(doctor_id: str, db: Session = Depends(get_db)):
    # Check if schedule exists
    existing_schedule = db.execute(text("""
        SELECT * FROM doctor_schedules WHERE doctor_id = :doctor_id
    """), {"doctor_id": doctor_id}).fetchone()
    
    if not existing_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # Delete the schedule
    db.execute(text("""
        DELETE FROM doctor_schedules WHERE doctor_id = :doctor_id
    """), {"doctor_id": doctor_id})
    
    db.commit()
    return {"message": "Schedule deleted successfully"}

@app.get("/api/doctors/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: str, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.post("/api/doctors")
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    try:
        existing = db.query(Doctor).filter(Doctor.doctor_id == doctor.doctor_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Doctor ID already exists")
        
        db_doctor = Doctor(
            doctor_id=doctor.doctor_id,
            doctor_name=doctor.doctor_name,
            specialization=doctor.specialization,
            consultation_charges=doctor.consultation_charges,
            hospital_charges=doctor.hospital_charges,
            status="Active"
        )
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        
        # Return as dict
        return {
            "doctor_id": db_doctor.doctor_id,
            "doctor_name": db_doctor.doctor_name,
            "specialization": db_doctor.specialization,
            "consultation_charges": float(db_doctor.consultation_charges),
            "hospital_charges": float(db_doctor.hospital_charges),
            "status": db_doctor.status,
            "created_at": db_doctor.created_at.isoformat(),
            "updated_at": db_doctor.updated_at.isoformat(),
            "message": "Doctor created successfully"
        }
    except Exception as e:
        print(f"Error creating doctor: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create doctor: {str(e)}")

@app.put("/api/doctors/{doctor_id}", response_model=DoctorResponse)
def update_doctor(doctor_id: str, doctor: DoctorUpdate, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    update_data = doctor.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_doctor, key, value)
    
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@app.delete("/api/doctors/{doctor_id}")
def deactivate_doctor(doctor_id: str, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db_doctor.status = "Inactive"
    db.commit()
    return {"message": "Doctor deactivated successfully"}

@app.delete("/api/doctors/{doctor_id}/delete")
def delete_doctor_permanently(doctor_id: str, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Check if doctor has any appointments
    appointment_count = db.query(Appointment).filter(Appointment.doctor_id == doctor_id).count()
    if appointment_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete doctor. Doctor has {appointment_count} associated appointments. Please deactivate instead."
        )
    
    # If no appointments, safe to delete
    db.delete(db_doctor)
    db.commit()
    return {"message": "Doctor deleted permanently"}

# =====================================================
# APPOINTMENTS ENDPOINTS
# =====================================================
@app.get("/api/appointments")
def get_appointments(
    status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    doctor_id: Optional[str] = None,
    patient_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Appointment)
    
    if status:
        query = query.filter(Appointment.status == status)
    if date_from:
        query = query.filter(Appointment.appointment_date >= date_from)
    if date_to:
        query = query.filter(Appointment.appointment_date <= date_to)
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
    
    appointments = query.order_by(Appointment.appointment_date.desc()).offset(skip).limit(limit).all()
    
    result = []
    for apt in appointments:
        # Get the bill information for this appointment
        bill = db.query(Bill).filter(Bill.appointment_id == apt.appointment_id).first()
        
        result.append({
            "appointment_id": apt.appointment_id,
            "patient_id": apt.patient_id,
            "doctor_id": apt.doctor_id,
            "appointment_date": apt.appointment_date.isoformat(),
            "appointment_time": apt.appointment_time.isoformat() if apt.appointment_time else None,
            "token_number": apt.token_number,
            "doctor_charges": float(apt.doctor_charges),
            "hospital_charges": float(apt.hospital_charges),
            "status": apt.status,
            "patient_name": apt.patient.patient_name if apt.patient else None,
            "patient_nic": apt.patient.nic if apt.patient else None,
            "patient_phone": apt.patient.phone_number if apt.patient else None,
            "doctor_name": apt.doctor.doctor_name if apt.doctor else None,
            "specialization": apt.doctor.specialization if apt.doctor else None,
            "created_at": apt.created_at.isoformat() if apt.created_at else None,
            # Include bill information
            "bill_total": float(bill.total_amount) if bill else float(apt.doctor_charges) + float(apt.hospital_charges),
            "additional_expenses": float(bill.additional_expenses_total) if bill else 0.0,
            "payment_status": bill.payment_status if bill else "Pending"
        })
    return result

@app.get("/api/appointments/today")
def get_today_appointments(db: Session = Depends(get_db)):
    return get_appointments(date_from=date.today(), date_to=date.today(), db=db)

@app.get("/api/appointments/doctor/{doctor_id}/today")
def get_doctor_today_appointments(doctor_id: str, db: Session = Depends(get_db)):
    return get_appointments(doctor_id=doctor_id, date_from=date.today(), date_to=date.today(), db=db)

@app.get("/api/appointments/{appointment_id}")
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    apt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Get additional expenses
    expenses = db.query(AdditionalExpense).filter(
        AdditionalExpense.appointment_id == appointment_id
    ).all()
    
    return {
        "appointment_id": apt.appointment_id,
        "patient_id": apt.patient_id,
        "doctor_id": apt.doctor_id,
        "appointment_date": apt.appointment_date.isoformat(),
        "token_number": apt.token_number,
        "doctor_charges": float(apt.doctor_charges),
        "hospital_charges": float(apt.hospital_charges),
        "status": apt.status,
        "patient": {
            "patient_id": apt.patient.patient_id,
            "patient_name": apt.patient.patient_name,
            "age": apt.patient.age,
            "phone_number": apt.patient.phone_number,
            "nic": apt.patient.nic,
            "gender": apt.patient.gender
        } if apt.patient else None,
        "doctor": {
            "doctor_id": apt.doctor.doctor_id,
            "doctor_name": apt.doctor.doctor_name,
            "specialization": apt.doctor.specialization
        } if apt.doctor else None,
        "bill": {
            "bill_id": apt.bill.bill_id,
            "total_amount": float(apt.bill.total_amount),
            "payment_status": apt.bill.payment_status
        } if apt.bill else None,
        "additional_expenses": [
            {
                "expense_id": e.expense_id,
                "service_type": e.service_type,
                "service_description": e.service_description,
                "amount": float(e.amount)
            } for e in expenses
        ]
    }

@app.post("/api/appointments")
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    # Validate patient exists
    patient = db.query(Patient).filter(Patient.patient_id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Validate doctor exists and is active
    doctor = db.query(Doctor).filter(
        Doctor.doctor_id == appointment.doctor_id,
        Doctor.status == "Active"
    ).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found or inactive")
    
    # Generate token number
    token_number = generate_token_number(db, appointment.doctor_id, appointment.appointment_date)
    
    # Get doctor's consultation charges and hospital charges
    doctor_charges = float(doctor.consultation_charges)
    hospital_charges = float(doctor.hospital_charges)  # Now based on doctor
    total_amount = doctor_charges + hospital_charges
    
    # Create appointment
    db_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        token_number=token_number,
        doctor_charges=doctor_charges,
        hospital_charges=hospital_charges,
        status="Scheduled"
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    
    # Create bill
    db_bill = Bill(
        appointment_id=db_appointment.appointment_id,
        bill_date=appointment.appointment_date,
        doctor_charges=doctor_charges,
        hospital_charges=hospital_charges,
        additional_expenses_total=0,
        subtotal=total_amount,
        total_amount=total_amount,
        payment_status="Pending"
    )
    db.add(db_bill)
    db.commit()
    
    return {
        "appointment_id": db_appointment.appointment_id,
        "token_number": token_number,
        "patient_name": patient.patient_name,
        "doctor_name": doctor.doctor_name,
        "appointment_date": appointment.appointment_date.isoformat(),
        "doctor_charges": doctor_charges,
        "hospital_charges": hospital_charges,
        "total_amount": total_amount,
        "message": "Appointment created successfully"
    }

@app.patch("/api/appointments/{appointment_id}/status")
def update_appointment_status(appointment_id: int, status: str, db: Session = Depends(get_db)):
    valid_statuses = ["Scheduled", "Completed", "Cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    apt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    apt.status = status
    db.commit()
    return {"message": f"Appointment status updated to {status}"}

@app.delete("/api/appointments/{appointment_id}")
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    apt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    apt.status = "Cancelled"
    db.commit()
    return {"message": "Appointment cancelled successfully"}

# =====================================================
# ADDITIONAL EXPENSES ENDPOINTS
# =====================================================
@app.get("/api/expenses/appointment/{appointment_id}")
def get_appointment_expenses(appointment_id: int, db: Session = Depends(get_db)):
    expenses = db.query(AdditionalExpense).filter(
        AdditionalExpense.appointment_id == appointment_id
    ).all()
    return [{
        "expense_id": e.expense_id,
        "service_type": e.service_type,
        "service_description": e.service_description,
        "amount": float(e.amount),
        "created_at": e.created_at.isoformat()
    } for e in expenses]

@app.post("/api/expenses")
def add_additional_expense(expense: AdditionalExpenseCreate, db: Session = Depends(get_db)):
    # Verify appointment exists
    apt = db.query(Appointment).filter(Appointment.appointment_id == expense.appointment_id).first()
    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Add expense
    db_expense = AdditionalExpense(
        appointment_id=expense.appointment_id,
        service_type=expense.service_type,
        service_description=expense.service_description,
        amount=expense.amount
    )
    db.add(db_expense)
    db.commit()
    
    # Update bill totals
    bill = db.query(Bill).filter(Bill.appointment_id == expense.appointment_id).first()
    if bill:
        total_expenses = db.query(func.sum(AdditionalExpense.amount)).filter(
            AdditionalExpense.appointment_id == expense.appointment_id
        ).scalar() or 0
        
        bill.additional_expenses_total = total_expenses
        bill.subtotal = float(bill.doctor_charges) + float(bill.hospital_charges) + float(total_expenses)
        bill.total_amount = bill.subtotal
        db.commit()
    
    return {"message": "Expense added successfully", "expense_id": db_expense.expense_id}

@app.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(AdditionalExpense).filter(AdditionalExpense.expense_id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    appointment_id = expense.appointment_id
    db.delete(expense)
    db.commit()
    
    # Update bill totals
    bill = db.query(Bill).filter(Bill.appointment_id == appointment_id).first()
    if bill:
        total_expenses = db.query(func.sum(AdditionalExpense.amount)).filter(
            AdditionalExpense.appointment_id == appointment_id
        ).scalar() or 0
        
        bill.additional_expenses_total = total_expenses
        bill.subtotal = float(bill.doctor_charges) + float(bill.hospital_charges) + float(total_expenses)
        bill.total_amount = bill.subtotal
        db.commit()
    
    return {"message": "Expense deleted successfully"}

# =====================================================
# BILLS ENDPOINTS (Add to main.py)
# =====================================================
@app.get("/api/bills")
def get_bills(
    payment_status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Bill)
    
    if payment_status:
        query = query.filter(Bill.payment_status == payment_status)
    if date_from:
        query = query.filter(Bill.bill_date >= date_from)
    if date_to:
        query = query.filter(Bill.bill_date <= date_to)
    
    bills = query.order_by(Bill.bill_date.desc()).offset(skip).limit(limit).all()
    
    result = []
    for bill in bills:
        apt = bill.appointment
        result.append({
            "bill_id": bill.bill_id,
            "appointment_id": bill.appointment_id,
            "token_number": apt.token_number if apt else None,
            "bill_date": bill.bill_date.isoformat(),
            "patient_name": apt.patient.patient_name if apt and apt.patient else None,
            "doctor_name": apt.doctor.doctor_name if apt and apt.doctor else None,
            "doctor_charges": float(bill.doctor_charges),
            "hospital_charges": float(bill.hospital_charges),
            "additional_expenses_total": float(bill.additional_expenses_total),
            "total_amount": float(bill.total_amount),
            "payment_status": bill.payment_status
        })
    return result

@app.get("/api/bills/{bill_id}")
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(Bill.bill_id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    apt = bill.appointment
    expenses = db.query(AdditionalExpense).filter(
        AdditionalExpense.appointment_id == bill.appointment_id
    ).all()
    
    return {
        "bill_id": bill.bill_id,
        "appointment_id": bill.appointment_id,
        "bill_date": bill.bill_date.isoformat(),
        "bill_time": bill.bill_time.isoformat() if bill.bill_time else None,
        "token_number": apt.token_number if apt else None,
        "patient": {
            "patient_id": apt.patient.patient_id,
            "patient_name": apt.patient.patient_name,
            "age": apt.patient.age,
            "phone_number": apt.patient.phone_number,
            "nic": apt.patient.nic
        } if apt and apt.patient else None,
        "doctor": {
            "doctor_id": apt.doctor.doctor_id,
            "doctor_name": apt.doctor.doctor_name,
            "specialization": apt.doctor.specialization
        } if apt and apt.doctor else None,
        "doctor_charges": float(bill.doctor_charges),
        "hospital_charges": float(bill.hospital_charges),
        "additional_expenses": [
            {
                "service_type": e.service_type,
                "service_description": e.service_description,
                "amount": float(e.amount)
            } for e in expenses
        ],
        "additional_expenses_total": float(bill.additional_expenses_total),
        "subtotal": float(bill.subtotal),
        "total_amount": float(bill.total_amount),
        "payment_status": bill.payment_status
    }

@app.get("/api/bills/appointment/{appointment_id}")
def get_bill_by_appointment(appointment_id: int, db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(Bill.appointment_id == appointment_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return get_bill(bill.bill_id, db)

@app.patch("/api/bills/{bill_id}/payment-status")
def update_payment_status(bill_id: int, status_update: PaymentStatusUpdate, db: Session = Depends(get_db)):
    # Find the bill
    bill = db.query(Bill).filter(Bill.bill_id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Update the payment status
    bill.payment_status = status_update.payment_status
    db.commit()
    
    return {"message": f"Payment status updated to {status_update.payment_status}", "success": True}

# =====================================================
# REPORTS ENDPOINTS
# =====================================================
@app.get("/api/reports/summary")
def get_report_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = date.today()
    if not end_date:
        end_date = date.today()
    
    # Total appointments
    total_appointments = db.query(Appointment).filter(
        Appointment.appointment_date.between(start_date, end_date)
    ).count()
    
    # Completed appointments
    completed = db.query(Appointment).filter(
        Appointment.appointment_date.between(start_date, end_date),
        Appointment.status == "Completed"
    ).count()
    
    # Cancelled appointments
    cancelled = db.query(Appointment).filter(
        Appointment.appointment_date.between(start_date, end_date),
        Appointment.status == "Cancelled"
    ).count()
    
    # Total revenue (paid bills)
    total_revenue = db.query(func.sum(Bill.total_amount)).filter(
        Bill.bill_date.between(start_date, end_date),
        Bill.payment_status == "Paid"
    ).scalar() or 0
    
    # Doctor fees collected
    doctor_fees = db.query(func.sum(Bill.doctor_charges)).filter(
        Bill.bill_date.between(start_date, end_date),
        Bill.payment_status == "Paid"
    ).scalar() or 0
    
    # Hospital charges collected
    hospital_charges = db.query(func.sum(Bill.hospital_charges)).filter(
        Bill.bill_date.between(start_date, end_date),
        Bill.payment_status == "Paid"
    ).scalar() or 0
    
    # Additional expenses collected
    additional_expenses = db.query(func.sum(Bill.additional_expenses_total)).filter(
        Bill.bill_date.between(start_date, end_date),
        Bill.payment_status == "Paid"
    ).scalar() or 0
    
    # Pending payments
    pending_amount = db.query(func.sum(Bill.total_amount)).filter(
        Bill.bill_date.between(start_date, end_date),
        Bill.payment_status == "Pending"
    ).scalar() or 0
    
    # New patients registered
    new_patients = db.query(Patient).filter(
        Patient.registration_date.between(start_date, end_date)
    ).count()
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        },
        "appointments": {
            "total": total_appointments,
            "completed": completed,
            "cancelled": cancelled,
            "scheduled": total_appointments - completed - cancelled,
            "completion_rate": round((completed / total_appointments * 100) if total_appointments else 0, 2)
        },
        "revenue": {
            "total_collected": float(total_revenue),
            "doctor_fees": float(doctor_fees),
            "hospital_charges": float(hospital_charges),
            "additional_services": float(additional_expenses),
            "pending_amount": float(pending_amount)
        },
        "patients": {
            "new_registrations": new_patients
        }
    }

@app.get("/api/reports/daily")
def get_daily_report(report_date: Optional[date] = None, db: Session = Depends(get_db)):
    if not report_date:
        report_date = date.today()
    return get_report_summary(start_date=report_date, end_date=report_date, db=db)

@app.get("/api/reports/doctor-wise")
def get_doctor_wise_report(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = date.today()
    if not end_date:
        end_date = date.today()
    
    results = db.query(
        Doctor.doctor_id,
        Doctor.doctor_name,
        Doctor.specialization,
        func.count(Appointment.appointment_id).label("total_appointments"),
        func.sum(Appointment.doctor_charges).label("total_doctor_fees")
    ).join(Appointment, Doctor.doctor_id == Appointment.doctor_id).filter(
        Appointment.appointment_date.between(start_date, end_date)
    ).group_by(Doctor.doctor_id).all()
    
    # Check payment status via vouchers for each doctor
    doctor_reports = []
    for r in results:
        doctor_id = r[0]
        total_fees = float(r[4] or 0)
        
        # Check if there's a paid voucher for this doctor covering this period
        paid_voucher = db.query(Voucher).filter(
            Voucher.doctor_id == doctor_id,
            Voucher.voucher_type == "DOCTOR_PAYMENT",
            Voucher.status == "PAID",
            Voucher.payment_period_start <= start_date,
            Voucher.payment_period_end >= end_date
        ).first()
        
        doctor_reports.append({
            "doctor_id": r[0],
            "doctor_name": r[1],
            "specialization": r[2],
            "total_appointments": r[3],
            "total_doctor_fees": total_fees,
            "payment_status": "Paid" if paid_voucher else "Pending",
            "voucher_number": paid_voucher.voucher_number if paid_voucher else None,
            "paid_at": paid_voucher.paid_at.isoformat() if paid_voucher and paid_voucher.paid_at else None
        })
    
    return doctor_reports

@app.get("/api/reports/service-wise")
def get_service_wise_report(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = date.today()
    if not end_date:
        end_date = date.today()
    
    results = db.query(
        AdditionalExpense.service_type,
        func.count(AdditionalExpense.expense_id).label("count"),
        func.sum(AdditionalExpense.amount).label("total_amount")
    ).filter(
        AdditionalExpense.created_at.between(
            datetime.combine(start_date, datetime.min.time()),
            datetime.combine(end_date, datetime.max.time())
        )
    ).group_by(AdditionalExpense.service_type).all()
    
    return [{
        "service_type": r[0],
        "count": r[1],
        "total_amount": float(r[2] or 0)
    } for r in results]

@app.get("/api/reports/appointments-by-date")
def get_appointments_by_date(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = date.today() - timedelta(days=7)
    if not end_date:
        end_date = date.today()
    
    from datetime import timedelta
    
    results = db.query(
        Appointment.appointment_date,
        func.count(Appointment.appointment_id)
    ).filter(
        Appointment.appointment_date.between(start_date, end_date)
    ).group_by(Appointment.appointment_date).order_by(Appointment.appointment_date).all()
    
    return [{
        "date": r[0].isoformat(),
        "count": r[1]
    } for r in results]

# =====================================================
# AUTH ENDPOINTS
# =====================================================

@app.post("/api/auth/register")
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    existing = db.query(AdminUser).filter(AdminUser.username == admin.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    db_admin = AdminUser(
        username=admin.username,
        password_hash=pwd_context.hash(admin.password),
        full_name=admin.full_name,
        email=admin.email,
        status="Active"
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return {"message": "Admin registered successfully", "admin_id": db_admin.admin_id}

@app.post("/api/auth/test")
def test_login_simple():
    """Simple test endpoint"""
    return {"message": "Test endpoint working"}

@app.post("/api/auth/login-raw")
async def login_raw(request: Request):
    """Raw login endpoint for debugging"""
    try:
        body = await request.json()
        print(f"🔍 Raw request body: {body}")
        
        username = body.get("username")
        password = body.get("password")
        
        print(f"🔍 Username: '{username}' (length: {len(username) if username else 0})")
        print(f"🔍 Password: '{password}' (length: {len(password) if password else 0})")
        
        return {"message": "Raw endpoint working", "username": username, "password_length": len(password) if password else 0}
        
    except Exception as e:
        print(f"❌ Raw endpoint error: {e}")
        return {"error": str(e)}

@app.post("/api/auth/login")
async def login(request: Request):
    """Database-based login endpoint"""
    try:
        # Parse request
        body = await request.json()
        username = body.get("username", "")
        password = body.get("password", "")
        
        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password are required")
        
        # Database authentication
        from .database import SessionLocal
        from .models.user import AdminUser
        from passlib.context import CryptContext
        from datetime import datetime, timedelta
        
        # Create password context for verification
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        db = SessionLocal()
        
        try:
            # Find admin user
            admin = db.query(AdminUser).filter(AdminUser.username == username).first()
            
            if not admin:
                raise HTTPException(status_code=401, detail="Invalid username or password")
            
            # Verify password against database
            if not pwd_context.verify(password, admin.password_hash):
                raise HTTPException(status_code=401, detail="Invalid username or password")
            
            # Check if account is active
            if str(admin.status) != "Active":
                raise HTTPException(status_code=403, detail="Account is inactive")
            
            # Update last login
            admin.last_login = datetime.utcnow()
            db.commit()
            
            # Create token
            expire = datetime.utcnow() + timedelta(minutes=480)  # 8 hours
            token_data = {"sub": admin.username, "admin_id": admin.admin_id, "exp": expire}
            access_token = jwt.encode(token_data, settings.secret_key, algorithm=settings.algorithm)
            
            return {
                "access_token": access_token, 
                "token_type": "bearer",
                "expires_in": 28800
            }
            
        finally:
            db.close()
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

@app.post("/api/auth/reset-password")
async def reset_password(request: Request):
    """Reset admin password"""
    try:
        # Parse request
        body = await request.json()
        username = body.get("username", "")
        new_password = body.get("new_password", "")
        
        if not username or not new_password:
            raise HTTPException(status_code=400, detail="Username and new password are required")
        
        if len(new_password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
        
        # Manual database connection
        from .database import SessionLocal
        from .models.user import AdminUser
        from passlib.context import CryptContext
        
        # Create password context for hashing
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        db = SessionLocal()
        
        try:
            # Find admin user
            admin = db.query(AdminUser).filter(AdminUser.username == username).first()
            
            if not admin:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Hash new password
            new_password_hash = pwd_context.hash(new_password)
            
            # Update password
            admin.password_hash = new_password_hash
            db.commit()
            
            return {"message": "Password reset successfully"}
            
        finally:
            db.close()
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Password reset error: {str(e)}")

# =====================================================
# SERVICES ENDPOINTS
# =====================================================
@app.get("/api/services")
def get_services(db: Session = Depends(get_db)):
    """Get all active services"""
    try:
        from .models.service import Service
        services = db.query(Service).filter(Service.is_active == "Active").all()
        
        result = []
        for service in services:
            result.append({
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "price": float(service.price),
                "category": service.category,
                "created_at": service.created_at.isoformat(),
                "updated_at": service.updated_at.isoformat(),
                "is_active": service.is_active
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching services: {str(e)}")

@app.get("/api/services/{service_id}")
def get_service(service_id: int, db: Session = Depends(get_db)):
    """Get a specific service"""
    try:
        from .models.service import Service
        service = db.query(Service).filter(Service.id == service_id).first()
        
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        return {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "price": float(service.price),
            "category": service.category,
            "created_at": service.created_at.isoformat(),
            "updated_at": service.updated_at.isoformat(),
            "is_active": service.is_active
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching service: {str(e)}")

@app.post("/api/services")
async def create_service(request: Request, db: Session = Depends(get_db)):
    """Create a new service"""
    try:
        from .models.service import Service
        
        body = await request.json()
        name = body.get("name", "")
        description = body.get("description", "")
        price = body.get("price", 0)
        category = body.get("category", "Other")
        
        if not name or price <= 0:
            raise HTTPException(status_code=400, detail="Name and valid price are required")
        
        service = Service(
            name=name,
            description=description,
            price=price,
            category=category
        )
        
        db.add(service)
        db.commit()
        db.refresh(service)
        
        return {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "price": float(service.price),
            "category": service.category,
            "message": "Service created successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating service: {str(e)}")

@app.put("/api/services/{service_id}")
async def update_service(service_id: int, request: Request, db: Session = Depends(get_db)):
    """Update a service"""
    try:
        from .models.service import Service
        
        service = db.query(Service).filter(Service.id == service_id).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        body = await request.json()
        
        if "name" in body:
            service.name = body["name"]
        if "description" in body:
            service.description = body["description"]
        if "price" in body:
            service.price = body["price"]
        if "category" in body:
            service.category = body["category"]
        
        service.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Service updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating service: {str(e)}")

@app.delete("/api/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    """Delete (deactivate) a service"""
    try:
        from .models.service import Service
        
        service = db.query(Service).filter(Service.id == service_id).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        service.is_active = "Inactive"
        service.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Service deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting service: {str(e)}")

# =====================================================
# RUN THE APP
# =====================================================
if __name__ == "__main__":
    import uvicorn
    # Add missing import at top if needed
    from datetime import timedelta
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

# =====================================================
# VOUCHER ENDPOINTS
# =====================================================

def generate_voucher_number(db: Session, voucher_type: str) -> str:
    """Generate unique voucher number"""
    today = date.today()
    prefix = "VCH"
    date_str = today.strftime("%Y%m%d")
    
    # Get the count of vouchers created today
    count = db.query(Voucher).filter(
        func.date(Voucher.created_at) == today
    ).count()
    
    sequence = str(count + 1).zfill(4)
    return f"{prefix}-{date_str}-{sequence}"

@app.get("/api/vouchers/summary")
def get_voucher_summary(db: Session = Depends(get_db)):
    """Get voucher summary statistics"""
    try:
        total_vouchers = db.query(Voucher).count()
        draft_count = db.query(Voucher).filter(Voucher.status == VoucherStatus.DRAFT).count()
        pending_count = db.query(Voucher).filter(Voucher.status == VoucherStatus.PENDING_APPROVAL).count()
        approved_count = db.query(Voucher).filter(Voucher.status == VoucherStatus.APPROVED).count()
        paid_count = db.query(Voucher).filter(Voucher.status == VoucherStatus.PAID).count()
        rejected_count = db.query(Voucher).filter(Voucher.status == VoucherStatus.REJECTED).count()
        
        total_amount = db.query(func.sum(Voucher.amount)).scalar() or 0
        pending_amount = db.query(func.sum(Voucher.amount)).filter(
            Voucher.status.in_([VoucherStatus.PENDING_APPROVAL, VoucherStatus.APPROVED])
        ).scalar() or 0
        
        return VoucherSummary(
            total_vouchers=total_vouchers,
            draft_count=draft_count,
            pending_approval_count=pending_count,
            approved_count=approved_count,
            paid_count=paid_count,
            rejected_count=rejected_count,
            total_amount=total_amount,
            pending_amount=pending_amount
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting voucher summary: {str(e)}")

@app.get("/api/vouchers", response_model=List[VoucherResponse])
def get_vouchers(
    voucher_type: Optional[str] = None,
    status: Optional[str] = None,
    doctor_id: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get vouchers with optional filters"""
    try:
        query = db.query(Voucher).join(Doctor, Voucher.doctor_id == Doctor.doctor_id, isouter=True)
        
        if voucher_type:
            query = query.filter(Voucher.voucher_type == voucher_type)
        if status:
            query = query.filter(Voucher.status == status)
        if doctor_id:
            query = query.filter(Voucher.doctor_id == doctor_id)
        if date_from:
            query = query.filter(Voucher.voucher_date >= date_from)
        if date_to:
            query = query.filter(Voucher.voucher_date <= date_to)
        
        vouchers = query.order_by(Voucher.created_at.desc()).all()
        
        result = []
        for voucher in vouchers:
            voucher_data = VoucherResponse.from_orm(voucher)
            if voucher.doctor:
                voucher_data.doctor_name = voucher.doctor.doctor_name
            result.append(voucher_data)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting vouchers: {str(e)}")

@app.get("/api/vouchers/{voucher_id}", response_model=VoucherResponse)
def get_voucher(voucher_id: int, db: Session = Depends(get_db)):
    """Get voucher by ID"""
    voucher = db.query(Voucher).filter(Voucher.voucher_id == voucher_id).first()
    if not voucher:
        raise HTTPException(status_code=404, detail="Voucher not found")
    
    voucher_data = VoucherResponse.from_orm(voucher)
    if voucher.doctor:
        voucher_data.doctor_name = voucher.doctor.doctor_name
    
    return voucher_data

@app.post("/api/vouchers", response_model=VoucherResponse)
def create_voucher(voucher: VoucherCreate, db: Session = Depends(get_db)):
    """Create new voucher"""
    try:
        # Validate required fields for DOCTOR_PAYMENT vouchers
        if voucher.voucher_type == "DOCTOR_PAYMENT":
            if not voucher.doctor_id:
                raise HTTPException(status_code=400, detail="Doctor selection is required for doctor payment vouchers")
        
        # Validate amount is positive
        if voucher.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")
        
        # Validate doctor exists if doctor_id provided
        if voucher.doctor_id:
            doctor = db.query(Doctor).filter(Doctor.doctor_id == voucher.doctor_id).first()
            if not doctor:
                raise HTTPException(status_code=404, detail="Doctor not found")
            if doctor.status != "Active":
                raise HTTPException(status_code=400, detail="Selected doctor is not active")
        
        # Generate voucher number
        voucher_number = generate_voucher_number(db, voucher.voucher_type)
        
        # Create voucher
        db_voucher = Voucher(
            voucher_number=voucher_number,
            voucher_type=voucher.voucher_type,
            doctor_id=voucher.doctor_id,
            payment_period_start=voucher.payment_period_start,
            payment_period_end=voucher.payment_period_end,
            amount=voucher.amount,
            description=voucher.description,
            voucher_date=voucher.voucher_date,
            status=VoucherStatus.DRAFT,
            created_by=1  # TODO: Get from JWT token
        )
        
        db.add(db_voucher)
        db.commit()
        db.refresh(db_voucher)
        
        voucher_data = VoucherResponse.from_orm(db_voucher)
        if db_voucher.doctor:
            voucher_data.doctor_name = db_voucher.doctor.doctor_name
        
        return voucher_data
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating voucher: {str(e)}")

@app.post("/api/vouchers/{voucher_id}/submit")
def submit_voucher_for_approval(voucher_id: int, db: Session = Depends(get_db)):
    """Submit voucher for approval"""
    try:
        voucher = db.query(Voucher).filter(Voucher.voucher_id == voucher_id).first()
        if not voucher:
            raise HTTPException(status_code=404, detail="Voucher not found")
        
        if not voucher.can_be_submitted:
            raise HTTPException(status_code=400, detail="Voucher cannot be submitted for approval")
        
        voucher.status = VoucherStatus.PENDING_APPROVAL
        voucher.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Voucher submitted for approval successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error submitting voucher: {str(e)}")

@app.post("/api/vouchers/{voucher_id}/approve")
def approve_voucher(voucher_id: int, db: Session = Depends(get_db)):
    """Approve voucher"""
    try:
        voucher = db.query(Voucher).filter(Voucher.voucher_id == voucher_id).first()
        if not voucher:
            raise HTTPException(status_code=404, detail="Voucher not found")
        
        if not voucher.can_be_approved:
            raise HTTPException(status_code=400, detail="Voucher cannot be approved")
        
        voucher.status = VoucherStatus.APPROVED
        voucher.approved_by = 1  # TODO: Get from JWT token
        voucher.approved_at = datetime.utcnow()
        voucher.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Voucher approved successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error approving voucher: {str(e)}")

@app.post("/api/vouchers/{voucher_id}/reject")
def reject_voucher(voucher_id: int, db: Session = Depends(get_db)):
    """Reject voucher"""
    try:
        voucher = db.query(Voucher).filter(Voucher.voucher_id == voucher_id).first()
        if not voucher:
            raise HTTPException(status_code=404, detail="Voucher not found")
        
        if not voucher.can_be_approved:
            raise HTTPException(status_code=400, detail="Voucher cannot be rejected")
        
        voucher.status = VoucherStatus.REJECTED
        voucher.approved_by = 1  # TODO: Get from JWT token
        voucher.approved_at = datetime.utcnow()
        voucher.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Voucher rejected successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error rejecting voucher: {str(e)}")

@app.post("/api/vouchers/{voucher_id}/pay")
def mark_voucher_as_paid(voucher_id: int, db: Session = Depends(get_db)):
    """Mark voucher as paid"""
    try:
        voucher = db.query(Voucher).filter(Voucher.voucher_id == voucher_id).first()
        if not voucher:
            raise HTTPException(status_code=404, detail="Voucher not found")
        
        if not voucher.can_be_paid:
            raise HTTPException(status_code=400, detail="Voucher cannot be marked as paid")
        
        voucher.status = VoucherStatus.PAID
        voucher.paid_at = datetime.utcnow()
        voucher.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Voucher marked as paid successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error marking voucher as paid: {str(e)}")

@app.delete("/api/vouchers/{voucher_id}")
def delete_voucher(voucher_id: int, db: Session = Depends(get_db)):
    """Delete voucher (allowed for DRAFT, REJECTED, and PAID status)"""
    try:
        voucher = db.query(Voucher).filter(Voucher.voucher_id == voucher_id).first()
        if not voucher:
            raise HTTPException(status_code=404, detail="Voucher not found")
        
        # Allow deletion of DRAFT, REJECTED, and PAID vouchers
        if voucher.status not in [VoucherStatus.DRAFT, VoucherStatus.REJECTED, VoucherStatus.PAID]:
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot delete voucher with status '{voucher.status}'. Only DRAFT, REJECTED, and PAID vouchers can be deleted."
            )
        
        # Store voucher number for response
        voucher_number = voucher.voucher_number
        
        # Delete the voucher
        db.delete(voucher)
        db.commit()
        
        return {"message": f"Voucher {voucher_number} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting voucher: {str(e)}")