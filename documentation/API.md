# CampusReserve API Documentation

## 1. Overview

CampusReserve provides a REST-style HTTP API for managing campus facilities, lab equipment, reservations, and reservation check-ins.

The backend is implemented using Flask and exposes its API under the `/api` prefix.

### Production Base URL

```text
https://campus-resource-reservation.onrender.com/api
```

The production API is hosted on Render and connects to the production MySQL database hosted by Aiven.

### Local Development Base URL

```text
http://127.0.0.1:5000/api
```

The frontend applications use the `VITE_API_BASE_URL` environment variable to select the appropriate API base URL.

---

## 2. System Architecture

The deployed CampusReserve system uses the following architecture:

```text
Student Frontend (Vercel)
        |
        | HTTPS / REST API
        v
Admin Frontend (Vercel) -----> Render Backend (Flask/Gunicorn)
                                      |
                                      | MySQL over SSL
                                      v
                              Aiven MySQL Database
```

### Production Components

| Component              | Platform       | Purpose                                     |
| ---------------------- | -------------- | ------------------------------------------- |
| Student frontend       | Vercel         | Student-facing application                  |
| Administrator frontend | Vercel         | Administrative management portal            |
| Backend API            | Render         | Flask REST API                              |
| Database               | Aiven          | Production MySQL database                   |
| Source control         | GitHub         | Source code and CI/CD                       |
| CI                     | GitHub Actions | Automated backend and frontend verification |

The production frontends communicate with the Render backend over HTTPS.

---

## 3. Technology

The API uses:

* Python 3.14.2
* Flask 3.1.3
* Flask-SQLAlchemy 3.1.1
* Flask-JWT-Extended 4.7.4
* Flask-CORS 6.0.5
* PyMySQL 1.2.0
* MySQL

The local development database uses MySQL Community Server 8.0.46.

The production database is hosted on Aiven and currently runs MySQL 8.4.8.

Authentication is implemented using JSON Web Tokens (JWT).

The production backend is served using Gunicorn.

---

## 4. Authentication

### 4.1 Registration

**Endpoint**

```http
POST /api/auth/register
```

**Purpose**

Creates a new student account.

**Request body**

```json
{
  "name": "Example Student",
  "student_id": "STU100",
  "email": "student@example.com",
  "password": "password"
}
```

Registration validates required account information and prevents duplicate email addresses and student IDs.

Passwords are stored as password hashes rather than plaintext values.

---

### 4.2 Login

**Endpoint**

```http
POST /api/auth/login
```

**Purpose**

Authenticates a registered user and returns a JWT access token.

**Request body**

```json
{
  "email": "student@example.com",
  "password": "password"
}
```

The returned access token is required for protected endpoints.

---

## 5. Authorization

Protected requests use the JWT access token in the HTTP Authorization header.

```http
Authorization: Bearer <access_token>
```

The system distinguishes between:

* `STUDENT`
* `ADMIN`

Administrative endpoints require an authenticated administrator.

A student attempting to access an administrator-only endpoint is rejected.

Ownership checks also prevent students from accessing or modifying another student's private reservations.

---

# 6. Health API

## 6.1 Health Check

```http
GET /api/health
```

**Purpose**

Checks whether the backend API is running.

**Authentication**

Not required.

**Successful response**

```json
{
  "message": "Campus Reservation API is running",
  "success": true
}
```

The production health endpoint is publicly accessible and is used to confirm backend availability.

---

# 7. Resource API

Resources represent campus facilities or equipment that can be reserved.

Supported resource types are:

* `LABORATORY`
* `STUDY_ROOM`
* `EQUIPMENT`

Supported resource statuses are:

* `AVAILABLE`
* `UNAVAILABLE`

---

## 7.1 List Resources

```http
GET /api/resources
```

**Purpose**

Returns the resources available in the system.

**Authentication**

Not required.

---

## 7.2 Get Resource

```http
GET /api/resources/<id>
```

**Purpose**

Returns information for one resource.

**Path parameter**

| Parameter | Description |
| --------- | ----------- |
| `id`      | Resource ID |

**Authentication**

Not required.

If the resource does not exist, the API returns an appropriate not-found response.

---

## 7.3 Create Resource

```http
POST /api/resources
```

**Purpose**

Creates a new campus resource.

**Authentication**

Required.

**Authorization**

Administrator only.

**Request body**

```json
{
  "name": "Computer Lab 3",
  "type": "LABORATORY",
  "description": "Computer laboratory",
  "location": "Main Campus",
  "capacity": 30,
  "status": "AVAILABLE"
}
```

The resource type must be one of the supported resource types.

Capacity must be a valid positive value.

---

# 8. Reservation API

Reservations associate a student with a resource for a specified date and time period.

Supported reservation statuses are:

* `PENDING`
* `CONFIRMED`
* `CANCELLED`
* `COMPLETED`

---

## 8.1 Create Reservation

```http
POST /api/reservations
```

**Purpose**

Creates a reservation for the authenticated student.

**Authentication**

Required.

The reservation request validates:

* Required reservation fields
* Resource existence
* Resource availability
* Reservation date
* Start time
* End time
* Valid chronological ordering of the reservation period

The start time must occur before the end time.

---

## 8.2 List Current User Reservations

```http
GET /api/reservations
```

**Purpose**

Returns reservations belonging to the authenticated user.

**Authentication**

Required.

Students can therefore view their own reservation history without accessing another user's reservations.

---

## 8.3 Get Reservation

```http
GET /api/reservations/<id>
```

**Purpose**

Returns details for a specific reservation.

**Authentication**

Required.

A student can access their own reservation.

Users cannot use this endpoint to access another student's reservation.

---

## 8.4 Cancel Reservation

```http
DELETE /api/reservations/<id>
```

**Purpose**

Cancels a reservation owned by the authenticated student.

**Authentication**

Required.

A reservation cannot be cancelled by another student.

Already-cancelled reservations are handled appropriately by the API.

---

# 9. Check-in API

CampusReserve supports reservation check-in using reservation-specific check-in data and QR/token-based check-in.

A reservation must satisfy the system's check-in requirements before check-in is accepted.

---

## 9.1 Check In to Reservation

```http
POST /api/reservations/<reservation_id>/check-in
```

**Purpose**

Checks the authenticated student into a specific reservation.

**Authentication**

Required.

The endpoint validates reservation ownership and reservation status before creating the check-in record.

Duplicate check-ins are prevented.

---

## 9.2 Get Reservation Check-in

```http
GET /api/reservations/<reservation_id>/check-in
```

**Purpose**

Returns the check-in information associated with a reservation.

**Authentication**

Required.

---

## 9.3 QR/Token Check-in

```http
POST /api/check-in/<qr_token>
```

**Purpose**

Processes check-in using the reservation's QR/token value.

The token identifies the reservation check-in operation.

The endpoint prevents invalid or already-completed check-in operations.

---

# 10. Administrator API

Administrator endpoints provide management functionality for reservations, resources, users, and check-ins.

All administrator endpoints require an authenticated administrator.

---

## 10.1 List All Reservations

```http
GET /api/admin/reservations
```

**Purpose**

Returns reservation information for administrative management.

**Authentication**

Required.

**Authorization**

Administrator only.

---

## 10.2 Update Reservation Status

```http
PUT /api/admin/reservations/<id>/status
```

**Purpose**

Allows an administrator to update the status of a reservation.

**Authentication**

Required.

**Authorization**

Administrator only.

**Request body**

```json
{
  "status": "CONFIRMED"
}
```

The status must be one of the supported reservation statuses.

---

## 10.3 Update Resource

```http
PUT /api/admin/resources/<id>
```

**Purpose**

Updates an existing resource.

**Authentication**

Required.

**Authorization**

Administrator only.

Resource information that can be managed includes the resource's descriptive and operational fields, subject to validation.

---

## 10.4 Update Resource Status

```http
PUT /api/admin/resources/<id>/status
```

**Purpose**

Changes the availability status of an existing resource.

**Authentication**

Required.

**Authorization**

Administrator only.

Supported statuses:

```text
AVAILABLE
UNAVAILABLE
```

---

## 10.5 Delete Resource

```http
DELETE /api/admin/resources/<id>
```

**Purpose**

Removes a resource from the system.

**Authentication**

Required.

**Authorization**

Administrator only.

---

## 10.6 List Check-ins

```http
GET /api/admin/check-ins
```

**Purpose**

Returns check-in records for administrative monitoring.

**Authentication**

Required.

**Authorization**

Administrator only.

---

## 10.7 List Users

```http
GET /api/admin/users
```

**Purpose**

Returns user information for administrative management.

**Authentication**

Required.

**Authorization**

Administrator only.

---

# 11. Endpoint Summary

| Method | Endpoint                                      | Authentication | Access             |
| ------ | --------------------------------------------- | -------------- | ------------------ |
| GET    | `/api/health`                                 | No             | Public             |
| POST   | `/api/auth/register`                          | No             | Public             |
| POST   | `/api/auth/login`                             | No             | Public             |
| GET    | `/api/resources`                              | No             | Public             |
| GET    | `/api/resources/<id>`                         | No             | Public             |
| POST   | `/api/resources`                              | Yes            | Admin              |
| POST   | `/api/reservations`                           | Yes            | Student            |
| GET    | `/api/reservations`                           | Yes            | Student            |
| GET    | `/api/reservations/<id>`                      | Yes            | Owner              |
| DELETE | `/api/reservations/<id>`                      | Yes            | Owner              |
| POST   | `/api/reservations/<reservation_id>/check-in` | Yes            | Student/Owner      |
| GET    | `/api/reservations/<reservation_id>/check-in` | Yes            | Authorized user    |
| POST   | `/api/check-in/<qr_token>`                    | Yes            | Authenticated user |
| GET    | `/api/admin/reservations`                     | Yes            | Admin              |
| PUT    | `/api/admin/reservations/<id>/status`         | Yes            | Admin              |
| PUT    | `/api/admin/resources/<id>`                   | Yes            | Admin              |
| PUT    | `/api/admin/resources/<id>/status`            | Yes            | Admin              |
| DELETE | `/api/admin/resources/<id>`                   | Yes            | Admin              |
| GET    | `/api/admin/check-ins`                        | Yes            | Admin              |
| GET    | `/api/admin/users`                            | Yes            | Admin              |

---

# 12. Common HTTP Responses

The API uses standard HTTP status codes to communicate the result of requests.

| Status | Meaning                                            |
| ------ | -------------------------------------------------- |
| `200`  | Request completed successfully                     |
| `201`  | Resource successfully created                      |
| `400`  | Invalid request or validation failure              |
| `401`  | Authentication required or authentication failed   |
| `403`  | Authenticated user does not have permission        |
| `404`  | Requested resource or record does not exist        |
| `409`  | Request conflicts with an existing record or state |

Exact response bodies depend on the endpoint and error condition.

---

# 13. Validation and Business Rules

The API implements validation at the backend rather than relying only on frontend validation.

Important rules include:

1. Required fields must be supplied.
2. Duplicate user email addresses are rejected.
3. Duplicate student IDs are rejected.
4. Resources must exist before they can be reserved.
5. Resources must be available for reservation.
6. Reservation start time must precede end time.
7. Users can only manage their own student reservations.
8. Administrative operations require administrator authorization.
9. Reservation statuses must use supported values.
10. Resource types must use supported values.
11. Resource capacity must be valid.
12. Duplicate check-ins are prevented.
13. Check-in ownership and reservation status are validated.
14. Invalid resource and reservation IDs are handled without creating invalid records.

---

# 14. Database Entities

The API operates on four primary database entities.

### Users

Stores student and administrator accounts.

Important information includes:

* User ID
* Name
* Student ID
* Email
* Password hash
* Role

### Resources

Stores reservable facilities and equipment.

Important information includes:

* Resource ID
* Name
* Type
* Description
* Location
* Capacity
* Status

### Reservations

Stores bookings made against resources.

Important information includes:

* Reservation ID
* User
* Resource
* Reservation date
* Start time
* End time
* Status

### Check-ins

Stores reservation check-in information.

Important information includes:

* Check-in ID
* Reservation
* Check-in status
* Check-in timestamp
* QR/token information used by the check-in workflow

---

# 15. Client Integration

The student frontend communicates with the API through service modules for:

* Authentication
* Resources
* Reservations
* Check-in

The administrator frontend communicates with the same backend API for administrative operations.

The applications use the Vite environment variable:

```text
VITE_API_BASE_URL
```

### Production configuration

```text
VITE_API_BASE_URL=https://campus-resource-reservation.onrender.com/api
```

### Local development configuration

```text
VITE_API_BASE_URL=http://127.0.0.1:5000/api
```

The local development value can be provided through a frontend `.env` file.

Example configuration files are provided as:

```text
student-mobile/.env.example
admin-web/.env.example
```

The `.env.example` files contain configuration examples only and do not contain secrets.

Vite environment variables prefixed with `VITE_` are client-side configuration values and must not contain passwords, private keys, or other secrets.

---

# 16. Production Deployment

CampusReserve is deployed as a multi-service web application.

### Student Frontend

Hosted on Vercel:

```text
https://campus-resource-reservation.vercel.app/
```

### Administrator Frontend

Hosted on Vercel:

```text
https://campus-resource-reservation-2vz5.vercel.app/
```

### Backend API

Hosted on Render:

```text
https://campus-resource-reservation.onrender.com
```

### Production Database

Hosted on Aiven MySQL.

The production database connection is configured through the backend `DATABASE_URL` environment variable.

Database credentials and cryptographic secrets are not stored in source control.

---

# 17. Security Considerations

The API uses JWT authentication for protected operations.

Security requirements include:

* Passwords must not be stored as plaintext.
* JWT-protected endpoints must validate the access token.
* Administrative endpoints must enforce administrator authorization.
* Users must not be able to access other users' private reservations.
* Environment secrets must remain outside source control.
* Production deployments must use secure secret values.
* Production API communication uses HTTPS.
* Client applications use the deployed API URL in production.
* CORS is restricted to the deployed CampusReserve frontend origins.

The production backend permits requests from:

```text
https://campus-resource-reservation.vercel.app
https://campus-resource-reservation-2vz5.vercel.app
```

No passwords or environment secrets are included in this documentation.

---

# 18. Testing

The backend API has an automated pytest test suite.

### Current verified test result

```text
108 passed
```

The test suite covers:

* Authentication
* Registration
* Login
* Protected routes
* Resource management
* Resource validation
* Reservation creation
* Reservation retrieval
* Reservation cancellation
* Reservation authorization
* Administrator operations
* Check-in
* Duplicate check-in prevention
* Error handling
* Access control

Backend tests are located in:

```text
backend/tests/
```

The backend test suite can be executed with:

```cmd
cd backend
python -m pytest --cov=app --cov-report=term-missing -q
```

The project previously verified approximately 99% application coverage. Coverage should be reported using the output of the coverage-enabled command above rather than assumed from a plain pytest run.

---

# 19. Frontend Testing and Builds

Both frontend applications have automated linting and production build verification.

### Student frontend

```cmd
cd student-mobile
npm run lint
npm run build
```

### Administrator frontend

```cmd
cd admin-web
npm run lint
npm run build
```

Both frontend lint checks and production builds have been successfully verified.

---

# 20. Continuous Integration

Backend CI is configured through:

```text
.github/workflows/backend-ci.yml
```

The workflow:

1. Checks out the repository.
2. Sets up Python.
3. Installs backend dependencies.
4. Runs the pytest suite with coverage reporting.

Frontend CI is configured through:

```text
.github/workflows/frontend-ci.yml
```

The workflow installs dependencies using the committed lock files and runs:

* ESLint
* Production build

for both:

```text
admin-web
student-mobile
```

GitHub Actions has successfully completed the backend and frontend CI workflows for the current project state.

---

# 21. Local Development

## Start the backend

From the backend directory with the virtual environment activated:

```cmd
python run.py
```

The development API is normally available at:

```text
http://127.0.0.1:5000
```

## Start the administrator frontend

From `admin-web`:

```cmd
npm run dev
```

The Vite development server uses the configured local development port.

## Start the student frontend

From `student-mobile`:

```cmd
npm run dev
```

The Vite development server uses the configured local development port.

The frontend development environments should use:

```text
VITE_API_BASE_URL=http://127.0.0.1:5000/api
```

---

# 22. Production Backend Configuration

The Render deployment uses Gunicorn rather than Flask's development server.

The production start command is:

```text
gunicorn run:app
```

Production configuration values are supplied through environment variables, including:

```text
SECRET_KEY
JWT_SECRET_KEY
DATABASE_URL
```

These values must not be committed to Git.

The backend configuration also converts compatible MySQL connection URLs to use the PyMySQL SQLAlchemy driver and removes unsupported `ssl-mode` query parameters before establishing the production database connection.

---

# 23. API Development Principles

Future API changes should follow these principles:

1. Preserve existing verified endpoints unless a requirement requires a change.
2. Preserve existing database relationships.
3. Maintain JWT authentication for protected operations.
4. Maintain role-based authorization.
5. Validate user input on the backend.
6. Return appropriate HTTP status codes.
7. Add automated tests for new behavior.
8. Update this API document when endpoints or contracts change.
9. Do not commit environment secrets.
10. Run the backend test suite before committing backend changes.
11. Verify frontend builds after changing client-side API configuration.
12. Verify production deployment after changes affecting the deployed API or frontend.

---

# 24. Current API Quality Status

The CampusReserve API has been implemented, automated-tested, integrated with both frontend applications, and deployed as a production service.

The current verified backend test suite contains:

```text
108 passing tests
```

The project also has:

* Automated backend CI
* Automated frontend CI
* Student production frontend
* Administrator production frontend
* Production Flask API
* Production MySQL database
* JWT authentication
* Role-based administrator authorization
* Restricted production CORS
* Environment-based frontend API configuration
* HTTPS production communication

The API documentation describes the currently implemented API contract and production integration.

This document should be updated whenever API endpoints, request/response contracts, authentication behavior, deployment architecture, or production configuration changes.

---

# 25. Conclusion

The CampusReserve API provides the backend services required for:

* Student authentication
* Resource discovery and management
* Reservations
* Reservation cancellation
* Reservation check-in
* QR/token-based check-in
* Administrator management
* User management
* Check-in monitoring

The API supports both the CampusReserve student and administrator applications while enforcing authentication, authorization, validation, ownership, and reservation business rules.

The complete system is deployed using Vercel for the frontends, Render for the Flask backend, and Aiven for the production MySQL database.
