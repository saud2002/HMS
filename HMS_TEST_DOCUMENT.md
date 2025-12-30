# Hospital Management System (HMS) - Complete Test Document

## Test Environment Setup
- **Browser**: Chrome/Firefox/Edge (latest version)
- **Server**: Backend running on http://127.0.0.1:8000
- **Database**: MySQL local database
- **Test Data**: Ensure you have sample patients, doctors, and appointments

---

## 1. LOGIN PAGE TESTING

### 1.1 Login Functionality
**Test Cases:**
- [ ] **Valid Login**: Enter correct username/password → Should redirect to dashboard
- [ ] **Invalid Login**: Enter wrong credentials → Should show error message
- [ ] **Empty Fields**: Submit without username/password → Should show validation error
- [ ] **Remember Me Checked**: Login with remember me → Should stay logged in after browser restart
- [ ] **Remember Me Unchecked**: Login without remember me → Should logout after browser close

### 1.2 Password Visibility Toggle
**Test Cases:**
- [ ] **Show Password**: Click eye icon → Password should become visible
- [ ] **Hide Password**: Click eye icon again → Password should be hidden
- [ ] **Icon Changes**: Eye icon should change between open/closed states

### 1.3 Forgot Password
**Test Cases:**
- [ ] **Open Modal**: Click "Forgot password?" → Modal should open
- [ ] **Username Field**: Enter username → Should accept input
- [ ] **New Password Field**: Enter new password → Should accept input with eye toggle
- [ ] **Confirm Password Field**: Enter matching password → Should accept input with eye toggle
- [ ] **Password Mismatch**: Enter different passwords → Should show error
- [ ] **Reset Success**: Valid data → Should show success message
- [ ] **Close Modal**: Click cancel/X → Modal should close

### 1.4 Auto-fill and Focus
**Test Cases:**
- [ ] **Username Auto-fill**: If remembered → Username should be pre-filled
- [ ] **Focus Management**: Page load → Username field should be focused (or password if username filled)

---

## 2. DASHBOARD PAGE TESTING

### 2.1 Statistics Cards
**Test Cases:**
- [ ] **Total Patients**: Card shows correct patient count
- [ ] **Total Doctors**: Card shows correct active doctor count
- [ ] **Today's Appointments**: Card shows correct appointment count for today
- [ ] **Pending Bills**: Card shows correct pending bill count
- [ ] **Today's Revenue**: Card shows correct revenue for paid bills today

### 2.2 Navigation
**Test Cases:**
- [ ] **Sidebar Toggle**: Click hamburger menu → Sidebar should collapse/expand
- [ ] **Menu Items**: Click each menu item → Should navigate to correct page
- [ ] **Active State**: Current page should be highlighted in sidebar
- [ ] **User Profile**: Click profile → Should show user menu
- [ ] **Logout**: Click logout → Should return to login page

### 2.3 Real-time Updates
**Test Cases:**
- [ ] **Date/Time**: Top bar should show current date and time
- [ ] **Auto Refresh**: Statistics should update when data changes

---

## 3. PATIENTS PAGE TESTING

### 3.1 Patient List Display
**Test Cases:**
- [ ] **Load Patients**: Page should display all patients in table
- [ ] **Patient Data**: Each row should show ID, name, age, phone, NIC, gender
- [ ] **Empty State**: If no patients → Should show "No patients found"
- [ ] **Loading State**: While loading → Should show loading indicator

### 3.2 Search Functionality
**Test Cases:**
- [ ] **Search by Name**: Type patient name → Should filter results
- [ ] **Search by NIC**: Type NIC number → Should filter results
- [ ] **Search by Phone**: Type phone number → Should filter results
- [ ] **Clear Search**: Clear search box → Should show all patients
- [ ] **No Results**: Search non-existent data → Should show "No patients found"

### 3.3 Add New Patient
**Test Cases:**
- [ ] **Open Modal**: Click "Add New Patient" → Modal should open
- [ ] **Auto-generate ID**: Patient ID should be auto-generated (P001, P002, etc.)
- [ ] **Required Fields**: Try to save without required fields → Should show validation errors
- [ ] **Valid Data**: Fill all fields correctly → Should save successfully
- [ ] **Duplicate NIC**: Try to add patient with existing NIC → Should show error
- [ ] **Phone Validation**: Enter invalid phone format → Should show validation error
- [ ] **Age Calculation**: Enter birth date → Age should be calculated automatically
- [ ] **Cancel**: Click cancel → Modal should close without saving

### 3.4 Edit Patient
**Test Cases:**
- [ ] **Open Edit**: Click edit icon → Modal should open with existing data
- [ ] **Pre-filled Data**: All fields should contain current patient data
- [ ] **Update Data**: Change information → Should save successfully
- [ ] **Validation**: Invalid data → Should show appropriate errors
- [ ] **Cancel Edit**: Click cancel → Should not save changes

### 3.5 Delete Patient
**Test Cases:**
- [ ] **Delete Confirmation**: Click delete icon → Should show confirmation dialog
- [ ] **Confirm Delete**: Click yes → Patient should be deleted
- [ ] **Cancel Delete**: Click no → Patient should remain
- [ ] **Constraint Check**: Try to delete patient with appointments → Should show error

---

## 4. DOCTORS PAGE TESTING

### 4.1 Doctor List Display
**Test Cases:**
- [ ] **Load Doctors**: Page should display all doctors (active and inactive)
- [ ] **Doctor Data**: Each row should show ID, name, specialization, fee, status
- [ ] **Status Badges**: Active (green), Inactive (red) badges should display correctly
- [ ] **Action Buttons**: Edit (blue), Deactivate/Activate (orange/green), Delete (red) icons

### 4.2 Search and Filter
**Test Cases:**
- [ ] **Search by Name**: Type doctor name → Should filter results
- [ ] **Search by Specialization**: Type specialization → Should filter results
- [ ] **Filter All**: Select "All Doctors" → Should show all doctors
- [ ] **Filter Active**: Select "Active Only" → Should show only active doctors
- [ ] **Filter Inactive**: Select "Inactive Only" → Should show only inactive doctors
- [ ] **Combined Filter**: Use search + status filter → Should apply both filters

### 4.3 Add New Doctor
**Test Cases:**
- [ ] **Open Modal**: Click "Add New Doctor" → Modal should open
- [ ] **Auto-generate ID**: Doctor ID should be auto-generated (DR001, DR002, etc.)
- [ ] **Required Fields**: Try to save without required fields → Should show validation errors
- [ ] **Valid Data**: Fill all fields correctly → Should save successfully
- [ ] **Duplicate ID**: System should prevent duplicate doctor IDs
- [ ] **Fee Validation**: Enter negative fee → Should show validation error
- [ ] **Status Selection**: Should default to "Active"

### 4.4 Edit Doctor
**Test Cases:**
- [ ] **Open Edit**: Click edit icon → Modal should open with existing data
- [ ] **Pre-filled Data**: All fields should contain current doctor data
- [ ] **Update Data**: Change information → Should save successfully
- [ ] **Status Change**: Change status in edit modal → Should update correctly

### 4.5 Deactivate/Activate Doctor
**Test Cases:**
- [ ] **Deactivate Active**: Click "Deactivate" on active doctor → Should show confirmation
- [ ] **Confirm Deactivate**: Confirm → Doctor status should change to "Inactive"
- [ ] **Activate Inactive**: Click "Activate" on inactive doctor → Should show confirmation
- [ ] **Confirm Activate**: Confirm → Doctor status should change to "Active"
- [ ] **Button Text**: Button should show "Deactivate" for active, "Activate" for inactive
- [ ] **Button Color**: Orange for deactivate, green for activate

### 4.6 Delete Doctor
**Test Cases:**
- [ ] **Delete Confirmation**: Click delete icon → Should show double confirmation
- [ ] **First Confirmation**: Click yes → Should show second confirmation
- [ ] **Final Confirmation**: Click yes → Doctor should be deleted permanently
- [ ] **Cancel Delete**: Click no at any step → Doctor should remain
- [ ] **Constraint Check**: Try to delete doctor with appointments → Should show error message
- [ ] **Safe Delete**: Delete doctor with no appointments → Should delete successfully

---

## 5. APPOINTMENTS PAGE TESTING

### 5.1 New Appointment Tab
**Test Cases:**
- [ ] **Patient Selection**: Dropdown should show all patients
- [ ] **Patient Details**: Select patient → Name and age should auto-fill
- [ ] **Doctor Selection**: Dropdown should show active doctors only
- [ ] **Doctor Details**: Select doctor → Specialization and fee should auto-fill
- [ ] **Hospital Charges**: Should default to 50, allow editing
- [ ] **Appointment Status**: Should show dropdown with Scheduled, Completed, Cancelled, No Show
- [ ] **Additional Services**: Should show checkboxes for available services
- [ ] **Service Selection**: Check services → Should calculate total
- [ ] **Required Fields**: Try to create without patient/doctor → Should show error
- [ ] **Create Success**: Valid data → Should create appointment and show bill

### 5.2 Bill Generation
**Test Cases:**
- [ ] **Auto Bill Creation**: Create appointment → Bill should be generated automatically
- [ ] **Bill Modal**: After creation → Bill modal should open automatically
- [ ] **Bill Content**: Should show patient info, doctor info, charges breakdown
- [ ] **Token Number**: Should display formatted token (DR008-20251229-001)
- [ ] **Token Formatting**: Last 3 digits should be larger, bold, blue
- [ ] **Print Function**: Click print → Should open print dialog
- [ ] **Payment Status**: Should show current payment status with controls

### 5.3 Payment Status Management
**Test Cases:**
- [ ] **Status Display**: Should show current payment status with color coding
- [ ] **Status Options**: Dropdown should show Pending, Paid, Partial
- [ ] **Update Status**: Change status → Click update → Should save successfully
- [ ] **Status Colors**: Pending (red), Paid (green), Partial (yellow)
- [ ] **No Bill State**: Appointment without bill → Should show "No Bill Generated"
- [ ] **Update Success**: Should show success message and refresh data

### 5.4 Today's Appointments Tab
**Test Cases:**
- [ ] **Load Today**: Should show appointments for current date only
- [ ] **Appointment Data**: Should show patient, doctor, time, status, amount
- [ ] **Status Badges**: Should show colored status badges
- [ ] **View Bill**: Click "View Bill" → Should open bill modal
- [ ] **Complete Appointment**: Click "Complete" → Should update status
- [ ] **Filter Section**: Should show filter options for today's appointments

### 5.5 Today's Appointments Filters
**Test Cases:**
- [ ] **Doctor Filter**: Select doctor → Should show only that doctor's appointments
- [ ] **Status Filter**: Select status → Should show only appointments with that status
- [ ] **Patient Filter**: Type patient name → Should filter by patient name
- [ ] **Clear Filters**: Click clear → Should reset all filters
- [ ] **Combined Filters**: Use multiple filters → Should apply all simultaneously

### 5.6 All Appointments Tab
**Test Cases:**
- [ ] **Load All**: Should show all appointments from all dates
- [ ] **Date Range**: Should show date range filters
- [ ] **Filter by Date**: Set date range → Should show appointments in range only
- [ ] **Doctor Filter**: Select doctor → Should filter by doctor
- [ ] **Status Filter**: Select status → Should filter by status
- [ ] **Patient Filter**: Type patient name → Should filter by patient
- [ ] **Clear All Filters**: Should reset all filters and show all appointments

### 5.7 Appointment Status Updates
**Test Cases:**
- [ ] **Complete Appointment**: Click complete → Status should change to "Completed"
- [ ] **Status Persistence**: Refresh page → Status changes should persist
- [ ] **Status History**: Should maintain status change history

---

## 6. VOUCHERS PAGE TESTING

### 6.1 Voucher Dashboard
**Test Cases:**
- [ ] **Statistics Cards**: Should show total vouchers, pending approval, approved, paid counts
- [ ] **Card Updates**: Create/update vouchers → Statistics should update
- [ ] **Navigation**: Should integrate with HMS sidebar navigation

### 6.2 Voucher List
**Test Cases:**
- [ ] **Load Vouchers**: Should display all vouchers in table
- [ ] **Voucher Data**: Should show voucher number, type, doctor, amount, status, dates
- [ ] **Status Badges**: Different colors for Draft, Pending, Approved, Paid, Rejected
- [ ] **Sorting**: Click column headers → Should sort by that column
- [ ] **Pagination**: If many vouchers → Should paginate results

### 6.3 Create New Voucher
**Test Cases:**
- [ ] **Open Modal**: Click "Create New Voucher" → Modal should open
- [ ] **Voucher Number**: Should auto-generate (VCH-YYYYMMDD-NNNN format)
- [ ] **Voucher Types**: Should show DOCTOR_PAYMENT, HOSPITAL_EXPENSE, ADJUSTMENT
- [ ] **Doctor Selection**: For DOCTOR_PAYMENT → Should show doctor dropdown
- [ ] **Date Fields**: Should show date pickers for period start/end
- [ ] **Amount Field**: Should accept decimal amounts
- [ ] **Description**: Should accept text description
- [ ] **Required Fields**: Should validate required fields
- [ ] **Save Draft**: Should save as Draft status
- [ ] **Submit for Approval**: Should save as Pending status

### 6.4 Voucher Workflow
**Test Cases:**
- [ ] **Draft → Pending**: Submit draft voucher → Should change to Pending
- [ ] **Pending → Approved**: Approve pending voucher → Should change to Approved
- [ ] **Approved → Paid**: Mark approved voucher as paid → Should change to Paid
- [ ] **Reject Voucher**: Reject pending voucher → Should change to Rejected
- [ ] **Status Restrictions**: Should only allow valid status transitions

### 6.5 Voucher Filters
**Test Cases:**
- [ ] **Filter by Status**: Select status → Should show only vouchers with that status
- [ ] **Filter by Type**: Select type → Should show only vouchers of that type
- [ ] **Filter by Doctor**: Select doctor → Should show only that doctor's vouchers
- [ ] **Date Range Filter**: Set date range → Should filter by voucher date
- [ ] **Clear Filters**: Should reset all filters

### 6.6 Edit/Delete Vouchers
**Test Cases:**
- [ ] **Edit Draft**: Should allow editing draft vouchers
- [ ] **Edit Restrictions**: Should prevent editing approved/paid vouchers
- [ ] **Delete Draft**: Should allow deleting draft vouchers
- [ ] **Delete Restrictions**: Should prevent deleting processed vouchers
- [ ] **Confirmation**: Delete should require confirmation

---

## 7. REPORTS PAGE TESTING

### 7.1 Doctor Report Tab
**Test Cases:**
- [ ] **Doctor Selection**: Dropdown should show all doctors + "All Doctors" option
- [ ] **Date Range**: Should require start and end dates
- [ ] **Generate Report**: Valid inputs → Should generate doctor report
- [ ] **Report Content**: Should show appointments, fees, patient list
- [ ] **All Doctors**: Select "All Doctors" → Should show aggregated data
- [ ] **Specific Doctor**: Select one doctor → Should show only that doctor's data
- [ ] **Print Report**: Click print → Should format for printing
- [ ] **Date Validation**: End date before start date → Should show error

### 7.2 Hospital Report Tab
**Test Cases:**
- [ ] **Date Range**: Should require start and end dates
- [ ] **Generate Report**: Should create comprehensive hospital report
- [ ] **Summary Statistics**: Should show patient registrations, appointments, completion rates
- [ ] **Revenue Breakdown**: Should show doctor fees, hospital charges, additional services
- [ ] **Payment Status**: Should show collected vs pending amounts
- [ ] **Doctor Summary**: Should show doctor-wise breakdown
- [ ] **Service Summary**: Should show additional services breakdown
- [ ] **Print Function**: Should format properly for printing

### 7.3 Summary Report Tab
**Test Cases:**
- [ ] **Date Selection**: Should allow selecting specific date
- [ ] **Daily Summary**: Should generate summary for selected date
- [ ] **Statistics Cards**: Should show appointments, patients, revenue, completion rate
- [ ] **Visual Design**: Should use colored gradient cards
- [ ] **Appointment Status**: Should show completed, scheduled, cancelled breakdown
- [ ] **Revenue Sources**: Should show breakdown by source type
- [ ] **Print Function**: Should format for printing

### 7.4 Revenue Calculations
**Test Cases:**
- [ ] **Paid Bills Only**: Revenue should only include bills marked as "Paid"
- [ ] **Pending Amounts**: Should show correct pending payment amounts
- [ ] **Total Calculations**: Should accurately sum all revenue sources
- [ ] **Date Filtering**: Should only include bills within selected date range
- [ ] **Zero Revenue**: If no paid bills → Should show $0.00 correctly

---

## 8. CROSS-PAGE FUNCTIONALITY TESTING

### 8.1 Navigation Testing
**Test Cases:**
- [ ] **Sidebar Navigation**: Click each menu item → Should navigate correctly
- [ ] **Breadcrumb Navigation**: Should show current page location
- [ ] **Back Button**: Browser back → Should work correctly
- [ ] **Direct URL Access**: Type page URLs directly → Should load correctly
- [ ] **Authentication Check**: Access pages without login → Should redirect to login

### 8.2 Data Consistency
**Test Cases:**
- [ ] **Patient-Doctor Relationship**: Patient appointments should show correct doctor
- [ ] **Bill-Appointment Link**: Bills should link to correct appointments
- [ ] **Status Updates**: Status changes should reflect across all pages
- [ ] **Real-time Updates**: Changes in one page should reflect in others
- [ ] **Data Integrity**: Deleting referenced data should show appropriate errors

### 8.3 Session Management
**Test Cases:**
- [ ] **Session Timeout**: Long inactivity → Should handle gracefully
- [ ] **Multiple Tabs**: Open multiple tabs → Should maintain session
- [ ] **Logout**: Logout from one tab → Should logout from all tabs
- [ ] **Token Refresh**: Should handle token refresh automatically

---

## 9. ERROR HANDLING TESTING

### 9.1 Network Errors
**Test Cases:**
- [ ] **Server Down**: Stop backend server → Should show appropriate error messages
- [ ] **Slow Network**: Simulate slow connection → Should show loading states
- [ ] **Connection Lost**: Disconnect internet → Should handle gracefully
- [ ] **Timeout**: Long-running requests → Should timeout appropriately

### 9.2 Data Validation Errors
**Test Cases:**
- [ ] **Required Fields**: Submit forms without required data → Should show validation
- [ ] **Invalid Formats**: Enter invalid email, phone, etc. → Should show format errors
- [ ] **Duplicate Data**: Try to create duplicates → Should prevent and show error
- [ ] **Constraint Violations**: Delete referenced data → Should show constraint errors

### 9.3 User Interface Errors
**Test Cases:**
- [ ] **Modal Errors**: Errors in modals → Should display within modal
- [ ] **Form Errors**: Field-level errors → Should highlight problematic fields
- [ ] **Toast Messages**: Success/error messages → Should appear and auto-dismiss
- [ ] **Error Recovery**: After error → User should be able to retry

---

## 10. RESPONSIVE DESIGN TESTING

### 10.1 Mobile Testing (< 768px)
**Test Cases:**
- [ ] **Sidebar**: Should collapse to hamburger menu
- [ ] **Tables**: Should scroll horizontally or stack appropriately
- [ ] **Modals**: Should fit mobile screen properly
- [ ] **Buttons**: Should be touch-friendly size
- [ ] **Forms**: Should stack vertically on mobile
- [ ] **Navigation**: Should be easily accessible

### 10.2 Tablet Testing (768px - 1024px)
**Test Cases:**
- [ ] **Layout**: Should adapt to tablet screen size
- [ ] **Touch Interactions**: Should work with touch input
- [ ] **Orientation**: Should work in both portrait and landscape

### 10.3 Desktop Testing (> 1024px)
**Test Cases:**
- [ ] **Full Layout**: Should use full screen width effectively
- [ ] **Hover States**: Should show hover effects on interactive elements
- [ ] **Keyboard Navigation**: Should support keyboard shortcuts

---

## 11. PERFORMANCE TESTING

### 11.1 Load Times
**Test Cases:**
- [ ] **Initial Load**: First page load should be under 3 seconds
- [ ] **Navigation**: Page transitions should be under 1 second
- [ ] **Data Loading**: Large datasets should load with pagination
- [ ] **Image Loading**: Icons and images should load quickly

### 11.2 Data Handling
**Test Cases:**
- [ ] **Large Datasets**: Test with 100+ patients, doctors, appointments
- [ ] **Search Performance**: Search should be responsive with large datasets
- [ ] **Filter Performance**: Filters should apply quickly
- [ ] **Memory Usage**: Should not cause memory leaks

---

## 12. SECURITY TESTING

### 12.1 Authentication
**Test Cases:**
- [ ] **Login Required**: All pages should require authentication
- [ ] **Session Security**: Sessions should expire appropriately
- [ ] **Password Security**: Passwords should be handled securely
- [ ] **Token Management**: JWT tokens should be managed properly

### 12.2 Data Security
**Test Cases:**
- [ ] **Input Sanitization**: Should prevent XSS attacks
- [ ] **SQL Injection**: Should prevent SQL injection
- [ ] **Data Validation**: Should validate all input data
- [ ] **Access Control**: Should prevent unauthorized data access

---

## TEST EXECUTION CHECKLIST

### Pre-Test Setup
- [ ] Backend server running on port 8000
- [ ] Database connected and initialized
- [ ] Sample data loaded (patients, doctors, appointments)
- [ ] Browser developer tools open for debugging

### Test Execution
- [ ] Execute tests in order (login first, then other pages)
- [ ] Document any failures with screenshots
- [ ] Test on multiple browsers (Chrome, Firefox, Edge)
- [ ] Test on different screen sizes
- [ ] Record performance metrics

### Post-Test Cleanup
- [ ] Document all issues found
- [ ] Prioritize issues by severity
- [ ] Create bug reports for failures
- [ ] Verify fixes after implementation

---

## ISSUE REPORTING TEMPLATE

**Issue ID**: [Unique identifier]
**Page**: [Which page the issue occurs on]
**Function**: [Which function is affected]
**Steps to Reproduce**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Result**: [What should happen]
**Actual Result**: [What actually happens]
**Severity**: [Critical/High/Medium/Low]
**Browser**: [Chrome/Firefox/Edge version]
**Screenshot**: [Attach if applicable]

---

## TESTING NOTES

- Test each function thoroughly before moving to the next
- Pay special attention to data relationships between pages
- Verify that all CRUD operations work correctly
- Ensure proper error handling and user feedback
- Test edge cases and boundary conditions
- Verify responsive design on different devices
- Check for memory leaks during extended testing
- Validate all security measures are working

This comprehensive test document covers every aspect of your HMS system. Execute these tests systematically to ensure your system is robust and user-friendly.