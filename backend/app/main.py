# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import patients, doctors, appointments, reports, auth
from app.config import settings

# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Hospital Management System API",
    description="API for managing patients, doctors, appointments, and reports",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration - Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(patients.router, prefix="/api/patients", tags=["Patients"])
app.include_router(doctors.router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(appointments.router, prefix="/api/appointments", tags=["Appointments"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "HMS API is running"}

# Dashboard statistics endpoint
@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    from app.database import SessionLocal
    from app.models.patient import Patient
    from app.models.doctor import Doctor
    from app.models.appointment import Appointment
    from datetime import date
    
    db = SessionLocal()
    try:
        total_patients = db.query(Patient).count()
        total_doctors = db.query(Doctor).filter(Doctor.is_active == True).count()
        today_appointments = db.query(Appointment).filter(
            Appointment.appointment_date == date.today()
        ).count()
        pending_appointments = db.query(Appointment).filter(
            Appointment.status == "scheduled"
        ).count()
        
        return {
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "today_appointments": today_appointments,
            "pending_appointments": pending_appointments
        }
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)