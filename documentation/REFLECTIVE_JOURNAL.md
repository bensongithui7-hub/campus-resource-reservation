# IBL 3300 SOFTWARE ENGINEERING STUDIO
# GROUP 7 — REFLECTIVE JOURNAL

## CampusReserve — Campus Smart Facility & Lab Equipment Reservation System

**Course:** IBL 3300 Software Engineering Studio  
**Institution:** Technical University of Kenya  
**Group:** 7  
**Project:** CampusReserve  
**Release:** v1.0.0

---

# 1. PURPOSE OF THE REFLECTIVE JOURNAL

This reflective journal records the learning, challenges, contributions, engineering decisions, and lessons associated with the development of CampusReserve.

The reflections are based on the implemented system, documented responsibilities, repository artefacts, testing results, deployment work, and final project state.

Where detailed historical activity records were unavailable, the reflections describe the contribution and learning evidenced by the final implementation rather than inventing specific meetings, dates, or undocumented events.

---

# 2. PROJECT OVERVIEW

CampusReserve is a web-based and mobile-responsive campus facility and lab equipment reservation system.

The system consists of:

- React/Vite student frontend.
- React/Vite administrator frontend.
- Flask REST API.
- MySQL database.
- JWT authentication.
- Reservation management.
- Check-in functionality.
- In-app notifications.
- Automated testing.
- Postman API testing.
- GitHub Actions CI.
- Vercel frontend deployment.
- Render backend deployment.
- Aiven MySQL production database.

The final release is 1.0.0.

---

# 3. GROUP MEMBER REFLECTIONS

## 3.1 Felistus Mbinya Mutiso

**Student ID:** SCCJ/05862P/2024  
**Primary responsibilities:** Project Management, Requirements, Documentation, QA Coordination

### Reflection

My involvement in CampusReserve provided experience in connecting software requirements and project organization with the implementation of an actual software product.

One of the important lessons from the project was that requirements must remain connected to the functionality being implemented. The reservation system required clearly defined student and administrator responsibilities, reservation states, resource management, authentication, check-in, and notification behavior.

Working around the requirements and documentation aspects of the project demonstrated the importance of maintaining a clear scope. The project deliberately remained within a layered client-server architecture instead of introducing unnecessary technologies such as microservices or a native mobile application.

The documentation work also demonstrated that technical documentation must describe the system that actually exists. This was particularly important when documenting architecture, UML, design patterns, ADRs, testing, QA, deployment, and maintenance.

The QA coordination perspective provided another important lesson: a system should not be considered complete simply because the interface appears to work. Backend tests, API testing, integration checks, CI, and system-level QA provide additional evidence that the implementation behaves as intended.

### Challenges and Learning

A major lesson was the need to coordinate requirements, implementation, testing, and documentation rather than treating them as completely separate activities.

The project also demonstrated how unexpected technical problems can affect project progress. Database issues, authentication configuration problems, API configuration errors, and deployment configuration all required attention before the final system could be considered ready.

I learned that effective project management in software engineering involves continuously relating the planned functionality to actual implementation evidence.

### Contribution to the Final Product

My responsibilities contributed to:

- Requirements documentation.
- Project organization.
- Software engineering documentation.
- QA coordination.
- Documentation of testing and acceptance checks.
- Supporting the final project report and handover documentation.

### Main Lesson

The main lesson I gained was that successful software engineering requires coordination between people, requirements, implementation, testing, and documentation. A technically functional system becomes much easier to understand and maintain when these areas are properly connected.

---

# 3.2 Benson Githui

**Student ID:** SCCJ/00627/2023  
**Primary responsibilities:** Backend/API, Database Integration, Authentication, System Integration

### Reflection

My main contribution to CampusReserve focused on the backend, database integration, authentication, and system integration.

Working on the backend provided practical experience in designing and implementing a REST API using Flask. The backend had to support authentication, resources, reservations, administration, check-in, and notifications while maintaining clear separation between different responsibilities.

One of the most important lessons was understanding the relationship between the database, backend business logic, and frontend functionality. A feature such as making a reservation is not only a frontend form. It requires API validation, database persistence, authentication, ownership checks, reservation-state handling, and appropriate responses back to the client.

Authentication also provided practical experience with JWT-based security, password hashing, protected routes, and role-based administrative access.

Database problems encountered during development demonstrated the importance of checking the complete application stack when an API operation fails. A backend error may originate from database schema or data state rather than from the route itself.

The project also provided significant experience with automated testing. The final backend test suite achieved 112 passing tests and 96% coverage. This demonstrated the value of testing both normal functionality and protected/error conditions.

### Challenges and Learning

One challenge was resolving database and seed-state problems that temporarily affected API operations.

Another challenge involved administrator account configuration. An existing student identifier conflicted with the intended administrator account, requiring the data state to be corrected before administrator authentication could work as intended.

Postman testing also exposed a duplicated /api path configuration issue. The problem produced a 404 response for a notification request and demonstrated how small configuration errors can appear to be backend defects until the complete request URL is inspected.

Deployment introduced another layer of complexity because the local API and production API use different environments. Environment-based configuration became important when moving from localhost to Render and Vercel.

### Contribution to the Final Product

My responsibilities contributed directly to:

- Flask REST API implementation.
- Database integration.
- SQLAlchemy models and persistence.
- JWT authentication.
- Password security.
- Protected routes.
- Role-based administration.
- Reservation lifecycle logic.
- Check-in logic.
- Notification functionality.
- Backend integration with the frontend applications.
- Automated backend testing.
- Production backend integration.

### Main Lesson

My main lesson was that backend engineering is not isolated from the rest of the system. Database design, API behavior, authentication, frontend integration, testing, and deployment all have to work together for the application to function reliably.

I also learned that automated testing and CI are particularly valuable when making backend changes because they provide evidence that existing functionality has not been unintentionally broken.

---

# 3.3 Ogeto Francis

**Student ID:** SCCJ/05678P/2025S  
**Primary responsibilities:** Frontend, UI Integration, User-Facing Functionality

### Reflection

My contribution to CampusReserve focused on the frontend and user-facing functionality.

The project provided practical experience in implementing a responsive React/Vite interface that communicates with a Flask REST API.

One important lesson was that frontend development involves more than designing screens. The interface has to consume API responses correctly, maintain authentication state, display meaningful feedback, and handle different states such as successful reservations, cancelled reservations, notifications, and errors.

The student portal was developed to provide users with access to registration, login, resource browsing, reservation functionality, reservation history, check-in, and notifications.

The administrator portal required a different interaction model because administrators need to manage resources and reservations rather than simply create reservations.

The project also demonstrated the importance of responsive design. Although the implementation is a web application rather than a native mobile application, the student interface was designed to remain usable on mobile-sized screens.

### Challenges and Learning

One lesson was the importance of keeping the frontend aligned with the backend API contract. When an endpoint, response, authentication requirement, or data structure changes, the frontend integration can also be affected.

The project also demonstrated the importance of handling user feedback clearly. Reservation actions, cancellation, authentication, and notifications need understandable interface responses so that users can determine whether an action succeeded.

UI refinement also showed that small layout and spacing changes can significantly affect usability without requiring a change to the underlying architecture.

### Contribution to the Final Product

My responsibilities contributed to:

- Student portal implementation.
- Administrator portal implementation.
- React/Vite integration.
- User-facing reservation functionality.
- Resource browsing.
- Reservation display and management.
- Notification interface.
- Responsive layout.
- UI refinement and branding.
- Integration of frontend functionality with the Flask API.

### Main Lesson

My main lesson was that frontend development depends heavily on understanding the complete system. A good interface must reflect the actual backend functionality and provide clear feedback to users.

I also learned that responsive web development can provide mobile accessibility without requiring the project to become a separate native mobile application.

---

# 4. GROUP REFLECTION

As a group, CampusReserve demonstrated the importance of dividing responsibilities while maintaining integration between different parts of the system.

The three responsibility areas were complementary:

| Member | Main Area | Contribution to Integration |
|---|---|---|
| Felistus Mbinya Mutiso | Project Management, Requirements, Documentation, QA | Requirements, documentation and quality coordination |
| Benson Githui | Backend, Database, Authentication, Integration | API, persistence, security and system integration |
| Ogeto Francis | Frontend and UI | User-facing functionality and API integration |

The project could not be completed effectively by treating these responsibilities as independent components.

The frontend depended on the API, the API depended on the database and authentication layer, and the entire implementation depended on requirements, testing, documentation, deployment, and QA.

---

# 5. TECHNICAL LESSONS LEARNED

## 5.1 Architecture

The project reinforced the value of selecting architecture according to project requirements.

A layered client-server REST architecture was sufficient for CampusReserve and avoided unnecessary complexity.

## 5.2 Database Design

The project demonstrated that database schema consistency is essential. Changes or inconsistencies in database state can affect apparently unrelated API functionality.

## 5.3 Authentication

JWT authentication and role-based authorization demonstrated the importance of protecting sensitive operations rather than relying only on frontend restrictions.

## 5.4 Testing

The final result of 112 passing automated tests and 96% coverage demonstrated the value of automated testing during development and final integration.

## 5.5 API Testing

Postman provided another perspective on the backend independently of the frontend. This helped identify request configuration problems and verify the API contract.

## 5.6 Continuous Integration

GitHub Actions demonstrated how automated testing, linting, and frontend builds can be run consistently when code changes are pushed.

## 5.7 Deployment

Moving from localhost to Vercel, Render, and Aiven demonstrated that deployment requires environment configuration and integration across multiple services.

## 5.8 Documentation

The project demonstrated that documentation should correspond to the actual implementation. Unsupported features or undocumented historical activities should not be presented as completed evidence.

---

# 6. SOFTWARE ENGINEERING PRACTICES REFLECTION

The project provided experience across several areas required by the Software Engineering Studio.

### Requirements Engineering

Requirements were translated into functional features such as resource browsing, reservation management, check-in, notifications, and administration.

### Object-Oriented Design

The backend models and application structure separate responsibilities for users, resources, reservations, check-ins, and notifications.

### Design

The application uses the Flask Application Factory Pattern and modular Blueprints together with layered/client-server REST architecture.

### Version Control

Git and GitHub were used to maintain source history and release the final version.

### Testing

Pytest, coverage, Postman, ESLint, and CI were used as complementary quality mechanisms.

### Quality Assurance

System-level QA considered authentication, resource operations, reservations, check-in, notifications, authorization, and persistence.

### Deployment

The final system was deployed using Vercel, Render, and Aiven.

### Maintenance

Maintenance and handover documentation was prepared to describe how the system can be operated and maintained after completion.

---

# 7. WHAT WE WOULD DO DIFFERENTLY

If the project were started again, the group would benefit from:

1. Establishing a stronger shared development schedule from the beginning.
2. Maintaining more detailed contemporaneous records of weekly activities.
3. Performing integration testing earlier.
4. Keeping deployment configuration aligned with development configuration from an earlier stage.
5. Establishing a clearer shared issue and defect tracking process.
6. Conducting code review more systematically throughout development.
7. Capturing project decisions and evidence continuously rather than reconstructing some documentation near the final stage.
8. Allocating additional time for final QA and documentation before the final deadline.

These improvements would reduce final-stage pressure and make the development process easier to demonstrate.

---

# 8. INDIVIDUAL CONTRIBUTION SUMMARY

## Felistus Mbinya Mutiso

**Primary contribution:** Project management, requirements, documentation and QA coordination.

Key contribution areas:

- Requirements organization.
- Project documentation.
- QA coordination.
- Software engineering process documentation.
- Final project documentation.

## Benson Githui

**Primary contribution:** Backend/API, database integration, authentication and system integration.

Key contribution areas:

- Flask backend.
- REST API.
- Database integration.
- Authentication.
- Authorization.
- Reservation logic.
- Check-in.
- Notifications.
- Automated backend testing.
- Integration and deployment support.

## Ogeto Francis

**Primary contribution:** Frontend, UI integration and user-facing functionality.

Key contribution areas:

- Student frontend.
- Administrator frontend.
- React/Vite integration.
- Resource browsing.
- Reservation interface.
- User-facing reservation management.
- Notifications interface.
- Responsive UI.
- Frontend/API integration.

---

# 9. OVERALL GROUP LEARNING OUTCOME

The group gained practical experience in taking a software system through multiple stages of the engineering lifecycle.

The most significant overall lesson was that software engineering is an integrated process.

Requirements influence design.  
Design influences implementation.  
Implementation requires testing.  
Testing supports QA.  
CI automates quality checks.  
Deployment introduces environment concerns.  
Documentation records the decisions and functionality required for maintenance.

CampusReserve provided practical experience connecting these activities into one software engineering project.

---

# 10. FINAL REFLECTION

The completion of CampusReserve demonstrated that a software project is not complete merely when its main screens work.

The final system required integration of:

- Requirements.
- Architecture.
- Database design.
- Backend development.
- Frontend development.
- Authentication.
- Testing.
- QA.
- CI.
- Deployment.
- Documentation.
- Maintenance planning.
- Handover.

The project also showed the importance of being honest about project evidence. Where historical records were incomplete, the group documented the current implementation and reconstructed evidence carefully instead of claiming activities that could not be supported.

The final v1.0.0 release therefore represents not only the implemented application but also the engineering artefacts surrounding it.

---

# 11. FINAL STATUS

**Project:** CampusReserve  
**Release:** v1.0.0  
**Branch:** master  
**Architecture:** Layered Client-Server REST  
**Frontend:** React/Vite  
**Backend:** Flask REST API  
**Database:** MySQL  
**Testing:** 112 passed, 96% coverage  
**CI:** GitHub Actions  
**Deployment:** Vercel + Render + Aiven  
**Final State:** Ready for technical walkthrough and handover

---

**END OF GROUP REFLECTIVE JOURNAL**
