# CampusReserve System Architecture

## 1. Overview

CampusReserve is a web-based campus facility and lab equipment reservation system.

The system follows a client-server architecture in which two separate React frontend applications communicate with a centralized Flask REST API backend. The backend manages authentication, authorization, business rules, reservations, resources, check-ins, and database operations.

The system is organized into four major logical components:

1. Student frontend
2. Administrator frontend
3. Flask REST API backend
4. MySQL database

The frontend applications communicate with the backend through HTTP/HTTPS API endpoints and do not access the database directly.

The system is deployed using:

* **Vercel** for the student frontend
* **Vercel** for the administrator frontend
* **Render** for the Flask backend
* **Aiven** for the production MySQL database

The deployed architecture preserves the same logical separation used during local development.

---

## 2. High-Level Architecture

```text
+---------------------------+
|     Student Frontend      |
|       React + Vite        |
|          Vercel           |
+-------------+-------------+
              |
              | HTTPS / JSON / JWT
              |
              v
+---------------------------------------+
|          Flask REST API               |
|             Render                    |
|                                       |
|  +---------------------------------+  |
|  | Authentication & Authorization  |  |
|  | JWT / Role-based Access         |  |
|  +---------------------------------+  |
|                                       |
|  +---------------------------------+  |
|  | Application Routes              |  |
|  | Auth / Resources / Reservations |  |
|  | Check-in / Administration       |  |
|  +---------------------------------+  |
|                                       |
|  +---------------------------------+  |
|  | SQLAlchemy Data Access          |  |
|  | Models / Database Operations    |  |
|  +---------------------------------+  |
+-------------------+-------------------+
                    |
                    | SQL / SSL
                    |
                    v
          +---------------------+
          |    MySQL Database   |
          |       Aiven         |
          |                     |
          | Users               |
          | Resources           |
          | Reservations        |
          | Check-ins           |
          +---------------------+


+---------------------------+
|    Administrator Portal   |
|       React + Vite        |
|          Vercel           |
+-------------+-------------+
              |
              | HTTPS / JSON / JWT
              |
              +-----------------------> Flask REST API
```

Both frontend applications communicate with the same backend API. The backend is the only application component that communicates with the MySQL database.

---

## 3. Architectural Style

CampusReserve uses a **client-server architecture** with a REST-style API and a layered backend structure.

The major separation of responsibilities is:

```text
Presentation Layer
        |
        v
API / Application Layer
        |
        v
Data Access / Model Layer
        |
        v
Database Layer
```

### Presentation Layer

The React applications provide the user interfaces for students and administrators.

### API / Application Layer

Flask routes expose HTTP endpoints and implement authentication, authorization, validation, and application behavior.

### Data Access / Model Layer

Flask-SQLAlchemy provides database abstraction and ORM functionality through the backend models.

### Database Layer

MySQL provides persistent storage for system users, resources, reservations, and check-in records.

---

# 4. System Components

## 4.1 Student Frontend

Location:

```text
student-mobile/
```

Technology:

* React
* Vite
* JavaScript
* npm

The student application provides the student-facing functionality of CampusReserve.

Major functionality includes:

* Student registration
* Student login
* Authentication/token handling
* Resource browsing
* Resource selection
* Reservation creation
* Reservation history
* Reservation cancellation
* Check-in
* Check-in token/QR workflow

The frontend communicates with the backend through service modules.

Relevant service area:

```text
student-mobile/src/services/
```

The service modules handle API communication for:

* Authentication
* Resources
* Reservations
* Check-in

The student frontend does not communicate directly with MySQL.

### Production deployment

The student frontend is deployed on Vercel.

Production URL:

```text
https://campus-resource-reservation.vercel.app/
```

The production API endpoint is configured through:

```text
VITE_API_BASE_URL
```

Production value:

```text
https://campus-resource-reservation.onrender.com/api
```

---

## 4.2 Administrator Frontend

Location:

```text
admin-web/
```

Technology:

* React
* Vite
* JavaScript
* npm
* ESLint

The administrator portal provides administrative management functionality.

The interface includes:

* Dashboard
* Reservations
* Resources
* Check-ins
* Users

Administrators communicate with the same Flask API used by the student application.

Administrative permissions are enforced by the backend rather than relying only on frontend navigation restrictions.

### Production deployment

The administrator frontend is deployed separately on Vercel.

Production URL:

```text
https://campus-resource-reservation-2vz5.vercel.app/
```

The production API endpoint is configured through:

```text
VITE_API_BASE_URL
```

Production value:

```text
https://campus-resource-reservation.onrender.com/api
```

---

# 5. Backend Architecture

Location:

```text
backend/
```

The backend is implemented using Flask.

The application uses the Flask application factory pattern.

The application factory is located at:

```text
backend/app/__init__.py
```

The backend uses:

* Flask
* Flask-SQLAlchemy
* Flask-JWT-Extended
* Flask-CORS
* PyMySQL
* python-dotenv

The production application is served using Gunicorn on Render.

Production API:

```text
https://campus-resource-reservation.onrender.com/api
```

---

# 6. Backend Application Structure

The main backend structure is:

```text
backend/
|
+-- app/
|   |
|   +-- __init__.py
|   +-- config.py
|   |
|   +-- models/
|   |   +-- __init__.py
|   |   +-- user.py
|   |   +-- resource.py
|   |   +-- reservation.py
|   |   +-- check_in.py
|   |
|   +-- routes/
|       +-- health.py
|       +-- auth.py
|       +-- protected.py
|       +-- resource.py
|       +-- reservation.py
|       +-- check_in.py
|       +-- admin.py
|
+-- tests/
|
+-- requirements.txt
+-- pytest.ini
+-- .gitignore
+-- Procfile
+-- run.py
```

---

# 7. Application Factory

The Flask application is created through:

```text
create_app()
```

The application factory:

1. Creates the Flask application.
2. Loads application configuration.
3. Applies optional test configuration.
4. Initializes SQLAlchemy.
5. Initializes JWT management.
6. Configures CORS.
7. Registers the application blueprints.

The same application factory is used by both the running application and the automated test suite.

For testing, the application can use an isolated SQLite database rather than the development or production MySQL database.

This separation improves testability without changing the production database architecture.

---

# 8. API Route Layer

API routes are organized into Flask blueprints.

## Health

```text
app/routes/health.py
```

Provides the API health endpoint:

```text
GET /api/health
```

## Authentication

```text
app/routes/auth.py
```

Handles:

* Registration
* Login
* User authentication

Primary endpoints include:

```text
POST /api/auth/register
POST /api/auth/login
```

## Protected Routes

```text
app/routes/protected.py
```

Contains authenticated route functionality used to verify protected access.

## Resources

```text
app/routes/resource.py
```

Handles resource operations including:

* Resource retrieval
* Resource details
* Resource creation

## Reservations

```text
app/routes/reservation.py
```

Handles:

* Reservation creation
* Reservation listing
* Reservation retrieval
* Reservation cancellation

## Check-in

```text
app/routes/check_in.py
```

Handles:

* Reservation check-in
* Check-in retrieval
* QR/token-based check-in

## Administration

```text
app/routes/admin.py
```

Handles administrative operations involving:

* Reservations
* Resources
* Check-ins
* Users

---

# 9. Authentication Architecture

CampusReserve uses JSON Web Tokens (JWT) for authentication.

The authentication flow is:

```text
Student/Admin
     |
     | Login credentials
     v
POST /api/auth/login
     |
     v
Flask authentication route
     |
     | Credentials validated
     v
JWT access token
     |
     v
Frontend stores authentication session data
     |
     | Authorization: Bearer <token>
     v
Protected API endpoint
     |
     v
JWT validation
     |
     v
Authorized operation
```

JWT authentication protects operations that require an authenticated user.

Role information contained in the authenticated identity is used to distinguish student and administrator access.

---

# 10. Authorization Architecture

CampusReserve uses backend authorization to enforce access control.

The two primary roles are:

```text
STUDENT
ADMIN
```

Student permissions include operations such as:

* Viewing resources
* Creating reservations
* Viewing their reservations
* Cancelling their own reservations
* Performing permitted check-in operations

Administrator permissions include operations such as:

* Managing resources
* Managing reservation statuses
* Viewing reservations
* Viewing check-ins
* Viewing users

Authorization is enforced by the backend so that security does not depend solely on frontend interface restrictions.

---

# 11. Resource Management

Resources represent campus facilities and equipment that can be reserved.

Supported resource types include:

```text
LABORATORY
STUDY_ROOM
EQUIPMENT
```

Supported resource statuses include:

```text
AVAILABLE
UNAVAILABLE
```

The resource route provides resource discovery and creation functionality, while administrative routes provide resource management operations.

The backend validates resource information before persistence.

Resource capacity is also validated.

---

# 12. Reservation Architecture

The reservation workflow connects a student, a resource, and a requested time period.

The general workflow is:

```text
Student
   |
   v
Browse Resources
   |
   v
Select Resource
   |
   v
Submit Reservation
   |
   v
Validate Request
   |
   +---- Resource exists?
   |
   +---- Resource available?
   |
   +---- Date valid?
   |
   +---- Time valid?
   |
   +---- Start before end?
   |
   v
Create Reservation
   |
   v
Reservation Status
```

Supported reservation statuses are:

```text
PENDING
CONFIRMED
CANCELLED
COMPLETED
```

Students can access their own reservations.

Administrative users can manage reservation statuses.

---

# 13. Check-in Architecture

Check-in is associated with a reservation.

The system supports reservation-specific check-in as well as QR/token-based check-in.

The general flow is:

```text
Reservation
     |
     v
Check-in eligibility validation
     |
     v
Check-in request / QR token
     |
     v
Validate reservation and ownership
     |
     v
Check-in record
     |
     v
CHECKED_IN
```

The system prevents duplicate check-ins.

Check-in records are associated with reservations and maintain check-in state and timestamp information.

---

# 14. Data Model

CampusReserve uses four primary entities:

```text
+-------------+
|    USERS    |
+------+------+
       |
       | 1
       |
       | many
       v
+------------------+
|  RESERVATIONS    |
+--------+---------+
         |
         | many
         |
         | 1
         v
+------------------+
|    RESOURCES     |
+------------------+


+------------------+
|  RESERVATIONS    |
+--------+---------+
         |
         | 1
         |
         | 0..1 / associated records
         v
+------------------+
|    CHECK_INS     |
+------------------+
```

The principal relationships are:

* One user can have many reservations.
* One resource can be associated with many reservations.
* A reservation is associated with a user.
* A reservation is associated with a resource.
* A reservation can have an associated check-in record.

---

# 15. User Entity

The `users` table stores system accounts.

Users contain information including:

* User ID
* Name
* Student ID
* Email
* Password hash
* Role

The role determines whether the account operates as a student or administrator.

Passwords are stored using password hashes rather than plaintext passwords.

---

# 16. Resource Entity

The `resources` table stores reservable facilities and equipment.

Resource information includes:

* Resource ID
* Name
* Type
* Description
* Location
* Capacity
* Status

Resources can represent:

* Laboratories
* Study rooms
* Equipment

---

# 17. Reservation Entity

The `reservations` table records resource bookings.

A reservation connects:

```text
User
 |
 +---- Reservation ---- Resource
```

Reservation information includes:

* Reservation ID
* User relationship
* Resource relationship
* Reservation date
* Start time
* End time
* Reservation status

---

# 18. Check-in Entity

The `check_ins` table records reservation check-in information.

A check-in is associated with a reservation.

Check-in information includes:

* Check-in ID
* Reservation relationship
* Check-in status
* Check-in timestamp
* QR/token-related information used by the check-in workflow

This relationship allows the system to determine whether a reservation has been checked in.

---

# 19. Database Architecture

The CampusReserve production database is MySQL hosted by Aiven.

The production database service is:

```text
Aiven MySQL
```

The backend accesses the database through SQLAlchemy and PyMySQL.

The frontend applications never connect directly to the production database.

Database connection configuration is supplied through environment configuration rather than hard-coded credentials.

Important configuration values include:

```text
DATABASE_URL
SECRET_KEY
JWT_SECRET_KEY
```

These values remain outside version control.

The production database uses SSL-secured communication between the Render backend and Aiven MySQL.

The database contains the following primary tables:

```text
users
resources
reservations
check_ins
```

---

# 20. API Communication

The frontends communicate with the backend using HTTP/HTTPS requests.

Data is exchanged using JSON.

The general communication pattern is:

```text
React Component
      |
      v
Frontend Service
      |
      v
HTTP / HTTPS Request
      |
      v
Flask API Route
      |
      v
Validation / Authorization
      |
      v
SQLAlchemy Model
      |
      v
MySQL
      |
      v
JSON Response
      |
      v
Frontend Service
      |
      v
React Interface
```

This separation prevents frontend applications from directly manipulating persistent database records.

---

# 21. Environment-Specific API Configuration

The frontend applications support environment-based API configuration through:

```text
VITE_API_BASE_URL
```

For local development, the fallback API address is:

```text
http://127.0.0.1:5000/api
```

For production, the Vercel deployments use:

```text
https://campus-resource-reservation.onrender.com/api
```

This allows the same frontend codebase to support both local development and production deployment without hard-coding a production-only API address into the application.

---

# 22. Cross-Origin Communication

Flask-CORS is configured in the backend to permit communication from the deployed frontend applications.

The production frontend origins are:

```text
https://campus-resource-reservation.vercel.app
https://campus-resource-reservation-2vz5.vercel.app
```

These origins are explicitly configured in the backend CORS settings.

During local development, the frontend applications run on local development servers and communicate with the local Flask API.

The local backend API is:

```text
http://127.0.0.1:5000/api
```

The frontend applications still communicate through the API rather than directly connecting to MySQL.

---

# 23. Error Handling

Validation and authorization are implemented at the API layer.

The backend handles conditions such as:

* Missing required fields
* Invalid credentials
* Duplicate accounts
* Invalid resource IDs
* Missing resources
* Unavailable resources
* Invalid reservation dates
* Invalid reservation times
* Invalid statuses
* Unauthorized access
* Forbidden administrative operations
* Missing reservations
* Duplicate check-ins

The API communicates request outcomes using HTTP status codes and appropriate response information.

---

# 24. Testing Architecture

The backend has a dedicated automated test suite.

Location:

```text
backend/tests/
```

Testing uses:

* pytest
* pytest-cov
* SQLite in-memory database for isolated application tests

The test application is created through the same Flask application factory used by the application.

This allows route behavior to be tested without requiring the development or production MySQL database.

The verified automated backend test suite currently contains:

```text
108 / 108 tests passing
```

The suite covers areas including:

* Authentication
* Resources
* Reservations
* Check-ins
* Administration
* Authorization
* Validation
* Error handling

A previous project coverage measurement recorded approximately:

```text
99% overall application coverage
```

Coverage can be regenerated using the project's pytest-cov configuration when required.

---

# 25. Continuous Integration Architecture

CampusReserve uses GitHub Actions for automated verification.

## Backend workflow

```text
.github/workflows/backend-ci.yml
```

The backend workflow:

1. Checks out the repository.
2. Installs Python 3.14.
3. Installs backend dependencies.
4. Installs pytest and pytest-cov.
5. Runs the backend automated test suite.
6. Generates coverage output.

The backend workflow runs for repository pushes and pull requests.

## Frontend workflow

```text
.github/workflows/frontend-ci.yml
```

The frontend workflow contains separate jobs for:

```text
admin-web
student-mobile
```

Each frontend job:

1. Checks out the repository.
2. Installs Node.js 24.
3. Uses the corresponding package lock file.
4. Runs `npm ci`.
5. Runs ESLint.
6. Runs the production build.

The CI workflows provide automated verification before and after repository changes.

---

# 26. Project Repository Architecture

The repository is organized as follows:

```text
campus-resource-reservation/
|
+-- admin-web/
|   +-- React administrator application
|
+-- backend/
|   +-- Flask API
|   +-- SQLAlchemy models
|   +-- API routes
|   +-- Automated tests
|
+-- database/
|   +-- Database schema
|   +-- Seed data
|   +-- Deployment database files
|
+-- documentation/
|   +-- SRS.md
|   +-- API.md
|   +-- ARCHITECTURE.md
|   +-- DATABASE.md
|   +-- USER_MANUAL.md
|   +-- UML documentation
|
+-- student-mobile/
|   +-- React student application
|
+-- .github/
    +-- workflows/
        +-- backend-ci.yml
        +-- frontend-ci.yml
```

---

# 27. Production Deployment Architecture

CampusReserve is currently deployed using three cloud services:

* Vercel for the student frontend
* Vercel for the administrator frontend
* Render for the Flask backend
* Aiven for the MySQL database

The production architecture is:

```text
                         Internet
                            |
             +--------------+--------------+
             |                             |
             v                             v
   +-------------------+         +-------------------+
   | Student Frontend  |         | Administrator     |
   | React + Vite      |         | Frontend          |
   | Vercel            |         | React + Vite      |
   +---------+---------+         | Vercel            |
             |                   +---------+---------+
             | HTTPS                       |
             +-------------+---------------+
                           |
                           v
                 +----------------------+
                 | Flask REST API       |
                 | Render               |
                 | Gunicorn             |
                 +----------+-----------+
                            |
                            | SQL / SSL
                            v
                 +----------------------+
                 | MySQL Database       |
                 | Aiven                |
                 +----------------------+
```

### Student production frontend

```text
https://campus-resource-reservation.vercel.app/
```

### Administrator production frontend

```text
https://campus-resource-reservation-2vz5.vercel.app/
```

### Production backend API

```text
https://campus-resource-reservation.onrender.com/api
```

### Production database

```text
Aiven MySQL
```

The production architecture maintains the same application-layer separation as the local development environment.

---

# 28. Deployment Responsibilities

## Vercel

Vercel hosts the two React frontend applications.

The frontend deployments are responsible for serving the built React applications to users.

The frontends communicate with the Render API using HTTPS.

## Render

Render hosts the Flask backend.

The production backend is started using Gunicorn.

The backend is responsible for:

* Authentication
* Authorization
* API processing
* Validation
* Reservation business logic
* Check-in processing
* Database communication

## Aiven

Aiven hosts the production MySQL database.

The database provides persistent storage for:

* Users
* Resources
* Reservations
* Check-ins

The backend connects to the database using the configured database connection string and SSL-secured database communication.

---

# 29. Production Configuration

Production configuration is supplied through environment variables.

Important backend configuration values include:

```text
SECRET_KEY
JWT_SECRET_KEY
DATABASE_URL
```

Frontend production configuration includes:

```text
VITE_API_BASE_URL
```

The production frontend value is:

```text
https://campus-resource-reservation.onrender.com/api
```

Secrets and database credentials are not stored in frontend source code or committed to the repository.

The repository ignores sensitive environment and database certificate files that should not be committed.

---

# 30. Security Boundaries

The system contains several important security boundaries.

### Boundary 1 — Client to API

Frontend applications communicate with the backend through HTTP/HTTPS API requests.

Protected operations require authentication.

Production frontend-to-backend communication uses HTTPS.

### Boundary 2 — API to Authorization

The backend determines whether the authenticated user has permission to perform the requested operation.

JWT identity and role information are used for authorization.

### Boundary 3 — API to Database

Only the backend communicates with the MySQL database.

Frontend applications do not receive database credentials and cannot directly access database tables.

### Boundary 4 — Configuration

Sensitive configuration values are supplied through environment variables and must not be committed to the repository.

### Boundary 5 — Cross-Origin Access

Production CORS is restricted to the known deployed frontend origins.

---

# 31. Local Development Architecture

The project can also be run locally for development and testing.

The local logical architecture is:

```text
+----------------------+
| Student Frontend     |
| React + Vite         |
| localhost             |
+----------+-----------+
           |
           | HTTP / JSON
           v
+----------------------+
| Flask API            |
| 127.0.0.1:5000       |
+----------+-----------+
           |
           | SQL
           v
+----------------------+
| Local MySQL          |
| MySQL 8.0            |
+----------------------+
```

The administrator frontend follows the same pattern:

```text
+----------------------+
| Admin Frontend       |
| React + Vite         |
| localhost             |
+----------+-----------+
           |
           | HTTP / JSON
           v
+----------------------+
| Flask API            |
| 127.0.0.1:5000       |
+----------------------+
```

The local environment is used for development, debugging, automated testing, and maintenance.

The production deployment does not depend on the local MySQL instance.

---

# 32. API and Database Separation

A fundamental architectural principle of CampusReserve is that the frontend applications never communicate directly with the database.

The correct data flow is:

```text
Frontend
   |
   v
REST API
   |
   v
Backend Validation
   |
   v
SQLAlchemy
   |
   v
MySQL
```

The following direct connection is not permitted:

```text
Frontend --------X--------> MySQL
```

This separation centralizes business rules, authentication, authorization, validation, and database access in the backend.

---

# 33. Authentication and Data Flow

A typical authenticated operation follows this sequence:

```text
1. User opens frontend
        |
        v
2. User submits credentials
        |
        v
3. Frontend sends login request
        |
        v
4. Flask validates credentials
        |
        v
5. Flask generates JWT
        |
        v
6. Frontend stores authentication data
        |
        v
7. Frontend sends Bearer token
        |
        v
8. Flask validates JWT
        |
        v
9. Backend checks authorization
        |
        v
10. Backend performs requested operation
        |
        v
11. SQLAlchemy communicates with MySQL
        |
        v
12. Flask returns JSON response
        |
        v
13. Frontend updates the interface
```

---

# 34. Reservation Data Flow

The reservation data flow is:

```text
Student
   |
   v
Student Frontend
   |
   | POST /api/reservations
   v
Flask Reservation Route
   |
   v
Authentication
   |
   v
Validation
   |
   +---- Resource validation
   |
   +---- Date validation
   |
   +---- Time validation
   |
   v
Reservation Model
   |
   v
MySQL
   |
   v
Reservation Response
   |
   v
Student Frontend
```

Administrative reservation management follows the same backend architecture but requires administrator authorization.

---

# 35. Check-in Data Flow

The check-in data flow is:

```text
Student
   |
   v
Reservation
   |
   v
Check-in request / token
   |
   v
Flask Check-in Route
   |
   v
JWT / Ownership Validation
   |
   v
Check-in Eligibility
   |
   v
Check-in Record
   |
   v
MySQL
   |
   v
Check-in Response
   |
   v
Frontend
```

The system prevents duplicate check-ins for the same reservation.

Administrators can view check-in records through the administrator application.

---

# 36. Architectural Decisions

The following architectural decisions are established and should be preserved unless a documented project requirement requires a change.

### Decision 1 — Flask REST API

Flask provides the backend HTTP API.

### Decision 2 — React Frontends

React and Vite are used for the student and administrator interfaces.

### Decision 3 — SQLAlchemy ORM

Flask-SQLAlchemy provides database interaction through application models.

### Decision 4 — MySQL

MySQL is the persistent application database.

The production MySQL database is hosted on Aiven.

### Decision 5 — JWT Authentication

JWT is used for authenticated API access.

### Decision 6 — Role-Based Authorization

Student and administrator roles provide different levels of access.

### Decision 7 — Separate Frontends

The student and administrator applications are maintained as separate frontend projects while sharing the backend API.

### Decision 8 — Automated Testing

Backend behavior is verified through pytest tests, while frontend quality is checked through linting and production builds.

### Decision 9 — Cloud Deployment

The production frontend applications are deployed on Vercel, the Flask backend is deployed on Render, and the MySQL database is hosted on Aiven.

### Decision 10 — Environment-Based Configuration

Environment variables are used to configure database connections, application secrets, JWT secrets, and frontend API endpoints.

---

# 37. Architectural Constraints

The following constraints apply to the current implementation:

1. The frontend must communicate through the backend API.
2. The frontend must not connect directly to MySQL.
3. Protected backend operations require JWT authentication.
4. Administrator operations require administrator authorization.
5. Existing API contracts should not be changed unnecessarily.
6. Existing database relationships should be preserved.
7. Backend changes should include appropriate automated tests.
8. Environment secrets must not be committed.
9. CI workflows should continue to validate backend and frontend changes.
10. Production frontend applications must communicate with the deployed backend API.
11. Production database credentials must remain server-side.
12. Production cross-origin access should remain restricted to the authorized frontend origins.

---

# 38. Deployment and Operational Status

The production architecture is currently implemented and operational.

The deployed components are:

```text
Student Frontend
    |
    +-- Vercel
    |
    +-- https://campus-resource-reservation.vercel.app/


Administrator Frontend
    |
    +-- Vercel
    |
    +-- https://campus-resource-reservation-2vz5.vercel.app/


Backend API
    |
    +-- Render
    |
    +-- https://campus-resource-reservation.onrender.com/api


Database
    |
    +-- Aiven MySQL
```

The production system has been manually exercised through the student and administrator applications.

Verified production functionality includes:

* Student login
* Student resource access
* Student reservations
* Reservation cancellation
* Student check-in
* Administrator login
* Administrator dashboard
* Administrator reservation viewing
* Administrator resource viewing
* Administrator check-in viewing
* Administrator user viewing
* Student-to-backend-to-administrator reservation flow

---

# 39. Current Architecture Status

The CampusReserve architecture is implemented and operational for the current project scope.

The system currently provides:

* Student-facing reservation functionality
* Administrator management functionality
* REST API communication
* JWT authentication
* Role-based authorization
* MySQL persistence
* Resource management
* Reservation management
* Reservation cancellation
* Reservation check-in
* QR/token-based check-in
* Automated backend testing
* Frontend linting
* Frontend production builds
* GitHub Actions continuous integration
* Production frontend deployment
* Production backend deployment
* Production MySQL database hosting
* Environment-based production configuration
* Restricted production CORS

The verified backend automated test suite currently contains:

```text
108 / 108 tests passing
```

A previous project coverage measurement recorded approximately:

```text
99% overall application coverage
```

The production deployment is operational and uses the following architecture:

```text
Vercel
   |
   v
Render
   |
   v
Aiven MySQL
```

---

# 40. Conclusion

CampusReserve uses a modular client-server architecture that separates presentation, API processing, data access, and persistent storage.

The student and administrator applications are maintained as independent React/Vite frontends while sharing a centralized Flask REST API.

The backend centralizes authentication, authorization, validation, reservation processing, check-in processing, and database access.

The production system is deployed using Vercel for the frontend applications, Render for the Flask API, and Aiven for the MySQL database. This deployment preserves the same logical architecture used during local development while providing a publicly accessible production system.

The architecture is suitable for the current academic project scope and provides a maintainable foundation for continued testing, demonstration, and future enhancement without requiring a fundamental architectural redesign.
