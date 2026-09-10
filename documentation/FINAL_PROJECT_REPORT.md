# IBL 3300 SOFTWARE ENGINEERING STUDIO
# FINAL PROJECT REPORT

## CampusReserve — Campus Smart Facility & Lab Equipment Reservation System

**Group:** 7  
**Course:** IBL 3300 Software Engineering Studio  
**Institution:** Technical University of Kenya  
**Project Type:** Web-based and mobile-responsive campus reservation system  
**Release:** v1.0.0

### Group Members

| Member | Student ID | Primary Responsibilities |
|---|---|---|
| Felistus Mbinya Mutiso | SCCJ/05862P/2024 | Project Management, Requirements, Documentation, QA Coordination |
| Benson Githui | SCCJ/00627/2023 | Backend/API, Database Integration, Authentication, System Integration |
| Ogeto Francis | SCCJ/05678P/2025S | Frontend, UI Integration, User-Facing Functionality |

---

# 1. EXECUTIVE SUMMARY

CampusReserve is a web-based and mobile-responsive system designed to simplify the reservation and management of campus facilities and lab equipment.

The system allows students to view available resources, submit reservations, view their reservations, cancel eligible reservations, receive in-app notifications, and complete reservation check-in using a generated check-in token/QR functionality.

Administrators can authenticate into the administration portal, manage resources, review users, manage reservations, confirm or cancel reservations, and monitor check-ins.

The implemented system uses two React/Vite frontend clients, a Flask REST API backend, and MySQL persistence. The production deployment uses Vercel for the frontend applications, Render for the backend API, and Aiven MySQL for the production database.

The final implementation was developed with an emphasis on maintainability, separation of concerns, authentication, database persistence, testing, continuous integration, documentation, and deployment readiness.

---

# 2. PROBLEM STATEMENT

Campus facilities and equipment can be difficult to manage efficiently when reservations depend on manual processes or disconnected communication.

Students need a convenient way to discover available facilities and equipment and submit reservations. Administrators require a centralized interface for managing resources, reservations, users, and check-ins.

CampusReserve addresses these challenges by providing a centralized reservation platform with role-based access and persistent database storage.

---

# 3. PROJECT OBJECTIVES

The project objectives were to:

1. Provide students with a convenient interface for viewing campus resources.
2. Allow authenticated students to create and manage reservations.
3. Allow administrators to manage facilities and equipment.
4. Provide a reservation lifecycle with controlled status transitions.
5. Provide reservation check-in functionality.
6. Provide in-app reservation notifications.
7. Protect authenticated operations using JWT-based authentication.
8. Persist application data using MySQL.
9. Provide separate student and administrator interfaces.
10. Apply software engineering practices including modular architecture, testing, documentation, CI, and deployment.

---

# 4. SYSTEM SCOPE

## 4.1 Student Functionality

The student portal provides:

- Student registration.
- Student login.
- Resource browsing.
- Resource availability display.
- Reservation creation.
- Viewing personal reservations.
- Reservation cancellation.
- Reservation check-in.
- Check-in token/QR functionality.
- In-app notifications.
- Notification read/unread state.

## 4.2 Administrator Functionality

The administrator portal provides:

- Administrator authentication.
- Dashboard.
- Resource management.
- Resource status management.
- Reservation management.
- Reservation confirmation and cancellation.
- Check-in monitoring.
- User management.

## 4.3 Out-of-Scope Features

The implementation does not claim:

- Native Android/iOS applications.
- Flutter/Dart implementation.
- Microservices.
- Email notifications.
- SMS notifications.
- Camera-based QR scanning unless separately implemented and demonstrated.
- Automatic reservation confirmation.

The student application is a responsive React/Vite web application that can be accessed from mobile devices.

---

# 5. REQUIREMENTS

## 5.1 Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | Users shall be able to register. |
| FR-02 | Users shall be able to authenticate. |
| FR-03 | Students shall be able to browse resources. |
| FR-04 | Students shall be able to create reservations. |
| FR-05 | Students shall be able to view their reservations. |
| FR-06 | Students shall be able to cancel eligible reservations. |
| FR-07 | Students shall be able to initiate reservation check-in. |
| FR-08 | Students shall receive relevant in-app reservation notifications. |
| FR-09 | Administrators shall be able to manage resources. |
| FR-10 | Administrators shall be able to manage reservations. |
| FR-11 | Administrators shall be able to manage resource availability/status. |
| FR-12 | Administrators shall be able to view users and check-ins. |

## 5.2 Non-Functional Requirements

The system was designed with the following qualities:

- Security through authenticated and role-protected operations.
- Maintainability through modular backend routes and frontend services.
- Usability through responsive web interfaces.
- Reliability through automated testing.
- Portability through environment-based configuration.
- Scalability within the intended monolithic/layered project scope.
- Availability through cloud deployment.
- Traceability through Git version control and documentation.

---

# 6. SYSTEM ARCHITECTURE

CampusReserve uses a layered client-server REST architecture.

The overall flow is:

Student React/Vite Client
        |
        v
Flask REST API
        |
        v
MySQL Database

Administrator React/Vite Client
        |
        v
Flask REST API
        |
        v
MySQL Database

The backend is organized using Flask's Application Factory Pattern and modular Blueprints.

The architecture was intentionally kept as a straightforward layered/client-server design rather than introducing microservices.

---

# 7. TECHNOLOGY STACK

| Layer | Technology |
|---|---|
| Student Frontend | React + Vite |
| Admin Frontend | React + Vite |
| Backend | Python + Flask |
| ORM | Flask-SQLAlchemy / SQLAlchemy |
| Authentication | Flask-JWT-Extended |
| Password Security | Werkzeug password hashing |
| Database | MySQL |
| Database Driver | PyMySQL |
| API Style | REST |
| Testing | Pytest |
| Coverage | pytest-cov |
| API Testing | Postman |
| Static Analysis | ESLint |
| CI | GitHub Actions |
| Student Deployment | Vercel |
| Admin Deployment | Vercel |
| Backend Deployment | Render |
| Production Database | Aiven MySQL |
| Version Control | Git + GitHub |

---

# 8. DATABASE DESIGN

The main database is campus_reservation.

The implemented database contains:

- users
- esources
- eservations
- check_ins
- 
otifications

Important resource types include:

- LABORATORY
- STUDY_ROOM
- EQUIPMENT

Reservation states include:

- PENDING
- CONFIRMED
- CANCELLED
- COMPLETED

Check-in states include:

- NOT_CHECKED_IN
- CHECKED_IN

The database design provides relationships between users, resources, reservations, check-ins, and notifications.

---

# 9. AUTHENTICATION AND AUTHORIZATION

Authentication is implemented using JSON Web Tokens.

The system provides:

- Student registration.
- Student login.
- Administrator login.
- Protected API routes.
- Role-based administrator operations.
- Password hashing.

The JWT access-token lifetime is configured for eight hours.

The backend validates ownership and reservation state before allowing sensitive reservation and check-in operations.

---

# 10. RESERVATION LIFECYCLE

The implemented reservation lifecycle is:

PENDING → CONFIRMED  
PENDING → CANCELLED  
CONFIRMED → CANCELLED  
CONFIRMED → COMPLETED

Reservations are not automatically confirmed.

Administrators control confirmation and cancellation through the administration portal.

Notifications are generated for:

- PENDING → CONFIRMED
- PENDING → CANCELLED
- CONFIRMED → CANCELLED

No notification is generated for CONFIRMED → COMPLETED.

---

# 11. API DESIGN

The REST API is organized into functional areas.

## Authentication

- POST /api/auth/register
- POST /api/auth/login

## Resources

- GET /api/resources
- GET /api/resources/<resource_id>
- POST /api/resources
- PUT /api/admin/resources/<resource_id>
- DELETE /api/admin/resources/<resource_id>
- PUT /api/admin/resources/<resource_id>/status

## Reservations

- POST /api/reservations
- GET /api/reservations
- GET /api/reservations/<reservation_id>
- DELETE /api/reservations/<reservation_id>

## Administration

- GET /api/admin/reservations
- GET /api/admin/check-ins
- GET /api/admin/users
- PUT /api/admin/reservations/<reservation_id>/status

## Check-in

- POST /api/reservations/<reservation_id>/check-in
- GET /api/reservations/<reservation_id>/check-in
- POST /api/check-in/<qr_token>

## Notifications

- GET /api/notifications
- PUT /api/notifications/<notification_id>/read

---

# 12. SOFTWARE DESIGN

## 12.1 Application Factory Pattern

The Flask Application Factory Pattern is used to create and configure application instances.

This supports:

- Separation of application creation and execution.
- Testing with controlled application instances.
- Centralized extension initialization.
- Cleaner configuration management.

## 12.2 Flask Blueprints

The backend uses modular Flask Blueprints to separate API responsibilities such as authentication, resources, reservations, check-ins, administration, and notifications.

Blueprints are treated as a Flask modularization mechanism rather than incorrectly claiming them as a GoF design pattern.

## 12.3 Architectural Styles

The implementation uses:

- Client-server architecture.
- Layered architecture.
- REST API architecture.

The selected architecture provides an appropriate balance between simplicity, maintainability, and the project's scope.

---

# 13. USER INTERFACES

## 13.1 Student Portal

The student portal provides:

- Registration.
- Login.
- Resource browsing.
- Reservation interface.
- Reservation history.
- Cancellation.
- Check-in.
- Notifications.

The interface is responsive and designed for access from desktop and mobile browsers.

## 13.2 Administration Portal

The administrator portal provides:

- Dashboard.
- Resource management.
- Reservation management.
- Check-in monitoring.
- User management.

Resource names are displayed in administrative workflows rather than exposing internal resource IDs unnecessarily.

---

# 14. SOFTWARE ENGINEERING PROCESS

The project followed an iterative software engineering approach.

The implementation included activities covering:

- Requirements analysis.
- Backlog planning.
- System design.
- Architecture selection.
- Database design.
- API development.
- Frontend development.
- Integration.
- Automated testing.
- API testing.
- Static analysis.
- Continuous integration.
- Deployment.
- QA/system testing.
- Documentation.
- Release preparation.
- Maintenance and handover planning.

Where historical evidence was unavailable, documentation was reconstructed from the current implementation and repository rather than presenting invented historical activity as fact.

---

# 15. VERSION CONTROL AND COLLABORATION

Git and GitHub were used for configuration management and source-code version control.

The project repository contains the application source code, documentation, CI workflows, and project artefacts.

The documented team responsibility allocation was:

- Felistus — project management, requirements, documentation and QA coordination.
- Benson — backend/API, database integration, authentication and system integration.
- Ogeto — frontend, UI integration and user-facing functionality.

The project uses the master branch.

The final release was tagged:

1.0.0

---

# 16. TESTING

Automated backend testing was implemented using Pytest.

Final automated test result:

**112 tests passed**

Coverage result:

**96% coverage**

Coverage measurement:

- 482 statements
- 21 missed statements
- 96% overall coverage

The result exceeds the project's approximately 70% target.

The test suite covers important backend functionality including authentication, resource operations, reservations, administration, check-in, notifications, authorization and application behavior.

Three existing deprecation warnings relating to datetime.utcnow() remained. These warnings did not cause test failures.

---

# 17. API TESTING

Postman was used for API-level verification.

The CampusReserve API Postman collection is organized into:

- Health
- Authentication
- Resources
- Student Reservations
- Admin
- Check-in
- Notifications

A representative end-to-end API workflow was verified:

1. Health endpoint returned HTTP 200.
2. Student authentication succeeded.
3. Resources were retrieved successfully.
4. A reservation was created.
5. The student's reservations were retrieved.
6. Administrator authentication succeeded.
7. Administrator reservations were retrieved.
8. The reservation was confirmed.
9. A confirmation notification was generated.
10. The notification was marked as read.

A Postman URL configuration issue involving a duplicated /api path was identified and corrected during testing.

---

# 18. QUALITY ASSURANCE AND SYSTEM TESTING

System testing covered the principal student and administrator workflows.

The QA process considered:

- Authentication.
- Resource browsing.
- Reservation creation.
- Reservation retrieval.
- Reservation cancellation.
- Administrator reservation management.
- Reservation status changes.
- Check-in.
- Notifications.
- Authorization.
- Database persistence.

The overall QA assessment was recorded as PASS based on the implemented and demonstrated functionality.

UAT-oriented acceptance checks were documented without falsely representing them as formal external stakeholder sign-offs.

---

# 19. CONTINUOUS INTEGRATION

GitHub Actions was implemented for automated quality checks.

## Backend CI

The backend workflow:

- Runs on pushes and pull requests.
- Uses Python 3.14.
- Installs project dependencies.
- Runs Pytest.
- Generates coverage information.

## Frontend CI

The frontend workflow:

- Uses Node 24.
- Installs dependencies.
- Runs ESLint.
- Builds the admin frontend.
- Runs ESLint.
- Builds the student frontend.

Successful CI runs were obtained for the final implementation.

An older historical workflow failure exists in the repository history. It occurred on an earlier project state and was superseded by later successful CI runs; it is not represented as a current defect.

---

# 20. DEPLOYMENT

The production architecture uses cloud-hosted services.

## Student Application

Vercel:

https://campus-resource-reservation.vercel.app/

## Administrator Application

Vercel:

https://campus-resource-reservation-2vz5.vercel.app/

## Backend API

Render:

https://campus-resource-reservation.onrender.com/

API base:

https://campus-resource-reservation.onrender.com/api

## Database

Aiven MySQL is used for the production database.

The deployment separates frontend hosting, backend hosting, and database persistence while maintaining the same application architecture.

Environment configuration is used so that the frontend can communicate with the appropriate backend API without hard-coding a local development dependency into production.

---

# 21. DEPLOYMENT AND CONFIGURATION MANAGEMENT

The system distinguishes between development and production environments.

Development backend:

http://127.0.0.1:5000

Development API:

http://127.0.0.1:5000/api

Production backend:

https://campus-resource-reservation.onrender.com

Production API:

https://campus-resource-reservation.onrender.com/api

Sensitive environment values are excluded from source control through .gitignore.

---

# 22. SECURITY CONSIDERATIONS

Security measures implemented include:

- Password hashing.
- JWT authentication.
- Protected API routes.
- Role-based administrative authorization.
- Reservation ownership validation.
- Reservation-state validation.
- Check-in ownership validation.
- Duplicate check-in protection.
- Environment-based configuration for sensitive deployment values.
- CORS configuration for API access.

The system is intended for academic demonstration and controlled deployment rather than production-critical campus infrastructure.

---

# 23. REFACTORING AND MAINTAINABILITY

The project was structured to improve maintainability through:

- Modular Flask routes.
- Separate data models.
- Frontend service modules.
- Application Factory Pattern.
- Environment-based configuration.
- Automated tests.
- CI workflows.
- Documentation.
- Explicit architectural decisions.

The project avoids unnecessary architectural complexity such as microservices because the selected layered architecture is appropriate for the current scope.

---

# 24. DOCUMENTATION

The project documentation includes:

- Software Requirements Specification.
- API documentation.
- Architecture documentation.
- Database documentation.
- UML use cases.
- UML class diagram documentation.
- UML sequence diagrams.
- UML activity diagrams.
- UML component diagram documentation.
- UML deployment diagram documentation.
- Design patterns documentation.
- Architecture Decision Records.
- Sprint Plan and Definition of Done.
- Collaborative Development documentation.
- Sprint Review and Retrospective.
- Release Plan.
- QA/UAT Report.
- QA/System Testing Report.
- User Manual.
- Maintenance and Handover documentation.

---

# 25. PROJECT MANAGEMENT AND ITERATION

The project was organized around iterative development and incremental delivery.

The major implementation progression was:

1. Project structure and repository setup.
2. Backend foundation.
3. Database and API implementation.
4. Authentication.
5. Student functionality.
6. Administrator functionality.
7. Reservation lifecycle.
8. Check-in.
9. Notifications.
10. UI refinement.
11. Automated testing.
12. API verification.
13. CI implementation.
14. Cloud deployment.
15. QA and system testing.
16. Documentation and release preparation.

The final release was identified as 1.0.0.

---

# 26. CHALLENGES ENCOUNTERED

Several implementation challenges were encountered during development.

### Database and schema issues

Database schema and seed-state issues temporarily affected API operations. The database was corrected and the application flow restored.

### Authentication configuration

Administrator account setup required resolving an existing student identifier conflict before the administrator credentials could be used successfully.

### Frontend/backend environment differences

The local development API used localhost while production required the deployed Render API. Environment-based configuration was therefore required for deployment.

### API configuration during Postman testing

A duplicated /api path caused one notification endpoint request to return HTTP 404. The collection variable usage was corrected and the endpoint subsequently returned HTTP 200.

### Deployment environment

The project required separate configuration for Vercel frontend deployments, Render backend deployment, and Aiven database connectivity.

These issues were handled as implementation and configuration problems rather than by changing the fundamental architecture.

---

# 27. CURRENT SYSTEM STATUS

| Area | Status |
|---|---|
| Student frontend | COMPLETE |
| Admin frontend | COMPLETE |
| Flask REST API | COMPLETE |
| Authentication | COMPLETE |
| Database persistence | COMPLETE |
| Reservations | COMPLETE |
| Check-in | COMPLETE |
| Notifications | COMPLETE |
| Automated backend tests | COMPLETE |
| Test coverage | COMPLETE |
| Postman API testing | COMPLETE |
| ESLint | COMPLETE |
| GitHub Actions CI | COMPLETE |
| Production deployment | COMPLETE |
| QA/system testing documentation | COMPLETE |
| UML documentation | COMPLETE |
| Architecture documentation | COMPLETE |
| Design patterns documentation | COMPLETE |
| ADR documentation | COMPLETE |
| Sprint/DoD documentation | COMPLETE |
| Release plan | COMPLETE |
| Maintenance/handover documentation | COMPLETE |
| Final project report | COMPLETE |
| Formal external UAT sign-off | NOT CLAIMED |

---

# 28. LIMITATIONS

The current system has several limitations:

1. The student application is a responsive web application rather than a native mobile application.
2. The QR/check-in implementation uses generated check-in token functionality; camera-based QR scanning is not claimed unless separately demonstrated.
3. The system does not implement email or SMS notification delivery.
4. The system is designed for the project's academic scope and is not positioned as a fully production-hardened institutional platform.
5. Some historical development evidence cannot be reconstructed with certainty and is therefore not falsely presented as completed historical activity.

---

# 29. FUTURE IMPROVEMENTS

Potential future improvements include:

- Native mobile application support.
- Camera-based QR scanning.
- Email and SMS notifications.
- Advanced reporting and analytics.
- Calendar integration.
- More sophisticated resource availability scheduling.
- Automated deployment pipelines with separate staging environments.
- Enhanced audit logging.
- More granular administrative permissions.
- Performance monitoring.
- Automated database migrations.

These improvements are outside the required v1.0.0 scope.

---

# 30. LESSONS LEARNED

The project demonstrated the importance of integrating software engineering practices with implementation rather than treating documentation and testing as activities performed only at the end.

Important lessons included:

- Requirements should guide implementation scope.
- Architecture decisions should match project complexity.
- Environment configuration is essential when moving from local development to cloud deployment.
- Automated testing provides confidence when modifying backend functionality.
- CI catches integration and build problems early.
- API testing complements frontend testing.
- Version control provides traceability for implementation changes.
- Documentation is most useful when it reflects the actual implementation.
- Technical evidence should be distinguished from reconstructed project records.
- A simple layered architecture can be more appropriate than introducing unnecessary distributed-system complexity.

---

# 31. CONCLUSION

CampusReserve provides a functional campus facility and lab equipment reservation platform with separate student and administrator interfaces.

The final implementation integrates React/Vite frontends, a Flask REST backend, MySQL persistence, JWT authentication, reservation management, check-in functionality, notifications, automated testing, API testing, CI, cloud deployment, and technical documentation.

The system achieved 112 passing automated tests with 96% test coverage and successfully completed the major integration, QA, deployment, and documentation activities required for the final project stage.

The project is released as version 1.0.0 and includes supporting documentation for operation, maintenance, and handover.

The implementation remains intentionally aligned with the original project scope and does not claim functionality or historical evidence that was not actually implemented or available.

---

# 32. HANDOVER SUMMARY

The final system consists of:

- Student React/Vite application.
- Administrator React/Vite application.
- Flask REST API.
- MySQL database.
- Automated backend tests.
- Frontend lint/build checks.
- GitHub Actions CI.
- Postman API collection.
- UML and architecture documentation.
- QA and system-testing documentation.
- User manual.
- Release plan.
- Maintenance and handover documentation.

**Release:** v1.0.0  
**Repository branch:** master  
**Deployment model:** Vercel + Render + Aiven  
**Final status:** READY FOR TECHNICAL WALKTHROUGH AND HANDOVER

---

**END OF FINAL PROJECT REPORT**
