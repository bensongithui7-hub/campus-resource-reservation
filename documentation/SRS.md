\# CampusReserve



\## Software Requirements Specification (SRS)



\*\*Project:\*\* Campus Smart Facility \& Lab Equipment Reservation System

\*\*System Name:\*\* CampusReserve

\*\*Course:\*\* IBL 3300 — Software Engineering Studio

\*\*Institution:\*\* Technical University of Kenya

\*\*Document Version:\*\* 1.0

\*\*Status:\*\* Final Project Documentation Draft

\*\*Date:\*\* September 2026



\---



\## 1. Introduction



\### 1.1 Purpose



This Software Requirements Specification defines the requirements, scope, users, interfaces, constraints, and functional behaviour of CampusReserve, a campus facility and laboratory equipment reservation system.



CampusReserve provides a centralized system through which students can view available campus resources, make reservations, manage their reservations, and complete reservation check-ins. Administrative users can manage resources, reservations, users, and check-in information through an administrative web portal.



This document describes the system as implemented and is intended to provide a consistent reference for development, testing, deployment, maintenance, demonstration, and evaluation.



\### 1.2 Scope



CampusReserve is a web-based campus resource reservation system consisting of:



\* A Flask-based REST API backend.

\* A student-facing React application.

\* An administrator-facing React web application.

\* A MySQL relational database for production use.

\* JWT-based authentication and role-based authorization.

\* Reservation management.

\* Resource management.

\* Reservation check-in functionality using QR/token-based check-in.

\* Automated backend testing.

\* Continuous integration workflows for backend and frontend applications.



The system supports three resource categories:



\* Laboratory resources.

\* Study rooms.

\* Equipment.



The system is designed to reduce manual resource-booking processes and provide students and administrators with a centralized mechanism for managing campus resource usage.



\### 1.3 Intended Audience



This document is intended for:



\* Students using CampusReserve.

\* System administrators.

\* Developers and maintainers.

\* Software engineering lecturers and project assessors.

\* Testers and quality-assurance personnel.

\* Deployment and infrastructure personnel.

\* Future developers extending the system.



\### 1.4 Definitions and Abbreviations



| Term          | Meaning                                                         |

| ------------- | --------------------------------------------------------------- |

| CampusReserve | Campus Smart Facility \& Lab Equipment Reservation System        |

| API           | Application Programming Interface                               |

| REST          | Representational State Transfer                                 |

| JWT           | JSON Web Token                                                  |

| UI            | User Interface                                                  |

| CRUD          | Create, Read, Update, Delete                                    |

| SRS           | Software Requirements Specification                             |

| CI            | Continuous Integration                                          |

| QR            | Quick Response                                                  |

| DB            | Database                                                        |

| Student       | A normal system user who can reserve resources                  |

| Administrator | A privileged user who manages system resources and reservations |

| Resource      | A reservable campus facility or item                            |

| Reservation   | A booking made by a student for a resource                      |

| Check-in      | Confirmation that a student has arrived for a reservation       |



\---



\# 2. Overall Description



\## 2.1 Product Perspective



CampusReserve is a client-server application.



The system consists of three major application layers:



1\. \*\*Presentation layer\*\*



&#x20;  \* Student React/Vite application.

&#x20;  \* Administrator React/Vite application.



2\. \*\*Application/API layer\*\*



&#x20;  \* Python Flask REST API.

&#x20;  \* JWT authentication and authorization.

&#x20;  \* Business logic for resources, reservations, and check-ins.



3\. \*\*Data layer\*\*



&#x20;  \* MySQL database in the production environment.

&#x20;  \* SQLAlchemy ORM for database interaction.



The applications communicate with the backend through HTTP API requests.



The backend API is exposed under the `/api` prefix.



\## 2.2 System Architecture



The implemented architecture can be summarized as:



```text

+-----------------------+

|   Student Frontend    |

|     React + Vite      |

+-----------+-----------+

&#x20;           |

&#x20;           | HTTP/REST

&#x20;           v

+-----------------------+

|      Flask API        |

| Authentication        |

| Resources             |

| Reservations          |

| Check-ins             |

| Administration        |

+-----------+-----------+

&#x20;           |

&#x20;           | SQLAlchemy

&#x20;           v

+-----------------------+

|    MySQL Database     |

| Users                 |

| Resources             |

| Reservations          |

| Check-ins             |

+-----------------------+



+-----------------------+

|    Admin Frontend     |

|     React + Vite      |

+-----------+-----------+

&#x20;           |

&#x20;           | HTTP/REST

&#x20;           v

&#x20;       Flask API

```



\## 2.3 Product Functions



The major functions of CampusReserve are:



\### Student functions



\* Student registration.

\* Student login.

\* Authenticated session management.

\* View available resources.

\* View individual resource information.

\* Create reservations.

\* View personal reservations.

\* View individual reservations.

\* Cancel reservations.

\* Check in to confirmed reservations.

\* View check-in information.



\### Administrator functions



\* Administrator authentication.

\* View reservations.

\* View check-ins.

\* View users.

\* Create resources.

\* Update resources.

\* Delete resources.

\* Change resource status.

\* Change reservation status.



\### System functions



\* Authentication using JWT.

\* Role-based authorization.

\* Resource availability enforcement.

\* Reservation validation.

\* Reservation ownership enforcement.

\* Check-in validation.

\* Duplicate check-in protection.

\* REST API communication.

\* Automated backend testing.

\* Continuous integration testing.



\---



\# 3. User Classes and Characteristics



\## 3.1 Student



Students are normal authenticated users of the system.



Students can:



\* Register an account.

\* Log into the system.

\* Browse resources.

\* Make reservations.

\* View their reservations.

\* Cancel eligible reservations.

\* Check in for confirmed reservations.



Students cannot perform administrator-only operations.



\## 3.2 Administrator



Administrators are privileged users responsible for managing system resources and reservation information.



Administrators can:



\* Access administrative functionality.

\* View system reservations.

\* View check-ins.

\* View users.

\* Create resources.

\* Modify resources.

\* Delete resources.

\* Change resource availability.

\* Change reservation status.



Administrator-only endpoints reject requests from normal students.



\---



\# 4. Functional Requirements



\## 4.1 Authentication and Registration



\### FR-01: Student Registration



The system shall allow a new student to create an account.



Registration requires the appropriate user information, including:



\* Name.

\* Student ID.

\* Email.

\* Password.



The system shall reject registration when required information is missing.



The system shall prevent duplicate email addresses.



The system shall prevent duplicate student IDs.



\### FR-02: User Login



The system shall authenticate registered users using their email and password.



A successful login shall provide a JWT access token and authenticated user information.



Invalid login credentials shall be rejected.



\### FR-03: Protected Resources



The system shall require authentication for protected operations.



Unauthenticated requests to protected endpoints shall be rejected.



\### FR-04: Role-Based Authorization



The system shall distinguish between student and administrator users.



Administrator-only operations shall reject unauthorized student requests.



\---



\# 5. Resource Management Requirements



\## 5.1 Resource Categories



The system shall support the following resource types:



\* `LABORATORY`

\* `STUDY\_ROOM`

\* `EQUIPMENT`



\## 5.2 Resource Status



Resources shall support the following statuses:



\* `AVAILABLE`

\* `UNAVAILABLE`



\## 5.3 Resource Listing



\### FR-05



The system shall allow users to retrieve the list of resources.



\### FR-06



The system shall allow users to retrieve details for an individual resource.



\### FR-07



The system shall prevent reservations against resources that are unavailable.



\## 5.4 Resource Creation



\### FR-08



An administrator shall be able to create a resource.



A resource contains information such as:



\* Name.

\* Type.

\* Description.

\* Location.

\* Capacity.

\* Status.



\## 5.5 Resource Updating



\### FR-09



An administrator shall be able to update an existing resource.



The system shall validate resource information including:



\* Resource type.

\* Capacity.

\* Status.



The system shall reject invalid resource data.



\## 5.6 Resource Deletion



\### FR-10



An administrator shall be able to delete an existing resource.



The system shall return an appropriate error when the specified resource does not exist.



\---



\# 6. Reservation Requirements



\## 6.1 Creating Reservations



\### FR-11



An authenticated student shall be able to create a reservation.



A reservation shall contain information identifying:



\* The student.

\* The resource.

\* Reservation date.

\* Start time.

\* End time.



\### FR-12



The system shall require the necessary reservation fields.



Requests with missing required information shall be rejected.



\### FR-13



The system shall validate the requested resource.



A reservation shall not be created for a resource that does not exist.



\### FR-14



The system shall reject reservations for unavailable resources.



\### FR-15



The system shall validate reservation dates and times.



The system shall reject invalid date/time values.



The system shall reject reservations where the start time is not before the end time.



\## 6.2 Viewing Reservations



\### FR-16



An authenticated student shall be able to retrieve their reservations.



\### FR-17



A student shall be able to retrieve an individual reservation belonging to them.



\### FR-18



A student shall not be able to access another student's reservation through ownership-protected operations.



\## 6.3 Cancelling Reservations



\### FR-19



A student shall be able to cancel an eligible reservation belonging to them.



\### FR-20



The system shall prevent unauthorized students from cancelling another student's reservation.



\### FR-21



The system shall handle attempts to cancel a reservation that is already cancelled.



\## 6.4 Reservation Status



Reservations shall support the following statuses:



\* `PENDING`

\* `CONFIRMED`

\* `CANCELLED`

\* `COMPLETED`



Administrators shall be able to update reservation status through the administrative API.



\---



\# 7. Check-in Requirements



\## 7.1 Check-in Creation



\### FR-22



The system shall allow an authenticated student to check in for an eligible reservation.



\### FR-23



Check-in shall be associated with a specific reservation.



\### FR-24



The system shall validate that the reservation is eligible for check-in.



\### FR-25



The system shall prevent duplicate check-ins for the same reservation.



\## 7.2 Token/QR Check-in



\### FR-26



The system shall support check-in using the reservation's QR/token value.



The check-in token shall be validated against the relevant reservation.



\### FR-27



The system shall reject invalid or unauthorized check-in tokens.



\## 7.3 Check-in Status



The check-in lifecycle shall distinguish between:



\* `NOT\_CHECKED\_IN`

\* `CHECKED\_IN`



A successful check-in shall record the check-in information associated with the reservation.



\---



\# 8. Administrator Requirements



\## 8.1 Reservation Administration



\### FR-28



An administrator shall be able to retrieve system reservations.



\### FR-29



An administrator shall be able to update reservation status.



The system shall validate the requested status.



\## 8.2 User Administration



\### FR-30



An administrator shall be able to retrieve system user information through the administrative interface/API.



\## 8.3 Check-in Administration



\### FR-31



An administrator shall be able to retrieve check-in information.



\## 8.4 Resource Administration



\### FR-32



An administrator shall be able to create resources.



\### FR-33



An administrator shall be able to update resources.



\### FR-34



An administrator shall be able to change resource availability.



\### FR-35



An administrator shall be able to delete resources.



\---



\# 9. API Requirements



The backend shall expose REST API endpoints under `/api`.



\## 9.1 Health



| Method | Endpoint      | Purpose           |

| ------ | ------------- | ----------------- |

| GET    | `/api/health` | Verify API health |



\## 9.2 Authentication



| Method | Endpoint             | Purpose             |

| ------ | -------------------- | ------------------- |

| POST   | `/api/auth/register` | Register a user     |

| POST   | `/api/auth/login`    | Authenticate a user |



\## 9.3 Resources



| Method | Endpoint                           | Purpose                |

| ------ | ---------------------------------- | ---------------------- |

| GET    | `/api/resources`                   | List resources         |

| GET    | `/api/resources/<id>`              | Retrieve resource      |

| POST   | `/api/resources`                   | Create resource        |

| PUT    | `/api/admin/resources/<id>`        | Update resource        |

| PUT    | `/api/admin/resources/<id>/status` | Update resource status |

| DELETE | `/api/admin/resources/<id>`        | Delete resource        |



\## 9.4 Reservations



| Method | Endpoint                              | Purpose                                  |

| ------ | ------------------------------------- | ---------------------------------------- |

| POST   | `/api/reservations`                   | Create reservation                       |

| GET    | `/api/reservations`                   | List reservations                        |

| GET    | `/api/reservations/<id>`              | Retrieve reservation                     |

| DELETE | `/api/reservations/<id>`              | Cancel/delete reservation                |

| GET    | `/api/admin/reservations`             | Retrieve reservations for administration |

| PUT    | `/api/admin/reservations/<id>/status` | Update reservation status                |



\## 9.5 Check-ins



| Method | Endpoint                                      | Purpose                       |

| ------ | --------------------------------------------- | ----------------------------- |

| POST   | `/api/reservations/<reservation\_id>/check-in` | Check in to reservation       |

| GET    | `/api/reservations/<reservation\_id>/check-in` | Retrieve reservation check-in |

| POST   | `/api/check-in/<qr\_token>`                    | Check in using token          |

| GET    | `/api/admin/check-ins`                        | Retrieve check-ins            |



\## 9.6 Users



| Method | Endpoint           | Purpose                           |

| ------ | ------------------ | --------------------------------- |

| GET    | `/api/admin/users` | Retrieve users for administration |



\---



\# 10. Database Requirements



The production system shall use a MySQL relational database.



The implemented database contains the following primary tables:



\* `users`

\* `resources`

\* `reservations`

\* `check\_ins`



\## 10.1 Users



The users table stores user account information and authorization roles.



Important information includes:



\* User ID.

\* Name.

\* Student ID.

\* Email.

\* Password hash.

\* Role.



Roles include:



\* `STUDENT`

\* `ADMIN`



Passwords shall not be stored as plaintext credentials.



\## 10.2 Resources



The resources table stores reservable campus facilities and equipment.



Important information includes:



\* Resource ID.

\* Name.

\* Type.

\* Description.

\* Location.

\* Capacity.

\* Status.



\## 10.3 Reservations



The reservations table records resource bookings.



Important information includes:



\* Reservation ID.

\* Student/user relationship.

\* Resource relationship.

\* Reservation date.

\* Start time.

\* End time.

\* Reservation status.

\* Check-in/token-related reservation information where applicable.



\## 10.4 Check-ins



The check-ins table records reservation attendance/check-in information.



Important information includes:



\* Check-in ID.

\* Reservation relationship.

\* Check-in timestamp.



\---



\# 11. External Interface Requirements



\## 11.1 Student Interface



The student application shall provide interfaces for:



\* Registration.

\* Login.

\* Dashboard.

\* Resource browsing.

\* Reservation creation.

\* Reservation history.

\* Reservation cancellation.

\* Check-in.



The student frontend is implemented using React and Vite.



\## 11.2 Administrator Interface



The administrator application shall provide interfaces for:



\* Dashboard.

\* Reservations.

\* Resources.

\* Check-ins.

\* Users.



The administrator frontend is implemented using React and Vite.



\## 11.3 API Interface



The frontends shall communicate with the Flask backend using HTTP requests.



The development API base URL is:



```text

http://127.0.0.1:5000/api

```



The development frontend applications use Vite development servers.



\---



\# 12. Non-Functional Requirements



\## 12.1 Security



\### NFR-01



The system shall authenticate users before allowing access to protected operations.



\### NFR-02



The system shall use JWT-based authentication.



\### NFR-03



The system shall enforce role-based authorization for administrator operations.



\### NFR-04



The system shall enforce reservation ownership.



\### NFR-05



The system shall not commit environment secrets such as database credentials or JWT secrets to the public source repository.



\## 12.2 Reliability



\### NFR-06



The API shall return appropriate HTTP status codes for successful and failed operations.



\### NFR-07



The system shall validate user input before performing operations.



\### NFR-08



The system shall prevent duplicate check-ins.



\## 12.3 Maintainability



\### NFR-09



The backend shall use a modular application structure separating models, routes, configuration, and application initialization.



\### NFR-10



The frontend applications shall maintain separate service and presentation responsibilities.



\### NFR-11



The project shall use version control through Git.



\## 12.4 Testability



\### NFR-12



Backend functionality shall be covered by automated tests.



\### NFR-13



Tests shall be executable independently of the production MySQL database using a test database configuration.



\### NFR-14



The automated backend test suite shall execute through pytest.



\### NFR-15



Continuous integration shall execute backend tests.



\### NFR-16



Continuous integration shall lint and build both frontend applications.



\## 12.5 Usability



\### NFR-17



The interfaces shall provide clear navigation for the primary student and administrator tasks.



\### NFR-18



The system shall provide appropriate feedback for successful and unsuccessful operations.



\### NFR-19



The reservation workflow shall allow students to identify resources and manage their bookings through the student interface.



\---



\# 13. System Constraints



The following constraints apply to the current implementation:



1\. The backend is implemented using Python and Flask.

2\. The database is MySQL for the production environment.

3\. SQLAlchemy is used for database access.

4\. JWT is used for API authentication.

5\. The student frontend uses React and Vite.

6\. The administrator frontend uses React and Vite.

7\. The backend API is organized under the `/api` prefix.

8\. The project uses Git for source-code version control.

9\. The project uses GitHub for remote source-code hosting.

10\. Automated backend testing uses pytest.

11\. CI workflows use GitHub Actions.

12\. Environment-specific secrets must be supplied through configuration/environment variables rather than committed to source control.



\---



\# 14. Technology Stack



\## Backend



| Technology               | Purpose                      |

| ------------------------ | ---------------------------- |

| Python 3.14.2            | Backend programming language |

| Flask 3.1.3              | Web/API framework            |

| Flask-SQLAlchemy 3.1.1   | ORM integration              |

| Flask-JWT-Extended 4.7.4 | JWT authentication           |

| Flask-CORS 6.0.5         | Cross-origin API access      |

| PyMySQL 1.2.0            | MySQL database driver        |

| python-dotenv 1.2.3      | Environment configuration    |



\## Database



| Technology                    | Purpose                        |

| ----------------------------- | ------------------------------ |

| MySQL Community Server 8.0.46 | Production relational database |



\## Frontend



| Technology      | Purpose                            |

| --------------- | ---------------------------------- |

| React           | User interface                     |

| Vite            | Frontend development/build tooling |

| Node.js 24.20.0 | JavaScript runtime                 |

| npm 11.19.0     | Package management                 |



\## Testing



| Technology | Purpose                   |

| ---------- | ------------------------- |

| pytest     | Backend automated testing |

| pytest-cov | Test coverage measurement |



\## Version Control and CI



| Technology     | Purpose                |

| -------------- | ---------------------- |

| Git            | Source control         |

| GitHub         | Remote repository      |

| GitHub Actions | Continuous integration |



\---



\# 15. Testing Requirements



The backend shall have automated tests covering:



\* Authentication.

\* Registration.

\* Login.

\* Protected routes.

\* Resource operations.

\* Reservation operations.

\* Reservation ownership.

\* Reservation validation.

\* Check-in operations.

\* Duplicate check-in prevention.

\* Administrator authorization.

\* Administrator operations.

\* Error handling and edge cases.



The current automated backend suite contains \*\*108 passing tests\*\*.



The latest full coverage execution achieved:



```text

108 passed

99% total coverage

```



The coverage report recorded:



```text

TOTAL    412 statements    3 missed    99% coverage

```



The automated tests use an isolated SQLite test database through the Flask application test configuration and do not depend on the production MySQL database.



\---



\# 16. Continuous Integration Requirements



The project shall use GitHub Actions for automated quality checks.



\## 16.1 Backend CI



The backend workflow shall:



1\. Check out the repository.

2\. Set up Python.

3\. Install backend dependencies.

4\. Install pytest and pytest-cov.

5\. Execute the backend test suite.

6\. Generate test coverage information.



The workflow is located at:



```text

.github/workflows/backend-ci.yml

```



\## 16.2 Frontend CI



The frontend workflow shall independently process:



\* `admin-web`

\* `student-mobile`



Each frontend shall:



1\. Check out the repository.

2\. Set up Node.js.

3\. Install dependencies using `npm ci`.

4\. Run ESLint.

5\. Build the application.



The workflow is located at:



```text

.github/workflows/frontend-ci.yml

```



\---



\# 17. Project Structure



The major project directories are:



```text

campus-resource-reservation/

│

├── admin-web/

├── backend/

├── database/

├── documentation/

├── student-mobile/

├── .github/

│   └── workflows/

│       ├── backend-ci.yml

│       └── frontend-ci.yml

└── .gitignore

```



The backend application is structured approximately as:



```text

backend/

├── app/

│   ├── \_\_init\_\_.py

│   ├── config.py

│   ├── models/

│   │   ├── user.py

│   │   ├── resource.py

│   │   ├── reservation.py

│   │   └── check\_in.py

│   └── routes/

│       ├── health.py

│       ├── auth.py

│       ├── protected.py

│       ├── resource.py

│       ├── reservation.py

│       ├── check\_in.py

│       └── admin.py

│

├── tests/

├── requirements.txt

└── pytest.ini

```



\---



\# 18. Error Handling Requirements



The system shall return appropriate responses for common error conditions, including:



\* Missing authentication.

\* Invalid authentication credentials.

\* Missing request data.

\* Invalid request data.

\* Duplicate registration information.

\* Invalid resource identifiers.

\* Missing resources.

\* Unavailable resources.

\* Invalid reservation dates.

\* Invalid reservation times.

\* Unauthorized reservation access.

\* Invalid reservation status.

\* Invalid resource status.

\* Invalid resource type.

\* Invalid resource capacity.

\* Missing reservations.

\* Duplicate check-ins.

\* Invalid check-in tokens.

\* Unauthorized administrator operations.



The frontend applications shall present appropriate feedback to users where applicable.



\---



\# 19. Deployment Considerations



The production deployment shall provide:



\* A Python runtime for the Flask API.

\* A MySQL database.

\* Environment variables for sensitive configuration.

\* A production-appropriate API host.

\* Production builds of the React applications.

\* Appropriate CORS configuration.

\* Secure JWT and application secrets.



Development configuration such as `127.0.0.1` API addresses shall not be treated as production deployment addresses.



Database credentials and cryptographic secrets shall be supplied through environment configuration and shall not be committed to the repository.



\---



\# 20. Acceptance Criteria



The system shall be considered functionally acceptable when:



1\. A student can register successfully.

2\. A registered student can log in.

3\. Protected endpoints reject unauthenticated requests.

4\. Students can retrieve resources.

5\. Students can create valid reservations.

6\. Invalid reservation requests are rejected.

7\. Unavailable resources cannot be reserved.

8\. Students can view their reservations.

9\. Students cannot manipulate another student's reservations.

10\. Students can cancel eligible reservations.

11\. Students can check in to eligible reservations.

12\. Duplicate check-ins are prevented.

13\. Administrators can access administrator functionality.

14\. Students are denied administrator-only functionality.

15\. Administrators can manage resources.

16\. Administrators can manage reservation status.

17\. Administrators can view users and check-ins.

18\. Backend automated tests pass.

19\. Backend CI executes successfully.

20\. Both frontend applications lint successfully.

21\. Both frontend applications build successfully.

22\. No environment secrets are committed to the public repository.



\---



\# 21. Known Implementation Decisions



The following decisions form part of the current implementation and should not be changed unnecessarily:



\* Flask is used as the backend framework.

\* SQLAlchemy is used as the ORM.

\* MySQL is the production database.

\* React/Vite is used for both frontend applications.

\* JWT is used for authentication.

\* Student and administrator applications remain separate frontend applications.

\* The backend uses modular route blueprints.

\* The API remains under `/api`.

\* Automated backend tests use an isolated test database.

\* GitHub Actions is used for CI.

\* Environment variables are used for sensitive configuration.



Changes to these decisions should only be made when there is a demonstrated technical or project requirement.



\---



\# 22. Current Project Quality Status



At the time of this document's preparation:



\* Backend automated tests: \*\*108 passing\*\*

\* Backend total test coverage: \*\*99%\*\*

\* Resource route coverage: \*\*100%\*\*

\* Administrator route coverage: \*\*100%\*\*

\* Check-in route coverage: \*\*100%\*\*

\* Backend application factory coverage: \*\*100%\*\*

\* Frontend lint/build workflows: configured

\* Backend CI workflow: configured

\* Frontend CI workflow: configured

\* Git repository: configured

\* GitHub remote repository: configured

\* Current branch: `master`

\* Working tree: clean

\* Project source code: pushed to GitHub



\---



\# 23. Future Enhancements



The following items may be considered future improvements rather than assumptions about the current implementation:



\* Advanced search and filtering.

\* More sophisticated availability calendars.

\* Notifications and reminders.

\* Email integration.

\* Expanded reporting and analytics.

\* Fine-grained administrator permissions.

\* Mobile packaging/deployment.

\* Automated deployment pipelines.

\* Additional performance and load testing.

\* Expanded audit logging.



Future enhancements should not be treated as currently implemented functionality unless they are subsequently developed and verified.



\---



\# 24. Conclusion



CampusReserve provides a centralized software solution for managing campus facility and laboratory equipment reservations.



The implemented system combines a Flask REST API, React-based student and administrator interfaces, relational database storage, JWT authentication, reservation management, resource management, and reservation check-in functionality.



The project has been supported by automated backend testing, high test coverage, Git-based version control, and GitHub Actions continuous integration.



This SRS provides the requirements baseline against which the implemented system, tests, documentation, deployment process, and final project evaluation can be assessed.



