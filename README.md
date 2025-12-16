# 🏥 Hospital Management System (HMS)

A comprehensive Hospital Management System built with FastAPI backend and vanilla HTML/CSS/JavaScript frontend. Designed for private medical centers to manage patients, doctors, appointments, billing, and generate reports.

## ✨ Features

### 👥 Patient Management
- Patient registration with validation
- Search and update patient records
- NIC and phone number validation
- Patient history tracking

### 👨‍⚕️ Doctor Management
- Doctor profile management
- Specialization tracking
- Consultation charges management
- Active/Inactive status control

### 📅 Appointment System
- Token-based queue management
- Automatic token number generation
- Doctor-wise appointment scheduling
- Status tracking (Scheduled/Completed/Cancelled)

### 💰 Billing System
- Itemized billing with multiple charge types
- Doctor consultation fees
- Hospital charges
- Additional services (Dressing, Scanning, Blood Testing, ECG, Other)
- Payment status tracking
- Bill generation and printing

### 📊 Reporting
- Daily doctor reports
- Hospital revenue reports
- Service-wise analytics
- Date range filtering
- PDF export capability

### 🔐 Security
- Admin authentication system
- JWT token-based security
- Password hashing with bcrypt
- Audit trail logging

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 5.7+ or 8.0+
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hospital-management-system
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env file with your database credentials
   # DATABASE_URL=mysql+pymysql://username:password@localhost:3306/hms
   ```

5. **Initialize database**
   ```bash
   python init_database.py
   ```

6. **Start the application**
   ```bash
   python start.py
   ```

7. **Access the application**
   - Frontend: Open `frontend/index.html` in your browser
   - API Documentation: http://localhost:8000/docs
   - API Base URL: http://localhost:8000/api

### Default Login
- **Username:** admin
- **Password:** admin123

## 📁 Project Structure

```
hospital-management-system/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── routers/         # API route handlers (optional)
│   │   ├── services/        # Business logic
│   │   ├── database.py      # Database configuration
│   │   ├── config.py        # Application settings
│   │   └── main.py          # FastAPI application
│   ├── init_database.py     # Database initialization
│   ├── start.py            # Application startup script
│   ├── requirements.txt     # Python dependencies
│   └── .env.example        # Environment template
├── frontend/
│   ├── css/
│   │   └── styles.css      # Application styles
│   ├── js/
│   │   ├── api.js          # API service layer
│   │   ├── common.js       # Common utilities
│   │   └── data.js         # Data management
│   ├── index.html          # Dashboard
│   ├── patients.html       # Patient management
│   ├── doctors.html        # Doctor management
│   ├── appointments.html   # Appointment booking
│   └── reports.html        # Reports and analytics
└── README.md
```

## 🗄️ Database Schema

The system uses a comprehensive MySQL database with the following key tables:

- **admin_users** - System administrators
- **patients** - Patient records
- **doctors** - Doctor profiles
- **appointments** - Appointment bookings
- **bills** - Billing information
- **additional_expenses** - Additional services
- **token_counter** - Token number management
- **system_logs** - Audit trail

### Key Features:
- Proper foreign key relationships
- Check constraints for data validation
- Indexes for performance optimization
- Views for complex reporting queries
- Stored procedures for business logic

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/hms

# Security
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=480

# Application
DEBUG=false
HOSPITAL_NAME=Your Hospital Name
```

### Database Setup

1. Create MySQL database:
   ```sql
   CREATE DATABASE hms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Run initialization script:
   ```bash
   python init_database.py
   ```

## 📖 API Documentation

### Authentication
```http
POST /api/auth/login
POST /api/auth/register
```

### Patients
```http
GET    /api/patients
POST   /api/patients
GET    /api/patients/{id}
PUT    /api/patients/{id}
DELETE /api/patients/{id}
GET    /api/patients/nic/{nic}
```

### Doctors
```http
GET    /api/doctors
POST   /api/doctors
GET    /api/doctors/{id}
PUT    /api/doctors/{id}
DELETE /api/doctors/{id}
GET    /api/doctors/specializations
```

### Appointments
```http
GET    /api/appointments
POST   /api/appointments
GET    /api/appointments/{id}
PATCH  /api/appointments/{id}/status
DELETE /api/appointments/{id}
GET    /api/appointments/today
```

### Bills & Expenses
```http
GET    /api/bills
GET    /api/bills/{id}
PATCH  /api/bills/{id}/payment-status
POST   /api/expenses
DELETE /api/expenses/{id}
```

### Reports
```http
GET    /api/reports/summary
GET    /api/reports/daily
GET    /api/reports/doctor-wise
GET    /api/reports/service-wise
```

## 🎯 Usage Guide

### 1. Patient Registration
1. Navigate to Patients page
2. Click "Add New Patient"
3. Fill in required information
4. System validates NIC and phone number
5. Patient gets unique ID automatically

### 2. Doctor Management
1. Go to Doctors page
2. Add doctor with unique ID
3. Set specialization and consultation charges
4. Manage active/inactive status

### 3. Appointment Booking
1. Open Appointments page
2. Select patient (search by name/NIC)
3. Choose doctor and date
4. System generates unique token number
5. Bill is created automatically

### 4. Additional Services
1. Open appointment details
2. Add services (Dressing, Scanning, etc.)
3. Bill updates automatically
4. Track payment status

### 5. Reports Generation
1. Visit Reports page
2. Select report type and date range
3. View detailed analytics
4. Print or export reports

## 🔒 Security Features

- **Authentication:** JWT-based admin authentication
- **Password Security:** Bcrypt hashing
- **Input Validation:** Comprehensive data validation
- **SQL Injection Protection:** SQLAlchemy ORM
- **Audit Trail:** Complete system logging
- **CORS Protection:** Configurable origins

## 🚀 Deployment

### Production Setup

1. **Environment Configuration**
   ```bash
   # Set production environment variables
   export DATABASE_URL="mysql+pymysql://user:pass@host:port/db"
   export SECRET_KEY="production-secret-key"
   export DEBUG=false
   ```

2. **Database Migration**
   ```bash
   python init_database.py
   ```

3. **Start with Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

4. **Nginx Configuration** (optional)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location /api {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location / {
           root /path/to/frontend;
           index index.html;
       }
   }
   ```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the database schema in `init_database.py`

## 🎉 Acknowledgments

- FastAPI for the excellent web framework
- SQLAlchemy for robust database ORM
- Pydantic for data validation
- MySQL for reliable database engine

---

**Built with ❤️ for healthcare management**