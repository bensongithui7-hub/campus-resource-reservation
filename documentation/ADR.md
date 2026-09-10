# Architecture Decision Records

> Current-state decision records for the implemented CampusReserve architecture. These records do not claim historical meetings or decisions where original evidence is unavailable.

## ADR-001: Client-Server Layered REST Architecture

**Status:** Accepted

### Context
CampusReserve requires separate student and administrator interfaces with centralized authentication, reservation processing, resource management, check-in processing, notifications, and database persistence.

### Decision
Use React/Vite clients communicating with a Flask REST API. The backend uses a layered organization separating routes, application logic, models, and persistence.

### Consequences
- Frontends and backend can be deployed independently.
- Business operations remain centralized.
- Responsibilities are separated.
- Multiple clients can consume the same API.
- Frontends depend on backend/API availability.

---

## ADR-002: React/Vite Responsive Web Clients

**Status:** Accepted

### Context
CampusReserve requires access from both desktop and mobile-sized screens.

### Decision
Implement the student and administrator clients as React/Vite responsive web applications.

The student client is mobile-responsive web software, not a native Flutter/Dart application.

### Consequences
- Users access the system through a web browser.
- Desktop and mobile screen sizes are supported.
- No native APK is required for the current scope.
- The implementation remains consistent with the actual project.

---

## ADR-003: Flask Application Factory

**Status:** Accepted

### Context
The backend requires different configurations for normal execution and automated testing.

### Decision
Use Flask's Application Factory pattern through create_app() in:

ackend/app/__init__.py

The factory creates the application, initializes extensions, configures the application, and registers blueprints.

### Consequences
- Application creation is centralized.
- Test applications can be created independently.
- Test-specific configuration can be supplied.
- Automated tests can use an isolated database.
- Application initialization is easier to maintain.

---

## ADR-004: Production Deployment Architecture

**Status:** Accepted

### Context
CampusReserve requires publicly accessible hosting for its frontend applications, backend API, and production database.

### Decision
Use:

- Vercel for the student frontend;
- Vercel for the administrator frontend;
- Render for the Flask backend;
- Aiven MySQL for the production database.

### Production Components

Student frontend:

https://campus-resource-reservation.vercel.app/

Administrator frontend:

https://campus-resource-reservation-2vz5.vercel.app/

Backend:

https://campus-resource-reservation.onrender.com

API:

https://campus-resource-reservation.onrender.com/api

### Consequences
- The application is publicly deployable.
- Frontends and backend are independently hosted.
- Production persistence is separated from application hosting.
- The system depends on external hosting and network availability.

---

## ADR-005: JWT Authentication

**Status:** Accepted

### Context
CampusReserve requires authenticated student and administrator operations.

### Decision
Use JSON Web Tokens for API authentication.

The Flask backend issues JWT access tokens after successful authentication. Protected endpoints require valid authentication tokens.

### Consequences
- Authentication is centralized in the backend.
- Protected endpoints can verify authenticated users.
- Role-based authorization can be applied to administrative operations.
- Frontends include authentication tokens when accessing protected endpoints.

---

## ADR-006: MySQL Persistence

**Status:** Accepted

### Context
CampusReserve requires persistent relational storage for users, resources, reservations, check-ins, and notifications.

### Decision
Use MySQL as the relational database and Flask-SQLAlchemy as the ORM/data-access layer.

### Consequences
- Relational database constraints support data integrity.
- SQLAlchemy provides object-relational mapping.
- Development/test and production database environments can remain separate.
- The application depends on database availability.

---

## ADR Summary

| ADR | Decision | Status |
|---|---|---|
| ADR-001 | Client-server layered REST architecture | Accepted |
| ADR-002 | React/Vite responsive web clients | Accepted |
| ADR-003 | Flask Application Factory | Accepted |
| ADR-004 | Vercel + Render + Aiven deployment | Accepted |
| ADR-005 | JWT authentication | Accepted |
| ADR-006 | MySQL persistence | Accepted |
