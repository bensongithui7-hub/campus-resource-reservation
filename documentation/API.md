# Architecture Decision Records (ADRs)

> Current-state decision records for the implemented CampusReserve architecture. These records document verified technical decisions made during system design and implementation.

---

## ADR-001: Client-Server Layered REST Architecture

**Status:** Accepted

### Context
CampusReserve requires separate student and administrator interfaces with centralized authentication, reservation processing, resource management, check-in processing, notifications, and database persistence.

### Decision
Use React/Vite clients communicating with a Flask REST API. The backend uses a layered architecture separating routes, application logic, models, and persistence layers.

### Consequences
- Frontends and backend can be deployed and scaled independently.
- Business operations and validation rules remain centralized.
- System responsibilities and component boundaries are cleanly separated.
- Multiple client types can consume the same RESTful API.
- Frontends depend on backend/API service availability.

---

## ADR-002: React/Vite Responsive Web Clients

**Status:** Accepted

### Context
CampusReserve requires access from both desktop and mobile-sized browser viewports.

### Decision
Implement the student and administrator client interfaces as React/Vite responsive web applications. The student client is implemented as a mobile-responsive web interface rather than a native mobile application.

### Consequences
- Users access the system directly through standard modern web browsers.
- Both desktop and mobile screen viewports are supported seamlessly.
- No platform-specific application binaries (e.g., APK/IPA) are required.
- The client implementation remains consistent across all supported user devices.

---

## ADR-003: Flask Application Factory Pattern

**Status:** Accepted

### Context
The backend requires isolated environments and distinct configurations for development, production, and automated testing.

### Decision
Implement Flask's Application Factory pattern via the `create_app()` function in `backend/app/__init__.py`. The factory instantiates the application, initializes database and security extensions, loads configuration objects, and registers API blueprints.

### Consequences
- Application instantiation is centralized in a single factory method.
- Test instances can be created independently with custom test configurations.
- Automated testing suites can run against an isolated testing database.
- Backend initialization and blueprint setup are clean and easily maintainable.

---

## ADR-004: Production Deployment Architecture

**Status:** Accepted

### Context
CampusReserve requires resilient, publicly accessible cloud hosting for its student interface, administrator portal, backend API, and database.

### Decision
Deploy the system components to the following cloud platforms:
- **Student Frontend:** Vercel
- **Administrator Frontend:** Vercel
- **Backend API:** Render
- **Database:** Aiven Managed MySQL

### Production Endpoints
- **Student Web Application:** [CampusReserve Student App](https://campus-resource-reservation.vercel.app/)[cite: 26, 30]
- **Administrator Portal:** [CampusReserve Admin App](https://campus-resource-reservation-2vz5.vercel.app/)[cite: 26, 30]
- **Backend Base URL:** `https://campus-resource-reservation.onrender.com`[cite: 26, 30]
- **REST API Base URL:** `https://campus-resource-reservation.onrender.com/api`[cite: 26, 30]

### Consequences
- The application stack is publicly accessible over HTTPS.
- Client applications and API backend services are decoupled and independently hosted.
- Database persistence is managed independently from application application servers.
- System availability relies on external platform uptime and network connectivity.

---

## ADR-005: JWT Authentication and Authorization

**Status:** Accepted

### Context
CampusReserve requires secure authentication and role-based access control for student and administrator operations.

### Decision
Implement JSON Web Tokens (JWT) for API authentication. The Flask backend issues signed JWT access tokens upon credential verification. Protected API endpoints enforce role-based authorization (`STUDENT` or `ADMIN`) by validating authorization headers.

### Consequences
- Authentication logic is fully centralized within the API backend.
- Protected endpoints securely identify and authorize incoming requests.
- Fine-grained role-based access control is enforced for administrative endpoints.
- Client applications transmit JWT tokens via Bearer headers for protected API requests.

---

## ADR-006: Relational MySQL Persistence with SQLAlchemy

**Status:** Accepted

### Context
CampusReserve requires transactional relational storage for user accounts, lab resources, reservations, check-ins, and user notifications.

### Decision
Use MySQL 8.4 as the primary relational database and Flask-SQLAlchemy (SQLAlchemy ORM) as the data-access layer.

### Consequences
- Relational schema constraints enforce foreign key integrity and data validity.
- SQLAlchemy ORM abstracts SQL queries and manages entity mappings safely.
- Isolated database instances can be configured for development, testing, and production.
- API functionality depends on database connectivity and runtime availability.

---

## Summary of Architecture Decision Records

| ADR ID | Title | Core Decision | Status |
| :--- | :--- | :--- | :--- |
| **ADR-001** | Client-Server Architecture | Layered REST API with React frontends & Flask backend | Accepted |
| **ADR-002** | Web Client Framework | React/Vite responsive web apps | Accepted |
| **ADR-003** | Flask Application Structure | Application Factory pattern (`create_app()`) | Accepted |
| **ADR-004** | Deployment Strategy | Multi-cloud deployment (Vercel + Render + Aiven) | Accepted |
| **ADR-005** | Authentication Scheme | Stateless JWT authentication with Role-Based Access Control | Accepted |
| **ADR-006** | Data Persistence Layer | Managed MySQL relational database via SQLAlchemy ORM | Accepted |
