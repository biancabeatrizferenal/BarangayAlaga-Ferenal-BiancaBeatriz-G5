# Barangay Alaga

Barangay Alaga is a web-based barangay healthcare appointment management system that allows residents to schedule and manage healthcare appointments while enabling barangay healthcare staff and administrators to oversee appointment records.

## Project Information

- **Developer:** Bianca Beatriz A. Ferenal
- **Course:** CSIT327 – Information Management 2
- **Section:** G5
- **Institution:** Cebu Institute of Technology – University
- **Project Development:** PD3 – Application Hardening

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Django 6.0.10 |
| Frontend | HTML, CSS, Django Templates |
| Database | PostgreSQL through Supabase |
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
- Appointment updating
- Appointment cancellation
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

Set `DJANGO_DEBUG=False` when testing custom error pages or configuring a production environment.

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
| `/accounts/dashboard/` | Role-based dashboard |
| `/accounts/profile/` | Profile management |
| `/appointments/` | Resident appointments |
| `/appointments/book/` | Appointment booking |
| `/appointments/staff/` | Staff appointment management |
| `/appointments/admin/` | Administrator appointment oversight |
| `/admin/` | Django administration |

## PD3 Application Hardening

PD3 focuses on improving the reliability, security, validation, and maintainability of existing application features rather than introducing new functionality.

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
- Custom 403, 404, and 500 error pages

### Access Control and Security

- Authentication requirements for protected pages
- Role-based access control for residents, staff, and administrators
- Appointment ownership verification
- CSRF protection
- POST-only appointment cancellation and status updates
- POST-only logout
- Environment-based secret and database configuration
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

Run the complete automated test suite:

```bash
python manage.py test
```

For detailed test results:

```bash
python manage.py test --verbosity=2
```

Run account tests only:

```bash
python manage.py test accounts
```

Run appointment tests only:

```bash
python manage.py test appointments
```

### Test Coverage

| Test Category | Number of Tests | Passed |
|---|---:|---:|
| Account functionality | 10 | 10 |
| Healthcare appointment functionality | 20 | 20 |
| **Total** | **30** | **30** |

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

The automated tests cover valid and invalid inputs, authentication, profile management, appointment operations, authorization, ownership restrictions, CSRF protection, database constraints, and appointment status transitions.

### Test Database Configuration

The application uses PostgreSQL for both application development and automated testing.

A custom Django test runner preserves the isolated test database between test executions. This prevents database teardown errors caused by persistent PostgreSQL connections encountered during testing with Supabase.

The application database remains separate from the test database. The configured database user must have sufficient permissions to create the test database during initial setup.

The underlying persistent connection issue remains a known infrastructure limitation.

## Git Branching Strategy

The project follows a branch-based development workflow.

- `main` – Stable project version
- `develop` – Integration branch
- `feature/*` – Feature development
- `hardening/*` – Application hardening
- `test/*` – Automated testing
- `docs/*` – Project documentation

Changes are integrated through pull requests.

### PD3 Pull Requests

| PR | Branch | Purpose |
|---|---|---|
| #7 | `hardening/access-control` | Access control and security |
| #8 | `hardening/data-integrity` | Data integrity and database efficiency |
| #9 | `test/core-feature-tests` | Automated testing and validation fixes |
| #10 | `hardening/validation-error-handling` | Validation and custom error pages |

## Known Limitations and Remaining Tasks

The following enhancements are deferred to a future development increment because PD3 focuses exclusively on hardening existing features:

- Appointment notifications
- Appointment search and filtering
- Healthcare announcements

The isolated PostgreSQL test database is intentionally preserved between test executions to avoid persistent connection-related teardown errors.

## Project Documentation

Project development completion reports are maintained in the `docs/` directory.

## Repository

https://github.com/biancabeatrizferenal/BarangayAlaga-Ferenal-BiancaBeatriz-G5

## Developer

Bianca Beatriz A. Ferenal

BS Information Technology – G5

Cebu Institute of Technology – University