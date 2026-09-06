# CampusReserve User Manual

## Campus Smart Facility & Lab Equipment Reservation System

**Project:** CampusReserve
**Course:** IBL 3300 Software Engineering Studio
**Institution:** Technical University of Kenya
**Version:** 1.0

---

# Table of Contents

1. Introduction
2. System Access
3. Student User Guide
4. Administrator User Guide
5. Reservation Workflow
6. Check-In Workflow
7. Common Errors and Solutions
8. Security and Account Guidelines
9. System Requirements
10. Support and Maintenance
11. Application API Reference
12. Related Project Documentation
13. Conclusion

---

# 1. Introduction

## 1.1 Purpose

CampusReserve is a web-based campus resource reservation system designed to allow students to view available campus facilities and equipment, make reservations, manage their reservations, and complete reservation check-ins.

The system also provides administrators with tools for managing resources, reservations, users, and check-in records.

CampusReserve is implemented as a web application consisting of student and administrator frontend applications connected to a Flask REST API and MySQL database.

## 1.2 Main User Roles

CampusReserve has two primary user roles.

### Student

Students can:

* Register for an account.
* Log into the system.
* View available resources.
* View resource details.
* Create reservations.
* View their reservation history.
* Cancel eligible reservations.
* Access check-in information for their reservations.
* Complete reservation check-in.

### Administrator

Administrators can:

* Log into the administrator portal.
* View system statistics and activity.
* View and manage reservations.
* Manage campus resources.
* Monitor check-in records.
* View registered users.
* Update reservation statuses.
* Update resource availability/status.

---

# 2. System Access

CampusReserve consists of two frontend applications supported by a Flask backend API.

The production system is hosted using Vercel for the frontend applications, Render for the backend API, and Aiven for the production MySQL database.

## 2.1 Student Application

The production student application is available at:

```text
https://campus-resource-reservation.vercel.app/
```

Students use this application to:

* Register and log in.
* Browse resources.
* Create reservations.
* View reservations.
* Cancel reservations.
* Access reservation check-in information.
* Complete check-ins.

### Local Development

During local development, the student application is started with Vite:

```cmd
cd student-mobile
npm run dev
```

The development server uses the project's configured Vite development port.

The local frontend communicates with:

```text
http://127.0.0.1:5000/api
```

## 2.2 Administrator Application

The production administrator application is available at:

```text
https://campus-resource-reservation-2vz5.vercel.app/
```

Administrators use this application to manage:

* Dashboard information
* Reservations
* Resources
* Check-ins
* Users

### Local Development

During local development:

```cmd
cd admin-web
npm run dev
```

The Vite development server uses the project's configured development port.

The local administrator application communicates with:

```text
http://127.0.0.1:5000/api
```

## 2.3 Backend

The production Flask backend is hosted on Render at:

```text
https://campus-resource-reservation.onrender.com
```

The production API base URL is:

```text
https://campus-resource-reservation.onrender.com/api
```

The backend provides:

* Authentication
* Resource management
* Reservation processing
* Reservation cancellation
* Check-in functionality
* Administrative operations

During local development, the backend is available at:

```text
http://127.0.0.1:5000
```

with the API prefix:

```text
/api
```

## 2.4 Production Database

The production database is hosted on Aiven using MySQL.

The backend connects to the production database through the `DATABASE_URL` environment variable.

Database credentials are not stored in the frontend or committed to the repository.

---

# 3. Student User Guide

## 3.1 Registering an Account

A new student can create an account through the CampusReserve student application.

### Steps

1. Open the CampusReserve student application.
2. Select the registration option.
3. Enter the required information:

   * Name
   * Student ID
   * Email address
   * Password
4. Submit the registration form.
5. If the information is valid and the email/student ID is not already registered, the account is created.
6. Log in using the newly created account.

### Registration Requirements

The system validates required registration information and prevents duplicate email addresses and duplicate student IDs.

---

# 3.2 Logging In

### Steps

1. Open the CampusReserve student application.
2. Enter the registered email address.
3. Enter the account password.
4. Submit the login form.
5. On successful authentication, the student is taken to the application dashboard.

The application maintains the authenticated session using a JWT access token stored in browser local storage.

---

# 3.3 Student Dashboard

After logging in, the student can access the main application functions.

Typical functions include:

* Viewing available resources.
* Creating reservations.
* Viewing existing reservations.
* Cancelling eligible reservations.
* Accessing check-in information.

The dashboard provides the main navigation point for student activities.

---

# 3.4 Viewing Resources

Students can browse campus facilities and equipment available for reservation.

Resources are categorized as:

* Laboratory
* Study Room
* Equipment

Each resource may provide information such as:

* Resource name
* Resource type
* Description
* Location
* Capacity
* Availability status

### Steps

1. Log into the student application.
2. Open the resources section.
3. Browse the available resources.
4. Select a resource to view its details.

Only resources that are available for reservation should be selected when creating a new reservation.

---

# 3.5 Creating a Reservation

Students can create reservations for available resources.

### Steps

1. Log into CampusReserve.
2. Open the resource list.
3. Select the desired resource.
4. Choose the reservation date.
5. Enter a start time.
6. Enter an end time.
7. Enter the purpose of the reservation where applicable.
8. Submit the reservation.
9. Review the result displayed by the system.

The backend validates the reservation information before creating the reservation.

### Reservation Validation

The system checks that:

* The student is authenticated.
* The requested resource exists.
* The resource is available.
* Required reservation information is supplied.
* The reservation date and time are valid.
* The start time occurs before the end time.
* The request follows the application's reservation rules.

---

# 3.6 Viewing My Reservations

Students can view reservations associated with their account.

### Steps

1. Log into CampusReserve.
2. Open the reservations or **My Reservations** section.
3. Review the displayed reservations.

Reservation information can include:

* Reservation ID
* Resource
* Date
* Start time
* End time
* Purpose
* Status

Reservation statuses include:

* `PENDING`
* `CONFIRMED`
* `CANCELLED`
* `COMPLETED`

---

# 3.7 Cancelling a Reservation

Students can cancel eligible reservations belonging to their account.

### Steps

1. Open **My Reservations**.
2. Locate the reservation to be cancelled.
3. Select the cancellation option.
4. Confirm the action if prompted.
5. The reservation status is updated to `CANCELLED`.

A student cannot cancel another student's reservation.

Reservations that are already cancelled cannot be cancelled again.

---

# 3.8 Checking In

CampusReserve supports reservation check-in using reservation-specific check-in information and a QR/check-in token mechanism.

### Student Check-In Process

1. Log into the student application.
2. Open the relevant reservation.
3. Access the check-in information.
4. Use the available QR/check-in token mechanism.
5. Submit the check-in request.
6. The system validates the reservation and check-in request.
7. A successful check-in is recorded by the system.

A reservation can only have one check-in record.

Duplicate check-in attempts are rejected by the system.

---

# 3.9 Check-In Status

A check-in can have statuses including:

* `NOT_CHECKED_IN`
* `CHECKED_IN`

The system records the time at which a successful check-in occurs.

After successful check-in, the corresponding reservation/check-in information can also be viewed through the administrator portal.

---

# 4. Administrator User Guide

## 4.1 Administrator Login

Administrators use the administrator application:

```text
https://campus-resource-reservation-2vz5.vercel.app/
```

### Steps

1. Open the CampusReserve administrator application.
2. Enter administrator credentials.
3. Submit the login form.
4. The system authenticates the administrator.
5. On successful authentication, the administrator dashboard is displayed.

Administrative API operations require an authenticated administrator account.

Students cannot perform administrator-only operations.

---

# 4.2 Administrator Dashboard

The administrator dashboard provides an overview of system activity.

The interface contains navigation areas including:

* Dashboard
* Reservations
* Resources
* Check-ins
* Users

The dashboard provides administrators with a central point from which system operations can be monitored and managed.

---

# 4.3 Managing Resources

Administrators can manage campus resources.

Resources contain information such as:

* Name
* Type
* Description
* Location
* Capacity
* Status

Supported resource types are:

* `LABORATORY`
* `STUDY_ROOM`
* `EQUIPMENT`

Supported resource statuses are:

* `AVAILABLE`
* `UNAVAILABLE`

## Updating a Resource

### Steps

1. Open the **Resources** section.
2. Locate the resource.
3. Select the resource management/edit option.
4. Update the required information.
5. Save the changes.
6. Confirm that the updated resource information is displayed.

## Changing Resource Availability

An administrator can change the status of a resource between:

* `AVAILABLE`
* `UNAVAILABLE`

An unavailable resource should not be used for new reservations.

## Deleting a Resource

Where supported by the administrator interface, an administrator can delete a resource.

The backend validates the resource ID and returns an appropriate error if the requested resource does not exist.

---

# 4.4 Managing Reservations

Administrators can view reservations across the system.

### Steps

1. Open the **Reservations** section.
2. Review the reservation records.
3. Select a reservation to view its details.
4. Where necessary, update its status.
5. Confirm that the updated status is reflected in the reservation list.

Reservation statuses include:

* `PENDING`
* `CONFIRMED`
* `CANCELLED`
* `COMPLETED`

Administrative reservation management allows the institution to monitor and control reservation activity.

---

# 4.5 Updating Reservation Status

Administrators can update the status of reservations.

### Steps

1. Open the **Reservations** section.
2. Locate the required reservation.
3. Select the status management option.
4. Select the appropriate status.
5. Save the change.
6. Verify the updated reservation status.

The backend validates the supplied status and rejects invalid status values.

---

# 4.6 Monitoring Check-Ins

Administrators can view check-in records through the **Check-ins** section.

The check-in management area allows administrators to monitor whether reservations have been checked into.

Check-in information can be associated with:

* Reservation
* QR/check-in token
* Check-in timestamp
* Check-in status

Administrators can use this information to monitor resource usage and attendance.

---

# 4.7 Viewing Users

Administrators can access the **Users** section.

The users section provides information about registered system users.

Users have one of two roles:

* `STUDENT`
* `ADMIN`

Administrative access is protected and student accounts cannot perform administrator-only operations.

---

# 5. Reservation Workflow

The normal reservation lifecycle is:

```text
Student Login
     |
     v
Browse Resources
     |
     v
Select Available Resource
     |
     v
Choose Date and Time
     |
     v
Submit Reservation
     |
     v
Reservation Created
     |
     v
Reservation Confirmed
     |
     v
Check In
     |
     v
Reservation Completed
```

A reservation may instead be cancelled:

```text
Reservation
     |
     v
Cancel Reservation
     |
     v
CANCELLED
```

Administrators can also manage reservation statuses where required.

---

# 6. Check-In Workflow

The check-in workflow is:

```text
Confirmed Reservation
       |
       v
Access Check-In
       |
       v
Submit QR/Check-In Token
       |
       v
Validate Reservation
       |
       +---- Invalid/Unauthorized ----> Reject Request
       |
       v
Create Check-In
       |
       v
CHECKED_IN
```

The system validates the reservation and user before accepting the check-in.

The system prevents duplicate check-ins for the same reservation.

---

# 7. Common Errors and Solutions

## 7.1 Invalid Login Credentials

**Problem:** Login fails.

**Possible causes:**

* Incorrect email.
* Incorrect password.
* Account does not exist.

**Solution:** Confirm the account credentials and register an account if necessary.

---

## 7.2 Duplicate Registration

**Problem:** Registration is rejected because information is already in use.

**Possible causes:**

* Email address is already registered.
* Student ID is already registered.

**Solution:** Use the existing account or provide unique registration information.

---

## 7.3 Resource Not Found

**Problem:** A requested resource cannot be found.

**Solution:** Return to the resource list and select an existing resource.

---

## 7.4 Resource Unavailable

**Problem:** A reservation cannot be created for a resource.

**Possible cause:** The resource is currently marked `UNAVAILABLE`.

**Solution:** Select another available resource or wait until the resource becomes available.

---

## 7.5 Invalid Reservation Time

**Problem:** Reservation creation fails because of the selected times.

**Possible causes:**

* Missing time information.
* Invalid date/time format.
* Start time is equal to or later than the end time.

**Solution:** Enter a valid reservation date and ensure the start time occurs before the end time.

---

## 7.6 Unauthorized Operation

**Problem:** The system rejects an operation because the user is not authorized.

**Possible causes:**

* The user is not logged in.
* The user does not own the requested reservation.
* A student is attempting an administrator-only operation.

**Solution:** Log in using the correct account and perform only operations permitted for that account role.

---

## 7.7 Duplicate Check-In

**Problem:** A check-in attempt is rejected because the reservation has already been checked into.

**Solution:** No further check-in is required for that reservation.

---

## 7.8 Production Application Does Not Load

**Problem:** A deployed frontend cannot communicate with the backend.

**Possible causes:**

* Temporary backend availability issue.
* Incorrect frontend environment configuration.
* Network connection problem.

**Solution:**

1. Refresh the application.
2. Confirm that the production application is using the correct deployed URL.
3. Check the backend health endpoint.
4. If the problem persists, report the issue for maintenance.

Production backend health can be checked at:

```text
https://campus-resource-reservation.onrender.com/api/health
```

---

# 8. Security and Account Guidelines

Users should follow normal account security practices.

## 8.1 Password Protection

Users should:

* Keep passwords private.
* Avoid sharing account credentials.
* Avoid storing passwords in publicly accessible documents.
* Use strong passwords.

Passwords are stored by the backend as password hashes rather than plain-text passwords.

## 8.2 Authentication

Protected API operations require JWT authentication.

The frontend maintains authenticated session information using browser local storage.

Users should log out when using a shared or public computer.

## 8.3 Role-Based Access

CampusReserve distinguishes between students and administrators.

Administrator operations are protected from ordinary student accounts.

A student cannot use a normal student account to access administrator-only functionality.

## 8.4 Secrets

Application secrets such as:

* Database credentials
* Flask secret keys
* JWT secret keys

must not be committed to the public source repository.

Production environment configuration is supplied through deployment environment variables.

Frontend `VITE_` configuration values are intended for client-side configuration and must not contain passwords or private secrets.

---

# 9. System Requirements

## 9.1 Student/Administrator Browser

A modern web browser is required.

Recommended browsers include current versions of:

* Google Chrome
* Microsoft Edge
* Mozilla Firefox

An internet connection is required when using the hosted production applications.

## 9.2 Development Environment

For local development, the project uses:

* Python 3.14.2
* Flask 3.1.3
* MySQL Community Server 8.0.46
* Node.js 24.20.0
* npm 11.19.0
* React
* Vite 8.2.2

## 9.3 Database

CampusReserve uses MySQL for persistent application data.

### Local Development Database

The local development database is:

```text
campus_reservation
```

### Production Database

The production database is hosted on Aiven.

The production database configuration is supplied to the backend through the `DATABASE_URL` environment variable.

The application uses the following main tables:

* `users`
* `resources`
* `reservations`
* `check_ins`

---

# 10. Support and Maintenance

## 10.1 Starting the Backend Locally

From the project root:

```cmd
cd backend
venv\Scripts\activate
python run.py
```

The backend should become available at:

```text
http://127.0.0.1:5000
```

The local API is available under:

```text
http://127.0.0.1:5000/api
```

## 10.2 Starting the Student Application

From the project root:

```cmd
cd student-mobile
npm install
npm run dev
```

The frontend should start using the project's configured Vite development port.

For local API communication, the frontend should use:

```text
VITE_API_BASE_URL=http://127.0.0.1:5000/api
```

## 10.3 Starting the Administrator Application

From the project root:

```cmd
cd admin-web
npm install
npm run dev
```

The frontend should start using the project's configured Vite development port.

For local API communication, the frontend should use:

```text
VITE_API_BASE_URL=http://127.0.0.1:5000/api
```

## 10.4 Production Frontend Configuration

The hosted applications use:

```text
VITE_API_BASE_URL=https://campus-resource-reservation.onrender.com/api
```

This configuration is supplied through the Vercel production environment.

The student and administrator applications therefore communicate with the deployed Render backend rather than a local Flask server.

## 10.5 Running Backend Tests

From the backend directory:

```cmd
cd backend
venv\Scripts\activate
python -m pytest --cov=app --cov-report=term-missing -q
```

The current locally verified backend test suite contains:

```text
108 passed
```

The automated tests cover authentication, resources, reservations, check-ins, administration, protected routes, and application setup.

## 10.6 Frontend Quality Checks

From `admin-web`:

```cmd
npm run lint
npm run build
```

From `student-mobile`:

```cmd
npm run lint
npm run build
```

Both frontend linting and production builds have been successfully verified.

## 10.7 Continuous Integration

The repository contains GitHub Actions workflows for:

* Backend testing and coverage.
* Student frontend linting and building.
* Administrator frontend linting and building.

The workflows run automatically for pushes and pull requests.

The backend CI workflow runs the automated pytest suite with coverage reporting.

The frontend CI workflow runs linting and production builds for both frontend applications.

---

# 11. Application API Reference

The frontend applications communicate with the backend through the REST API.

### Production API Base URL

```text
https://campus-resource-reservation.onrender.com/api
```

### Authentication

```text
POST /api/auth/register
POST /api/auth/login
```

### Health

```text
GET /api/health
```

### Resources

```text
GET /api/resources
GET /api/resources/<id>
POST /api/resources
```

### Reservations

```text
POST /api/reservations
GET /api/reservations
GET /api/reservations/<id>
DELETE /api/reservations/<id>
```

### Check-In

```text
POST /api/reservations/<reservation_id>/check-in
GET /api/reservations/<reservation_id>/check-in
POST /api/check-in/<qr_token>
```

### Administration

```text
GET /api/admin/reservations
PUT /api/admin/reservations/<id>/status

PUT /api/admin/resources/<id>
PUT /api/admin/resources/<id>/status
DELETE /api/admin/resources/<id>

GET /api/admin/check-ins
GET /api/admin/users
```

Detailed endpoint information is provided in:

```text
documentation/API.md
```

---

# 12. Related Project Documentation

The following documents provide additional project information:

* `SRS.md` — Software Requirements Specification
* `API.md` — API documentation
* `ARCHITECTURE.md` — System architecture
* `DATABASE.md` — Database design and ERD documentation
* `USER_MANUAL.md` — This user manual
* `UML_USE_CASES.md` — UML use cases
* `UML_ACTIVITY_DIAGRAMS.md` — UML activity diagrams
* `UML_SEQUENCE_DIAGRAMS.md` — UML sequence diagrams
* `UML_CLASS_DIAGRAM.md` — UML class diagram
* `UML_COMPONENT_DIAGRAM.md` — UML component diagram
* `UML_DEPLOYMENT_DIAGRAM.md` — UML deployment diagram

These documents are maintained as part of the CampusReserve project documentation set.

---

# 13. Conclusion

CampusReserve provides a centralized platform for managing campus facility and equipment reservations.

Students can use the system to:

* Register and authenticate.
* Discover campus resources.
* Create reservations.
* View and manage their reservations.
* Cancel eligible reservations.
* Complete reservation check-ins.

Administrators can use the system to:

* Monitor system activity.
* Manage resources.
* Manage reservation statuses.
* Monitor check-ins.
* View registered users.

The system combines:

* React
* Vite
* Flask REST API
* JWT-based authentication
* MySQL
* Vercel
* Render
* Aiven
* GitHub Actions

The production deployment allows the student and administrator applications to communicate with the hosted backend through HTTPS while the backend connects to the production MySQL database.

CampusReserve is therefore available as a complete deployed web application while retaining a local development environment for continued maintenance and development.