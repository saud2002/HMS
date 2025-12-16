# 🚀 HMS Quick Start Guide

Your Hospital Management System is ready! Here's how to get it running in 5 minutes.

## ✅ System Status: WORKING ✅

The core system has been tested and is fully functional.

## 🏃‍♂️ Quick Start (5 Minutes)

### 1. Install Dependencies (Windows)
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements-minimal.txt
```

### 2. Configure Database
```cmd
copy .env.example .env
```
Edit `.env` file with your MySQL credentials:
```
DATABASE_URL=mysql+pymysql://root:@localhost:3306/hms
```

### 3. Initialize Database
```cmd
python init_database.py
```

### 4. Test System
```cmd
python quick_test.py
```

### 5. Start Application
```cmd
python start.py
```

### 6. Access Your HMS
- **API Server:** http://127.0.0.1:8000 (or http://localhost:8000)
- **API Docs:** http://127.0.0.1:8000/docs
- **Frontend:** Open `frontend/index.html` in your browser
- **Login:** username: `admin`, password: `admin123`

## 🎯 What You Get

### ✅ Complete Features
- **Patient Registration** with validation
- **Doctor Management** with specializations
- **Appointment Booking** with token system
- **Billing System** with itemized charges
- **Reports & Analytics** with date filtering
- **User Authentication** with JWT security

### ✅ Database Features
- **Proper relationships** and constraints
- **Audit trail** for all operations
- **Token counter** for queue management
- **Views and procedures** for reporting

### ✅ API Features
- **RESTful API** with full CRUD operations
- **Data validation** with Pydantic
- **Error handling** and logging
- **Interactive documentation** at `/docs`

## 📱 Using the System

### Patient Registration
1. Go to Patients page
2. Click "Add New Patient"
3. Fill required information (Name, Age, Phone, Gender, NIC)
4. System validates and saves

### Appointment Booking
1. Go to Appointments page
2. Select patient (search by name/NIC)
3. Choose doctor and date
4. System generates token number automatically
5. Bill is created instantly

### Billing & Services
1. View appointment details
2. Add additional services (Dressing, Scanning, etc.)
3. Bill updates automatically
4. Mark payment status

### Reports
1. Go to Reports page
2. Select date range
3. View doctor-wise or hospital summary
4. Print reports

## 🔧 Troubleshooting

### Database Issues
- **MySQL not running:** Start XAMPP or MySQL service
- **Connection failed:** Check credentials in `.env`
- **Tables not created:** Run `python init_database.py`

### Installation Issues
- **Package conflicts:** Use `requirements-minimal.txt`
- **Permission errors:** Run as Administrator
- **Python version:** Use Python 3.8-3.11

### Application Issues
- **Port in use:** Change port in `start.py`
- **Import errors:** Check virtual environment activation
- **Frontend not loading:** Open `frontend/index.html` directly

## 🎉 Success Indicators

You'll know it's working when:
- ✅ `python quick_test.py` shows all tests passed
- ✅ API docs load at http://localhost:8000/docs
- ✅ You can login with admin/admin123
- ✅ Frontend shows dashboard with stats

## 📞 Next Steps

1. **Customize hospital info** in `backend/app/config.py`
2. **Add your doctors** in the Doctors page
3. **Register patients** and start booking appointments
4. **Generate reports** to track performance

## 🏥 Your HMS is Production Ready!

The system includes:
- **Enterprise-grade database design**
- **Proper security and validation**
- **Complete audit trail**
- **Scalable architecture**
- **Professional UI/UX**

**Start managing your hospital efficiently! 🎯**