# Manual Token Number Feature

## Changes Made

The system has been updated to support **manual token number entry** while maintaining automatic generation as a fallback.

### Backend Changes

#### 1. Schema Update (`backend/app/schemas/appointment.py` & `HMS/backend/app/schemas/appointment.py`)
- Added optional `token_number` field to `AppointmentCreate` schema
- Added validator to ensure token number is not empty if provided
- Token number is optional (max 50 characters)

#### 2. API Endpoint Update (`backend/app/main.py` & `HMS/backend/app/main.py`)
- Modified `/api/appointments` POST endpoint
- Logic now checks if manual token is provided:
  - **If provided**: Validates uniqueness and uses the manual token
  - **If not provided**: Auto-generates token using existing logic
- Returns error if duplicate token number is detected

### Frontend Changes

#### 1. Form Update (`frontend/appointments.html` & `HMS/frontend/appointments.html`)
- Added new input field: "Token Number (Optional)"
- Field includes placeholder text: "Leave empty for auto-generate"
- Helper text below field explains the behavior
- Field is limited to 50 characters (matching backend validation)

#### 2. JavaScript Update
- Modified `createAppointment()` function to capture manual token input
- Token is only sent to backend if user enters a value
- Form reset now clears the token number field

## How to Use

### Automatic Token Generation (Default)
1. Leave the "Token Number" field empty
2. System will auto-generate token in format: `{doctor_id}-{YYYYMMDD}-{counter:03d}`
3. Example: `DOC001-20260218-001`

### Manual Token Entry
1. Enter your desired token number in the "Token Number" field
2. System will validate uniqueness
3. If token already exists, you'll receive an error message
4. Token can be any format up to 50 characters

## Validation Rules

- Token number must be unique across all appointments
- Token number cannot be empty string (if provided)
- Maximum length: 50 characters
- Duplicate tokens will be rejected with error message

## Benefits

- **Flexibility**: Users can choose between manual and automatic token generation
- **Backward Compatible**: Existing auto-generation logic remains intact
- **Data Integrity**: Uniqueness validation prevents duplicate tokens
- **User-Friendly**: Clear UI guidance on how to use the feature
