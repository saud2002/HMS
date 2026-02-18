# HMS Database Connection Troubleshooting Guide

## Issue
Data is not loading from the database in the HMS frontend.

## Diagnosis Results

### ✅ What's Working
1. **MySQL Server**: Running on port 3306
2. **Backend Server**: Running on port 8000
3. **Database Connection**: Successfully connected to `hms` database
4. **Database Tables**: All required tables exist (13 tables found)
5. **Sample Data**: Database has 1 patient, 1 doctor, 4 services
6. **API Endpoints**: All API endpoints responding correctly
   - `/api/health` - ✅ Working
   - `/api/dashboard/stats` - ✅ Working
   - `/api/patients` - ✅ Working (returns 1 patient)
   - `/api/doctors` - ✅ Working (returns 1 doctor)
   - `/api/services` - ✅ Working (returns 4 services)

### 🔍 Possible Issues

The backend and database are working correctly. The issue is likely on the frontend side:

## Troubleshooting Steps

### Step 1: Test Frontend Connection
Open this URL in your browser:
```
http://localhost:8000/test_connection.html
```

This diagnostic page will:
- Test all API endpoints
- Show detailed error messages
- Display console logs
- Help identify where the connection fails

### Step 2: Check Browser Console
1. Open your browser (Chrome/Edge/Firefox)
2. Press `F12` to open Developer Tools
3. Go to the "Console" tab
4. Look for any error messages (red text)
5. Common errors to look for:
   - CORS errors
   - 401 Unauthorized errors
   - Network errors
   - JavaScript errors

### Step 3: Check Network Tab
1. In Developer Tools, go to "Network" tab
2. Refresh the page
3. Look for API calls (should start with `/api/`)
4. Check if they're:
   - ✅ Status 200 (success)
   - ❌ Status 401 (authentication issue)
   - ❌ Status 404 (endpoint not found)
   - ❌ Status 500 (server error)

### Step 4: Check Authentication
The HMS system requires authentication. Make sure:

1. You're logged in:
   ```
   http://localhost:8000/login.html
   ```

2. Check if token exists in browser:
   - Open Console (F12)
   - Type: `localStorage.getItem('access_token')`
   - Should return a token string
   - If null, you need to log in

3. Default admin credentials (if not changed):
   - Username: `admin`
   - Password: Check `backend/create_admin.py` for default password

### Step 5: Clear Browser Cache
Sometimes old cached files cause issues:

1. Press `Ctrl + Shift + Delete`
2. Select "Cached images and files"
3. Click "Clear data"
4. Refresh the page (`Ctrl + F5`)

### Step 6: Check for JavaScript Errors
1. Open any HMS page (e.g., patients.html)
2. Open Console (F12)
3. Look for errors like:
   - "API is not defined"
   - "Cannot read property of undefined"
   - "Failed to fetch"

## Quick Tests

### Test 1: Direct API Call
Open browser console and run:
```javascript
fetch('/api/patients')
  .then(r => r.json())
  .then(data => console.log('Patients:', data))
  .catch(err => console.error('Error:', err));
```

### Test 2: Check API Object
Open browser console and run:
```javascript
console.log('API object:', window.API);
console.log('Patients API:', window.API?.Patients);
```

### Test 3: Manual Patient Load
Open patients.html and run in console:
```javascript
API.Patients.getAll()
  .then(patients => console.log('Loaded patients:', patients))
  .catch(error => console.error('Error loading patients:', error));
```

## Common Solutions

### Solution 1: Authentication Issue
If you see 401 errors or redirects to login:

1. Go to login page: `http://localhost:8000/login.html`
2. Log in with admin credentials
3. Try accessing the page again

### Solution 2: CORS Issue
If you see CORS errors in console:

1. Make sure you're accessing via `http://localhost:8000` (not file://)
2. Check backend CORS settings in `backend/app/config.py`
3. Restart backend server

### Solution 3: Script Loading Order
If API is undefined:

1. Check that scripts are loaded in correct order in HTML:
   ```html
   <script src="/static/js/data.js"></script>
   <script src="/static/js/common.js"></script>
   <script src="/static/js/api.js"></script>
   ```

### Solution 4: Create Admin User
If you can't log in:

```bash
cd backend
python create_admin.py
```

This will create/reset the admin user.

## Verification Commands

### Check if backend is running:
```bash
netstat -ano | findstr :8000
```

### Check if MySQL is running:
```bash
netstat -ano | findstr :3306
```

### Test database connection:
```bash
cd backend
python test_db_connection.py
```

### Test API endpoints:
```bash
cd backend
python test_api.py
```

## Files Created for Troubleshooting

1. `backend/test_db_connection.py` - Tests database connection and tables
2. `backend/test_api.py` - Tests all API endpoints
3. `frontend/test_connection.html` - Browser-based connection test

## Next Steps

1. Open `http://localhost:8000/test_connection.html` in your browser
2. Click all the test buttons
3. Check the results and console logs
4. Report back which tests fail and what error messages you see

## Contact Information

If the issue persists, provide:
1. Screenshot of browser console (F12 → Console tab)
2. Screenshot of network tab showing failed requests
3. Results from test_connection.html
4. Any error messages you see

---

**Note**: The backend and database are confirmed working. The issue is most likely:
- Authentication (not logged in)
- Browser cache (old files)
- JavaScript errors in console
- CORS or network issues
