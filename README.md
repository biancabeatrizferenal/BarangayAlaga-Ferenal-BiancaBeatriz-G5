# Barangay Alaga

### Community-Based Healthcare Made Accessible

Barangay Alaga is a web-based barangay healthcare appointment management system that allows residents to schedule and manage healthcare appointments while enabling barangay healthcare staff and administrators to oversee appointment records.

## Project Information

- **System Name:** Barangay Alaga
- **Developer:** Bianca Beatriz A. Ferenal
- **Course:** CSIT327 – Information Management 2
- **Section:** G5
- **Institution:** Cebu Institute of Technology – University
- **Project Development:** PD3 – Application Hardening
- **Core Feature:** Healthcare Appointment Booking and Management

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Django 6.0.10 |
| Frontend | HTML, CSS, Django Templates |
| Database | PostgreSQL through Supabase |
| Database Driver | Psycopg 3 |
| Development Environment | Visual Studio Code |
| Version Control | Git and GitHub |
| Automated Testing | Django Test Framework |

## Existing Application Features

### Resident

- Account registration and authentication
- Resident dashboard
- Profile management
- Healthcare appointment booking
- Appointment details viewing
- Pending appointment updating
- Pending appointment cancellation
- Appointment status monitoring

### Healthcare Staff

- Staff dashboard
- View healthcare appointment records
- View appointment details
- Confirm or reject pending appointments
- Mark confirmed appointments as completed

### Administrator

- Administrator dashboard
- View healthcare appointment records
- View appointment details
- Monitor appointment statistics

Administrator appointment oversight is read-only.

## Core Feature: Healthcare Appointment Booking and Management

The primary feature implemented during Project Development 2 is the Healthcare Appointment Booking and Management module.

This module supports the complete appointment workflow from resident booking to staff processing and administrator monitoring.

Project Development 3 focuses on hardening this existing module and its supporting account functionality.

### Available Healthcare Services

- General Checkup
- Medical Consultation
- Vaccination
- Maternal Care
- Other Healthcare Services

### Appointment Booking Rules

- Appointment dates and times must not be in the past.
- Appointments may be scheduled up to 90 days in advance.
- Appointment slots use 30-minute intervals.
- Available appointment times are from 9:00 AM to 5:00 PM.
- The lunch break from 12:00 PM to 1:00 PM is excluded.
- Duplicate active appointment slots are prevented.
- New appointment requests receive Pending status.
- Residents can edit or cancel only their own pending appointments.

### Appointment Status Workflow

Pending appointments may be confirmed or rejected by healthcare staff.

Confirmed appointments may be marked as completed.

Residents may cancel their own pending appointments.

The system uses the following appointment statuses:

- Pending
- Confirmed
- Completed
- Rejected
- Cancelled

## Database Design

The application uses Supabase PostgreSQL as its primary database.

### Main Models

**User**

- Stores account information and assigned user roles.
- Supports resident, staff, and administrator accounts.

**ResidentProfile**

- Stores additional resident information.
- Connected to the User model through a one-to-one relationship.

**StaffProfile**

- Stores additional healthcare staff information.
- Connected to the User model through a one-to-one relationship.

**Appointment**

- Stores healthcare appointment information.
- Connected to the User model through a foreign key.
- Records service type, appointment date, appointment time, reason, status, and timestamps.

Django migrations are used to manage database schema changes.

A conditional database uniqueness constraint prevents multiple active appointments from occupying the same date and time.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/biancabeatrizferenal/BarangayAlaga-Ferenal-BiancaBeatriz-G5.git
cd BarangayAlaga-Ferenal-BiancaBeatriz-G5
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

For macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

Verify the installed dependencies:

```bash
python -m pip check
```

### 4. Configure environment variables

Create a `.env` file using the provided `.env.example` file as a reference.

For Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Configure the following environment variables using your own PostgreSQL or Supabase database credentials:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True

DB_NAME=postgres
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=your-database-host
DB_PORT=5432
```

Generate a Django secret key if needed:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

The actual `.env` file must never be committed to GitHub.

Set `DJANGO_DEBUG=False` when testing custom error pages. Production environments must also use `DEBUG=False` and appropriate deployment security settings.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Verify the application configuration

```bash
python manage.py check
```

### 7. Run the development server

```bash
python manage.py runserver
```

Access the application at:

http://127.0.0.1:8000/

## Application Routes

| Route | Description |
|---|---|
| `/accounts/register/` | Resident registration |
| `/accounts/login/` | User authentication |
| `/accounts/logout/` | User logout through POST |
| `/accounts/dashboard/` | Role-based dashboard |
| `/accounts/profile/` | Profile management |
| `/appointments/` | Resident appointments |
| `/appointments/book/` | Appointment booking |
| `/appointments/staff/` | Staff appointment management |
| `/appointments/admin/` | Administrator appointment oversight |
| `/admin/` | Django administration |

## PD3 Application Hardening

Project Development 3 focuses on improving the reliability, security, validation, and maintainability of existing application features rather than introducing new functionality.

### Validation and Error Handling

- Server-side form validation
- Duplicate email validation
- Philippine mobile number validation
- Minimum registration age validation
- Profile photo size and format validation
- Appointment date and time validation
- Duplicate appointment slot prevention
- Invalid appointment status transition prevention
- User-friendly success and error messages
- Custom 403 Forbidden error page
- Custom 404 Page Not Found error page
- Custom 500 Internal Server Error page
- Safe handling of invalid appointment IDs

### Access Control and Security

- Authentication requirements for protected pages
- Django password hashing
- Role-based access control for residents, staff, and administrators
- Appointment ownership verification
- CSRF protection
- POST-only appointment cancellation and status updates
- POST-only logout
- Environment-based secret and database configuration
- Environment-based DEBUG configuration
- Django ORM for database operations

### Data Integrity and Reliability

- Database-level unique constraints for active appointment slots
- Foreign key relationships
- Atomic database transactions
- Row-level locking for appointment mutations
- Redirect-after-POST implementation
- Appointment cancellation confirmation
- Optimized administrator appointment statistics
- Related-object query optimization using `select_related()`

## Automated Testing

Automated tests are implemented using Django's testing framework.

### Run All Tests

```bash
python manage.py test
```

### Run Tests with Detailed Output

```bash
python manage.py test --verbosity=2
```

### Run Account Tests Only

```bash
python manage.py test accounts
```

### Run Appointment Tests Only

```bash
python manage.py test appointments
```

### Test File Locations

- `accounts/tests.py`
- `appointments/tests.py`

### Test Coverage

| Test Category | Number of Tests | Passed |
|---|---:|---:|
| Account functionality | 10 | 10 |
| Healthcare appointment functionality | 20 | 20 |
| **Total** | **30** | **30** |

### Account Tests

| Test Name | Result |
|---|---|
| `test_valid_resident_registration` | Pass |
| `test_duplicate_email_registration` | Pass |
| `test_underage_registration` | Pass |
| `test_invalid_phone_registration` | Pass |
| `test_valid_login` | Pass |
| `test_invalid_login` | Pass |
| `test_dashboard_requires_login` | Pass |
| `test_valid_profile_update` | Pass |
| `test_logout_requires_post` | Pass |
| `test_valid_logout` | Pass |

### Healthcare Appointment Tests

| Test Name | Result |
|---|---|
| `test_valid_appointment_booking` | Pass |
| `test_past_appointment_date_rejected` | Pass |
| `test_duplicate_appointment_slot_rejected` | Pass |
| `test_valid_appointment_update` | Pass |
| `test_valid_appointment_cancellation` | Pass |
| `test_other_resident_cannot_view_appointment` | Pass |
| `test_other_resident_cannot_update_appointment` | Pass |
| `test_other_resident_cannot_cancel_appointment` | Pass |
| `test_resident_cannot_access_staff_pages` | Pass |
| `test_resident_cannot_access_admin_pages` | Pass |
| `test_cancellation_requires_post` | Pass |
| `test_status_update_requires_post` | Pass |
| `test_valid_staff_status_update` | Pass |
| `test_invalid_status_transition_rejected` | Pass |
| `test_appointment_list_requires_login` | Pass |
| `test_invalid_appointment_id_returns_404` | Pass |
| `test_appointment_details_displayed` | Pass |
| `test_admin_appointment_counts` | Pass |
| `test_database_prevents_duplicate_active_slot` | Pass |
| `test_cancellation_requires_csrf_token` | Pass |

### Final Regression Test Results

| Metric | Result |
|---|---|
| Total tests | 30 |
| Passed | 30 |
| Failures | 0 |
| Errors | 0 |
| Passing rate | 100% |
| Execution time | 151.555 seconds |
| Exit code | 0 |
| Django system check | No issues |
| Dependency check | No broken requirements |

Recorded test output:

```text
Found 30 test(s).
Using existing test database for alias 'default'...
System check identified no issues (0 silenced).
..............................
----------------------------------------------------------------------
Ran 30 tests in 151.555s

OK
Preserving test database for alias 'default'...
```

The automated tests cover valid and invalid inputs, authentication, profile management, appointment operations, authorization, ownership restrictions, CSRF protection, database constraints, and appointment status transitions.

### Test Database Configuration

The application uses PostgreSQL for both application development and automated testing.

A custom Django test runner is implemented in:

```text
config/test_runner.py
```

The custom test runner preserves the isolated test database between test executions. This prevents database teardown errors caused by persistent PostgreSQL connections encountered during testing with Supabase.

The application database remains separate from the test database.

The configured database user must have sufficient permissions to create the test database during initial setup.

Use a dedicated development or testing database environment when running automated tests.

The underlying persistent connection issue remains a known infrastructure limitation.

## Git Branching Strategy

The project follows a branch-based development workflow.

### Main Branches

- `main` – Stable project version
- `develop` – Integration branch

### PD2 Feature Branches

- `feature/appointment-booking`
- `feature/appointment-management`
- `feature/admin-appointment-oversight`
- `feature/appointment-tests`
- `docs/pd2-documentation`

### PD3 Working Branches

- `hardening/validation-error-handling`
- `hardening/access-control`
- `hardening/data-integrity`
- `test/core-feature-tests`
- `docs/pd3-hardening-report`

Changes are integrated through GitHub pull requests.

Development commits follow Conventional Commits naming conventions, including:

- `feat`
- `fix`
- `perf`
- `test`
- `docs`
- `chore`
- `refactor`

Working branches are retained for project development verification.

### PD3 Pull Requests

| PR | Branch | Purpose |
|---|---|---|
| [#7](https://github.com/biancabeatrizferenal/BarangayAlaga-Ferenal-BiancaBeatriz-G5/pull/7) | `hardening/access-control` | Access control and security |
| [#8](https://github.com/biancabeatrizferenal/BarangayAlaga-Ferenal-BiancaBeatriz-G5/pull/8) | `hardening/data-integrity` | Data integrity and database efficiency |
| [#9](https://github.com/biancabeatrizferenal/BarangayAlaga-Ferenal-BiancaBeatriz-G5/pull/9) | `test/core-feature-tests` | Automated testing and validation fixes |
| [#10](https://github.com/biancabeatrizferenal/BarangayAlaga-Ferenal-BiancaBeatriz-G5/pull/10) | `hardening/validation-error-handling` | Validation and custom error pages |
| [#6](https://github.com/biancabeatrizferenal/BarangayAlaga-Ferenal-BiancaBeatriz-G5/pull/6) | `develop` | Combined PD2 and PD3 release |

## Known Limitations and Remaining Tasks

The following enhancements are deferred to a future development increment because PD3 focuses exclusively on hardening existing features.

| Remaining Task | Priority | Target Increment |
|---|---|---|
| Appointment notifications | High | PD4 |
| Appointment search and filtering | Medium | PD4 |
| Healthcare announcements | Medium | PD4 |

### Outstanding Issue

The isolated PostgreSQL test database cannot always be deleted after testing because another database connection remains active.

A custom Django test runner preserves the isolated test database as a workaround.

All 30 automated tests pass successfully using this configuration.

## Project Documentation

Project development completion reports are maintained in the `docs/` directory.

The required PD3 report filename is:

```text
BarangayAlaga-Ferenal-BiancaBeatriz-G5-PD3.pdf
```

## Project Development 3 Deliverables

- Hardened healthcare appointment management module
- Hardened account registration and profile validation
- Custom 403, 404, and 500 error pages
- Authentication and role-based access control
- Appointment ownership protection
- CSRF protection and POST-only mutations
- Database constraints and atomic transactions
- Database query optimization
- 30 automated tests
- Updated README documentation
- Environment configuration template
- Verified project dependencies
- PD3 Hardening Completion Report
- GitHub working branches and pull requests

## Repository

https://github.com/biancabeatrizferenal/BarangayAlaga-Ferenal-BiancaBeatriz-G5

## Developer

**Bianca Beatriz A. Ferenal**

BS Information Technology – G5

Cebu Institute of Technology – University
