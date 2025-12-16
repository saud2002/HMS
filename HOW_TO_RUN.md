# 🚀 How to Run Your HMS System

## 🎯 **Quick Start (Easiest Method)**

### **Option 1: Simple Double-Click Method**
1. **Start Backend:**
   - Double-click `start_hms_complete.bat`
   - This will start backend and open frontend automatically

2. **Login:**
   - Username: `admin`
   - Password: `admin123`

---

## 🔧 **Manual Method (More Control)**

### **Step 1: Start Backend Server**
```cmd
cd backend
venv\Scripts\activate
python start.py
```
Keep this terminal open - you'll see API logs here.

### **Step 2: Open Frontend**
Choose one of these methods:

**Method A: Direct File Opening**
- Navigate to your project folder
- Double-click `frontend/index.html`

**Method B: Using Python Server**
```cmd
cd frontend
python start_frontend.py
```
This opens frontend at http://127.0.0.1:3000

---

## 🌐 **Advanced: Both Servers Method**

### **Run Both with One Command:**
```cmd
python start_both_servers.py
```

This will:
- ✅ Start backend server (port 8000)
- ✅ Start frontend server (port 3000)  
- ✅ Open browser automatically
- ✅ Show all URLs and login info

---

## 📱 **Access Points**

Once running, you can access:

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://127.0.0.1:3000 | Main HMS Application |
| **Backend API** | http://127.0.0.1:8000 | API Server |
| **API Docs** | http://127.0.0.1:8000/docs | Interactive API Documentation |
| **Health Check** | http://127.0.0.1:8000/api/health | Server Status |

---

## 🔑 **Login Credentials**

- **Username:** admin
- **Password:** admin123

---

## 🏥 **HMS Features Available**

Once logged in, you can:

### 📊 **Dashboard**
- View hospital statistics
- Quick action buttons
- Recent activity feed

### 👥 **Patient Management**
- Register new patients
- Search existing patients
- Update patient information
- View patient history

### 👨‍⚕️ **Doctor Management**
- Add new doctors
- Set specializations
- Manage consultation charges
- Active/Inactive status

### 📅 **Appointment System**
- Book new appointments
- Automatic token generation
- View today's appointments
- Update appointment status

### 💰 **Billing System**
- Generate itemized bills
- Add additional services:
  - Dressing
  - Scanning (CT, MRI, X-Ray)
  - Blood Testing
  - ECG
  - Other Services
- Track payment status
- Print bills

### 📈 **Reports & Analytics**
- Daily doctor reports
- Hospital revenue reports
- Service-wise analytics
- Date range filtering
- Export capabilities

---

## 🔧 **Troubleshooting**

### **Backend Won't Start**
```cmd
cd backend
python quick_test.py
```

### **Frontend Can't Connect**
- Check if backend is running at http://127.0.0.1:8000
- Verify API URL in `frontend/js/api.js`

### **Database Issues**
```cmd
cd backend
python create_admin.py
```

### **Port Conflicts**
- Backend uses port 8000
- Frontend uses port 3000
- Change ports if needed in the scripts

---

## 🎉 **You're All Set!**

Your Hospital Management System is now ready for production use. The system includes:

- ✅ **Professional UI/UX**
- ✅ **Complete patient workflow**
- ✅ **Secure authentication**
- ✅ **Comprehensive reporting**
- ✅ **Real-time data updates**
- ✅ **Print-ready documents**

**Start managing your hospital efficiently! 🏥**