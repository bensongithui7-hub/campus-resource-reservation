\# CampusReserve System Architecture



\## 1. Overview



CampusReserve is a web-based campus facility and lab equipment reservation system.



The system follows a client-server architecture in which two React frontend applications communicate with a Flask REST API backend. The backend manages authentication, authorization, business rules, reservations, resources, check-ins, and database operations.



The primary system components are:



1\. Student frontend

2\. Administrator frontend

3\. Flask REST API backend

4\. MySQL database



The architecture is organized so that frontend applications communicate with the backend through HTTP API endpoints rather than accessing the database directly.



\---



\## 2. High-Level Architecture



```text

+---------------------------+

|     Student Frontend      |

|       React + Vite        |

+-------------+-------------+

&#x20;             |

&#x20;             | HTTP / JSON / JWT

&#x20;             |

&#x20;             v

+---------------------------------------+

|          Flask REST API               |

|                                       |

|  +---------------------------------+  |

|  | Authentication \& Authorization   |  |

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

&#x20;                   |

&#x20;                   | SQL

&#x20;                   |

&#x20;                   v

&#x20;         +---------------------+

&#x20;         |    MySQL Database   |

&#x20;         |                     |

&#x20;         | Users               |

&#x20;         | Resources           |

&#x20;         | Reservations        |

&#x20;         | Check-ins           |

&#x20;         +---------------------+



+---------------------------+

|    Administrator Portal   |

|       React + Vite        |

+-------------+-------------+

&#x20;             |

&#x20;             | HTTP / JSON / JWT

&#x20;             |

&#x20;             +-----------------------> Flask REST API

```



\---



\## 3. Architectural Style



CampusReserve uses a client-server architecture with a REST-style API.



The major separation of responsibilities is:



```text

Presentation Layer

&#x20;       |

&#x20;       v

API / Application Layer

&#x20;       |

&#x20;       v

Data Access / Model Layer

&#x20;       |

&#x20;       v

Database Layer

```



\### Presentation Layer



The React applications provide the user interfaces for students and administrators.



\### API / Application Layer



Flask routes expose HTTP endpoints and implement authentication, authorization, validation, and application behavior.



\### Data Access / Model Layer



Flask-SQLAlchemy provides the database abstraction and ORM functionality used by the backend models.



\### Database Layer



MySQL provides persistent storage for system users, resources, reservations, and check-in records.



\---



\# 4. System Components



\## 4.1 Student Frontend



Location:



```text

student-mobile/

```



Technology:



\* React

\* Vite

\* JavaScript

\* npm



The student application provides the student-facing functionality of CampusReserve.



Major functionality includes:



\* Student registration

\* Student login

\* Session/token handling

\* Resource browsing

\* Resource selection

\* Reservation creation

\* Reservation history

\* Reservation cancellation

\* Check-in

\* Check-in token/QR workflow



The frontend communicates with the backend through service modules.



Relevant service areas include:



```text

student-mobile/src/services/

```



These services handle API communication for:



\* Authentication

\* Resources

\* Reservations

\* Check-in



The frontend does not communicate directly with MySQL.



\---



\## 4.2 Administrator Frontend



Location:



```text

admin-web/

```



Technology:



\* React

\* Vite

\* JavaScript

\* npm

\* ESLint



The administrator portal provides administrative management functionality.



The interface includes areas for:



\* Dashboard

\* Reservations

\* Resources

\* Check-ins

\* Users



Administrators communicate with the same Flask API used by the student application.



Administrative permissions are enforced by the backend rather than relying only on frontend navigation restrictions.



\---



\# 5. Backend Architecture



Location:



```text

backend/

```



The backend is implemented using Flask.



The application uses an application factory:



```text

backend/app/\_\_init\_\_.py

```



The application factory creates the Flask application, initializes extensions, and registers the API blueprints.



The backend uses:



\* Flask

\* Flask-SQLAlchemy

\* Flask-JWT-Extended

\* Flask-CORS

\* PyMySQL

\* python-dotenv



\---



\# 6. Backend Application Structure



The main backend structure is:



```text

backend/

|

+-- app/

|   |

|   +-- \_\_init\_\_.py

|   +-- config.py

|   |

|   +-- models/

|   |   +-- \_\_init\_\_.py

|   |   +-- user.py

|   |   +-- resource.py

|   |   +-- reservation.py

|   |   +-- check\_in.py

|   |

|   +-- routes/

|       +-- health.py

|       +-- auth.py

|       +-- protected.py

|       +-- resource.py

|       +-- reservation.py

|       +-- check\_in.py

|       +-- admin.py

|

+-- tests/

|

+-- requirements.txt

+-- pytest.ini

+-- .gitignore

+-- run.py

```



\---



\# 7. Application Factory



The Flask application is created through:



```text

create\_app()

```



The factory:



1\. Creates the Flask application.

2\. Loads the application configuration.

3\. Applies optional test configuration.

4\. Initializes SQLAlchemy.

5\. Initializes JWT management.

6\. Enables CORS.

7\. Registers the application blueprints.



The optional test configuration allows the automated test suite to use an isolated SQLite database instead of the development MySQL database.



This separation improves testability without changing the production database architecture.



\---



\# 8. API Route Layer



API routes are organized into Flask blueprints.



\## Health



```text

app/routes/health.py

```



Provides the API health endpoint.



\## Authentication



```text

app/routes/auth.py

```



Handles:



\* Registration

\* Login

\* User authentication



\## Protected Routes



```text

app/routes/protected.py

```



Contains authenticated route functionality used to verify protected access.



\## Resources



```text

app/routes/resource.py

```



Handles resource retrieval and resource creation.



\## Reservations



```text

app/routes/reservation.py

```



Handles:



\* Reservation creation

\* Reservation listing

\* Reservation retrieval

\* Reservation cancellation



\## Check-in



```text

app/routes/check\_in.py

```



Handles:



\* Reservation check-in

\* Check-in retrieval

\* QR/token check-in



\## Administration



```text

app/routes/admin.py

```



Handles administrative operations involving:



\* Reservations

\* Resources

\* Check-ins

\* Users



\---



\# 9. Authentication Architecture



CampusReserve uses JSON Web Tokens (JWT) for authentication.



The authentication flow is:



```text

Student/Admin

&#x20;    |

&#x20;    | Login credentials

&#x20;    v

POST /api/auth/login

&#x20;    |

&#x20;    v

Flask authentication route

&#x20;    |

&#x20;    | Credentials validated

&#x20;    v

JWT access token

&#x20;    |

&#x20;    v

Frontend stores authenticated session data

&#x20;    |

&#x20;    | Authorization: Bearer <token>

&#x20;    v

Protected API endpoint

&#x20;    |

&#x20;    v

JWT validation

&#x20;    |

&#x20;    v

Authorized operation

```



JWT authentication protects operations that require an authenticated user.



Role information is used to distinguish student and administrator access.



\---



\# 10. Authorization Architecture



CampusReserve uses backend authorization to enforce access control.



The two primary roles are:



```text

STUDENT

ADMIN

```



Student permissions include operations such as:



\* Viewing resources

\* Creating reservations

\* Viewing their reservations

\* Cancelling their own reservations

\* Performing permitted check-in operations



Administrator permissions include operations such as:



\* Managing resources

\* Managing reservation statuses

\* Viewing reservations

\* Viewing check-ins

\* Viewing users



Authorization is enforced by the backend so that security does not depend solely on the frontend interface.



\---



\# 11. Resource Management



Resources represent campus facilities and equipment that can be reserved.



Supported resource types are:



```text

LABORATORY

STUDY\_ROOM

EQUIPMENT

```



Supported resource statuses are:



```text

AVAILABLE

UNAVAILABLE

```



The resource route provides resource discovery and creation functionality, while administrative routes provide resource management operations.



The backend validates resource information before persistence.



Resource capacity is also validated.



\---



\# 12. Reservation Architecture



The reservation workflow connects a student, a resource, and a requested time period.



The general workflow is:



```text

Student

&#x20;  |

&#x20;  v

Browse Resources

&#x20;  |

&#x20;  v

Select Resource

&#x20;  |

&#x20;  v

Submit Reservation

&#x20;  |

&#x20;  v

Validate Request

&#x20;  |

&#x20;  +---- Resource exists?

&#x20;  |

&#x20;  +---- Resource available?

&#x20;  |

&#x20;  +---- Date valid?

&#x20;  |

&#x20;  +---- Time valid?

&#x20;  |

&#x20;  +---- Start before end?

&#x20;  |

&#x20;  v

Create Reservation

&#x20;  |

&#x20;  v

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



\---



\# 13. Check-in Architecture



Check-in is associated with a reservation.



The system supports reservation-specific check-in as well as QR/token-based check-in.



General flow:



```text

Reservation

&#x20;    |

&#x20;    v

Check-in eligibility validation

&#x20;    |

&#x20;    v

Check-in request / QR token

&#x20;    |

&#x20;    v

Validate reservation and ownership

&#x20;    |

&#x20;    v

Check-in record

&#x20;    |

&#x20;    v

CHECKED\_IN

```



The system prevents duplicate check-ins.



Check-in records are associated with reservations and maintain check-in state and timestamp information.



\---



\# 14. Data Model



CampusReserve uses four primary entities.



```text

+-------------+

|    USERS    |

+------+------+

&#x20;      |

&#x20;      | 1

&#x20;      |

&#x20;      | many

&#x20;      v

+------------------+

|  RESERVATIONS    |

+--------+---------+

&#x20;        |

&#x20;        | many

&#x20;        |

&#x20;        | 1

&#x20;        v

+------------------+

|    RESOURCES     |

+------------------+



+------------------+

|  RESERVATIONS    |

+--------+---------+

&#x20;        |

&#x20;        | 1

&#x20;        |

&#x20;        | 0..1 / associated records

&#x20;        v

+------------------+

|    CHECK\_INS     |

+------------------+

```



\---



\# 15. User Entity



The `users` table stores system accounts.



Users contain information including:



\* User ID

\* Name

\* Student ID

\* Email

\* Password hash

\* Role



The role determines whether the account operates as a student or administrator.



Passwords are stored using password hashes rather than plaintext passwords.



\---



\# 16. Resource Entity



The `resources` table stores reservable facilities and equipment.



Resource information includes:



\* Resource ID

\* Name

\* Type

\* Description

\* Location

\* Capacity

\* Status



Resources can be:



\* Laboratories

\* Study rooms

\* Equipment



\---



\# 17. Reservation Entity



The `reservations` table records resource bookings.



A reservation connects:



```text

User

&#x20; |

&#x20; +---- Reservation ---- Resource

```



Reservation information includes:



\* Reservation ID

\* User relationship

\* Resource relationship

\* Reservation date

\* Start time

\* End time

\* Reservation status



\---



\# 18. Check-in Entity



The `check\_ins` table records reservation check-in information.



A check-in is associated with a reservation.



Check-in information includes:



\* Check-in ID

\* Reservation relationship

\* Check-in status

\* Check-in timestamp

\* QR/token-related information used by the check-in workflow



This relationship allows the system to determine whether a reservation has been checked in.



\---



\# 19. Database Architecture



The production/development backend uses MySQL.



Database name:



```text

campus\_reservation

```



The backend accesses MySQL through SQLAlchemy and PyMySQL.



The application does not expose database credentials to the frontend.



Database connection configuration is supplied through environment configuration rather than hard-coded credentials.



The environment configuration includes values such as:



```text

DATABASE\_URL

SECRET\_KEY

JWT\_SECRET\_KEY

```



These values must remain outside version control.



\---



\# 20. API Communication



The frontends communicate with the backend using HTTP requests.



Data is exchanged using JSON.



The general communication pattern is:



```text

React Component

&#x20;     |

&#x20;     v

Frontend Service

&#x20;     |

&#x20;     v

HTTP Request

&#x20;     |

&#x20;     v

Flask API Route

&#x20;     |

&#x20;     v

Validation / Authorization

&#x20;     |

&#x20;     v

SQLAlchemy Model

&#x20;     |

&#x20;     v

MySQL

&#x20;     |

&#x20;     v

JSON Response

&#x20;     |

&#x20;     v

Frontend Service

&#x20;     |

&#x20;     v

React Interface

```



This separation prevents frontend applications from directly manipulating persistent database records.



\---



\# 21. Cross-Origin Communication



Flask-CORS is enabled by the backend to support communication between the local frontend development servers and the Flask API.



During local development, the applications run on separate development ports.



The backend API is available at:



```text

http://127.0.0.1:5000/api

```



The frontends communicate with this API rather than directly connecting to MySQL.



\---



\# 22. Error Handling



Validation and authorization are implemented at the API layer.



The backend handles conditions such as:



\* Missing required fields

\* Invalid credentials

\* Duplicate accounts

\* Invalid resource IDs

\* Missing resources

\* Unavailable resources

\* Invalid reservation dates

\* Invalid reservation times

\* Invalid statuses

\* Unauthorized access

\* Forbidden administrative operations

\* Missing reservations

\* Duplicate check-ins



The API communicates request outcomes using HTTP status codes and appropriate response information.



\---



\# 23. Testing Architecture



The backend has a dedicated automated test suite.



Location:



```text

backend/tests/

```



Testing uses:



\* pytest

\* pytest-cov

\* SQLite in-memory database for isolated application tests



The test application is created through the same Flask application factory used by the application.



This allows route behavior to be tested without requiring the development MySQL database.



The verified suite currently contains:



```text

108 passing tests

99% overall application coverage

```



The test suite covers authentication, resources, reservations, check-ins, administration, authorization, validation, and error handling.



\---



\# 24. Continuous Integration Architecture



CampusReserve uses GitHub Actions for automated verification.



Backend workflow:



```text

.github/workflows/backend-ci.yml

```



The backend workflow:



1\. Checks out the repository.

2\. Installs Python 3.14.

3\. Installs backend dependencies.

4\. Installs pytest and pytest-cov.

5\. Runs the backend automated test suite.

6\. Generates coverage output.



Frontend workflow:



```text

.github/workflows/frontend-ci.yml

```



The frontend workflow contains jobs for:



```text

admin-web

student-mobile

```



Each frontend job:



1\. Checks out the repository.

2\. Installs Node.js 24.

3\. Uses the corresponding package lock file.

4\. Runs `npm ci`.

5\. Runs ESLint.

6\. Runs the production build.



\---



\# 25. Project Repository Architecture



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

|   +-- Database schema and database-related files

|

+-- documentation/

|   +-- SRS.md

|   +-- API.md

|   +-- ARCHITECTURE.md

|

+-- student-mobile/

|   +-- React student application

|

+-- .github/

&#x20;   +-- workflows/

&#x20;       +-- backend-ci.yml

&#x20;       +-- frontend-ci.yml

```



\---



\# 26. Deployment Architecture



A production deployment should preserve the same logical architecture:



```text

&#x20;                   Internet

&#x20;                      |

&#x20;                      v

&#x20;             +----------------+

&#x20;             | Student Client |

&#x20;             +-------+--------+

&#x20;                     |

&#x20;                     |

&#x20;             +-------v--------+

&#x20;             | Admin Client   |

&#x20;             +-------+--------+

&#x20;                     |

&#x20;                     | HTTPS

&#x20;                     v

&#x20;            +------------------+

&#x20;            |  Flask API       |

&#x20;            |  Application     |

&#x20;            +--------+---------+

&#x20;                     |

&#x20;                     | SQL

&#x20;                     v

&#x20;            +------------------+

&#x20;            |  MySQL Database  |

&#x20;            +------------------+

```



For deployment:



\* The Flask API should run on a production-capable server.

\* The MySQL database should be securely hosted.

\* HTTPS should be used.

\* Production secrets must be supplied through secure environment configuration.

\* Frontend API configuration must point to the deployed backend.

\* Database credentials must never be placed in frontend source code.



\---



\# 27. Security Boundaries



The system contains several important security boundaries.



\### Boundary 1 — Client to API



All protected requests require authentication.



\### Boundary 2 — API to Authorization



The backend determines whether the authenticated user has permission to perform the requested operation.



\### Boundary 3 — API to Database



Only the backend communicates with the database.



\### Boundary 4 — Configuration



Sensitive configuration values are supplied through environment variables and must not be committed to the repository.



\---



\# 28. Architectural Decisions



The following architectural decisions are established and should be preserved unless a documented project requirement requires change.



\### Decision 1 — Flask REST API



Flask provides the backend HTTP API.



\### Decision 2 — React Frontends



React and Vite are used for the student and administrator interfaces.



\### Decision 3 — SQLAlchemy ORM



Flask-SQLAlchemy provides database interaction through application models.



\### Decision 4 — MySQL



MySQL is the persistent production/development database.



\### Decision 5 — JWT Authentication



JWT is used for authenticated API access.



\### Decision 6 — Role-Based Authorization



Student and administrator roles provide different levels of access.



\### Decision 7 — Separate Frontends



The student and administrator applications are maintained as separate frontend projects while sharing the backend API.



\### Decision 8 — Automated Testing



Backend behavior is verified through pytest tests, while frontend quality is checked through linting and production builds.



\---



\# 29. Architectural Constraints



The following constraints apply to the current implementation:



1\. The frontend must communicate through the backend API.

2\. The frontend must not connect directly to MySQL.

3\. Protected backend operations require JWT authentication.

4\. Administrator operations require administrator authorization.

5\. Existing API contracts should not be changed unnecessarily.

6\. Existing database relationships should be preserved.

7\. Backend changes should include appropriate automated tests.

8\. Environment secrets must not be committed.

9\. CI workflows should continue to validate backend and frontend changes.



\---



\# 30. Current Architecture Status



The CampusReserve architecture is implemented and operational for the current project scope.



The system currently provides:



\* Student-facing reservation functionality

\* Administrator management functionality

\* REST API communication

\* JWT authentication

\* Role-based authorization

\* MySQL persistence

\* Resource management

\* Reservation management

\* Reservation check-in

\* Automated backend testing

\* Frontend linting and production builds

\* GitHub Actions continuous integration



The current backend test suite contains 108 passing tests with 99% overall application coverage.



\---



\# 31. Conclusion



CampusReserve uses a modular client-server architecture that separates presentation, API processing, data access, and persistent storage.



The architecture supports independent development of the student and administrator interfaces while maintaining a centralized backend for authentication, authorization, business rules, and data management.



The design is suitable for the current academic project scope and provides a foundation for future deployment and maintenance without requiring a fundamental architectural redesign.



