# ============== app/routers/appointments.py ==============
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date, datetime
from app.database import get_db
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse

router = APIRouter()

def generate_appointment_id(db: Session) -> str:
    last = db.query(Appointment).order_by(Appointment.id.desc()).first()
    num = (last.id + 1) if last else 1
    return f"APT-{num:05d}"

@router.get("/", response_model=List[dict])
def get_appointments(
    skip: int = 0, limit: int = 100,
    status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    doctor_id: Optional[int] = None,
    patient_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Appointment).options(
        joinedload(Appointment.patient),
        joinedload(Appointment.doctor)
    )
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
        apt_dict = {
            "id": apt.id, "appointment_id": apt.appointment_id,
            "patient_id": apt.patient_id, "doctor_id": apt.doctor_id,
            "appointment_date": apt.appointment_date.isoformat(),
            "appointment_time": apt.appointment_time.isoformat(),
            "duration_minutes": apt.duration_minutes, "status": apt.status,
            "appointment_type": apt.appointment_type, "reason": apt.reason,
            "notes": apt.notes, "diagnosis": apt.diagnosis, "prescription": apt.prescription,
            "patient_name": f"{apt.patient.first_name} {apt.patient.last_name}" if apt.patient else None,
            "doctor_name": f"Dr. {apt.doctor.first_name} {apt.doctor.last_name}" if apt.doctor else None,
            "specialization": apt.doctor.specialization if apt.doctor else None,
            "created_at": apt.created_at.isoformat() if apt.created_at else None
        }
        result.append(apt_dict)
    return result

@router.get("/today")
def get_today_appointments(db: Session = Depends(get_db)):
    return get_appointments(date_from=date.today(), date_to=date.today(), db=db)

@router.get("/{appointment_id}")
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    apt = db.query(Appointment).options(
        joinedload(Appointment.patient), joinedload(Appointment.doctor)
    ).filter(Appointment.id == appointment_id).first()
    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {
        "id": apt.id, "appointment_id": apt.appointment_id,
        "patient_id": apt.patient_id, "doctor_id": apt.doctor_id,
        "appointment_date": apt.appointment_date.isoformat(),
        "appointment_time": apt.appointment_time.isoformat(),
        "status": apt.status, "appointment_type": apt.appointment_type,
        "reason": apt.reason, "notes": apt.notes, "diagnosis": apt.diagnosis,
        "prescription": apt.prescription,
        "patient_name": f"{apt.patient.first_name} {apt.patient.last_name}" if apt.patient else None,
        "doctor_name": f"Dr. {apt.doctor.first_name} {apt.doctor.last_name}" if apt.doctor else None
    }

@router.post("/", response_model=dict)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    # Verify patient and doctor exist
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db_apt = Appointment(**appointment.model_dump(), appointment_id=generate_appointment_id(db))
    db.add(db_apt)
    db.commit()
    db.refresh(db_apt)
    return {"id": db_apt.id, "appointment_id": db_apt.appointment_id, "message": "Appointment created"}

@router.put("/{appointment_id}")
def update_appointment(appointment_id: int, appointment: AppointmentUpdate, db: Session = Depends(get_db)):
    db_apt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for key, value in appointment.model_dump(exclude_unset=True).items():
        setattr(db_apt, key, value)
    db.commit()
    return {"message": "Appointment updated successfully"}

@router.patch("/{appointment_id}/status")
def update_status(appointment_id: int, status: str, db: Session = Depends(get_db)):
    db_apt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db_apt.status = status
    db.commit()
    return {"message": f"Status updated to {status}"}

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_apt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(db_apt)
    db.commit()
    return {"message": "Appointment deleted"}


# ============== app/routers/reports.py ==============
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from app.database import get_db
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.doctor import Doctor

router = APIRouter()

@router.get("/summary")
def get_summary(
    start_date: date = Query(default=None),
    end_date: date = Query(default=None),
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    total_appointments = db.query(Appointment).filter(
        Appointment.appointment_date.between(start_date, end_date)
    ).count()
    
    completed = db.query(Appointment).filter(
        Appointment.appointment_date.between(start_date, end_date),
        Appointment.status == "completed"
    ).count()
    
    cancelled = db.query(Appointment).filter(
        Appointment.appointment_date.between(start_date, end_date),
        Appointment.status == "cancelled"
    ).count()
    
    new_patients = db.query(Patient).filter(
        func.date(Patient.created_at).between(start_date, end_date)
    ).count()
    
    return {
        "period": {"start": start_date.isoformat(), "end": end_date.isoformat()},
        "total_appointments": total_appointments,
        "completed_appointments": completed,
        "cancelled_appointments": cancelled,
        "new_patients": new_patients,
        "completion_rate": round((completed/total_appointments*100) if total_appointments else 0, 1)
    }

@router.get("/appointments-by-doctor")
def appointments_by_doctor(
    start_date: date = Query(default=None),
    end_date: date = Query(default=None),
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    results = db.query(
        Doctor.id, Doctor.first_name, Doctor.last_name, Doctor.specialization,
        func.count(Appointment.id).label("total"),
        func.sum(func.case((Appointment.status == "completed", 1), else_=0)).label("completed")
    ).join(Appointment, Doctor.id == Appointment.doctor_id).filter(
        Appointment.appointment_date.between(start_date, end_date)
    ).group_by(Doctor.id).all()
    
    return [{
        "doctor_id": r[0], "name": f"Dr. {r[1]} {r[2]}",
        "specialization": r[3], "total_appointments": r[4], "completed": r[5] or 0
    } for r in results]

@router.get("/appointments-by-date")
def appointments_by_date(
    start_date: date = Query(default=None),
    end_date: date = Query(default=None),
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = date.today() - timedelta(days=7)
    if not end_date:
        end_date = date.today()
    
    results = db.query(
        Appointment.appointment_date, func.count(Appointment.id)
    ).filter(
        Appointment.appointment_date.between(start_date, end_date)
    ).group_by(Appointment.appointment_date).order_by(Appointment.appointment_date).all()
    
    return [{"date": r[0].isoformat(), "count": r[1]} for r in results]


# ============== app/routers/auth.py ==============
# This auth router is not used in the current monolithic setup
# The main.py file handles authentication directly