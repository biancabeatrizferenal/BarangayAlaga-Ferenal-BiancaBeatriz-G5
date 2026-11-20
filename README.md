
# Barangay Alaga

### Community-Based Healthcare Made Accessible

Barangay Alaga is a web-based healthcare appointment management system designed to improve access to community healthcare services.

The application allows residents to book and manage healthcare appointments, healthcare staff to process appointment requests, and administrators to monitor appointment records.

This project was developed as part of the IM2 Project Development requirements.

## Project Information

- **Project Name:** Barangay Alaga
- **Developer:** Bianca Beatriz A. Ferenal
- **Section:** G5
- **Framework:** Django 6.0.10
- **Database:** Supabase PostgreSQL
- **Frontend:** HTML, CSS, Django Templates
- **Programming Language:** Python

## Technology Stack

### Backend
- Python
- Django 6.0.10
- Django ORM
- Psycopg 3

### Frontend
- HTML5
- CSS3
- Django Template Language

### Database
- Supabase PostgreSQL

### Development Tools
- Visual Studio Code
- Git
- GitHub
- Python Virtual Environment

## User Roles

Barangay Alaga supports three user roles.

### Resident
Residents can:
- Register an account.
- Log in and log out.
- View and update their profile.
- Book healthcare appointments.
- View their appointment history.
- Edit pending appointments.
- Cancel pending appointments.
- Track appointment statuses.

### Staff
Healthcare staff can:
- Log in to their accounts.
- Access the staff dashboard.
- View appointment requests.
- Review resident appointment details.
- Confirm pending appointments.
- Reject pending appointments.
- Mark confirmed appointments as completed.

### Administrator
Administrators can:
- Log in to their accounts.
- Access the administrator dashboard.
- View all healthcare appointments.
- Monitor appointment statistics.
- Review individual appointment records.

Administrator appointment oversight is read-only.

## Core Feature: Healthcare Appointment Booking and Management

The primary feature implemented for Project Development 2 is the Healthcare Appointment Booking and Management module.

This module supports the complete appointment workflow from resident booking to staff processing and administrator monitoring.

### Available Healthcare Services

- General Checkup
- Medical Consultation
- Vaccination
- Maternal Care
- Other Healthcare Services

### Appointment Booking Rules

- Residents must select a future appointment date.
- Appointments may be scheduled up to 90 days in advance.
- Appointment slots use 30-minute intervals.
- Available appointment times are from 9:00 AM to 5:00 PM.
- The lunch break from 12:00 PM to 1:00 PM is excluded.
- Duplicate active appointment slots are prevented.
- New appointment requests receive Pending status.
- Residents can edit or cancel only pending appointments.

### Appointment Status Workflow

Pending appointments may be confirmed or rejected by staff.

Confirmed appointments may be marked as completed.

Residents can cancel their own pending appointments.

The system uses the following statuses:

- Pending
- Confirmed
- Completed
- Rejected
- Cancelled

## Database Design

The application uses Supabase PostgreSQL as its primary database.

### Main Models

**User**
- Stores account information and assigned user role.

**ResidentProfile**
- Stores additional resident information.
- Connected to the User model through a one-to-one relationship.

**StaffProfile**
- Stores additional staff information.
- Connected to the User model through a one-to-one relationship.

**Appointment**
- Stores appointment information.
- Connected to the User model through a foreign key.
- Records service type, appointment date, appointment time, reason, status, and timestamps.

Django migrations are used to manage database schema changes.

A conditional database uniqueness constraint prevents multiple active appointments from occupying the same date and time.

## Security and Validation

Barangay Alaga implements:

- Django authentication
- Password hashing
- Role-based access control
- Login-required views
- Resident appointment ownership checks
- CSRF protection for form submissions
- Server-side form validation
- Database-level appointment slot protection
- Atomic database transactions
- Restricted appointment status transitions

Environment variables are used to configure database credentials.

The `.env` file must not be committed to GitHub.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/biancabeatrizferenal/BarangayAlaga-Ferenal-BiancaBeatriz-G5.git
```

### 2. Navigate to the project folder

```bash
cd BarangayAlaga-Ferenal-BiancaBeatriz-G5
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project root.

Configure the Supabase PostgreSQL credentials using the variable names expected by `config/settings.py`.

Do not share or commit actual database credentials.

### 7. Apply database migrations

```bash
python manage.py migrate
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/

## Automated Testing

Automated tests are implemented using Django's testing framework.

The appointment test suite contains 13 test cases covering:

- Resident appointment viewing
- Appointment ownership protection
- Appointment creation
- Duplicate appointment prevention
- Appointment cancellation
- Staff appointment confirmation
- Staff appointment completion
- Invalid status transition prevention
- Administrator appointment oversight
- Role-based access restrictions
- HTTP method restrictions

### Run the Tests

```bash
python manage.py test appointments --settings=config.test_settings -v 2
```

The test settings use an isolated in-memory SQLite database instead of the production Supabase PostgreSQL database.

## Git Branching Strategy

The project follows a feature-branch development workflow.

### Main Branches

- `main` — Stable project version
- `develop` — Integration branch

### Feature Branches

- `feature/appointment-booking`
- `feature/appointment-management`
- `feature/admin-appointment-oversight`
- `feature/appointment-tests`

### Documentation Branch

- `docs/pd2-documentation`

Feature branches are merged through GitHub Pull Requests.

Commits follow Conventional Commits naming conventions.

## Project Development 2 Deliverables

- Complete Django appointment module
- Supabase PostgreSQL integration
- Database models and migrations
- Forms and server-side validation
- Role-based views and URL routes
- Resident, Staff, and Administrator interfaces
- Appointment workflow and status management
- Automated appointment tests
- GitHub feature branches and pull requests
- Project documentation

## Developer

**Bianca Beatriz A. Ferenal**

BS Information Technology

Cebu Institute of Technology – University

Section G5
