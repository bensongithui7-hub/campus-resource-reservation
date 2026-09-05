\# UML Component Diagram — CampusReserve



\## 1. Purpose



The UML Component Diagram describes the major software components of the CampusReserve system and the dependencies between them.



It provides a high-level view of how the student application, administrator portal, Flask REST API, authentication, application routes, and MySQL database work together.



The component structure reflects the implemented CampusReserve project.



\---



\## 2. Major Components



\### 2.1 Student Frontend



\*\*Technology:\*\* React + Vite



\*\*Location:\*\* `student-mobile/`



The Student Frontend provides the user interface for students.



Main responsibilities include:



\* Student registration.

\* Student login.

\* Session management.

\* Resource browsing.

\* Resource details.

\* Reservation creation.

\* Viewing reservations.

\* Reservation cancellation.

\* Check-in functionality.



The frontend communicates with the Flask REST API through HTTP requests.



\---



\### 2.2 Administrator Frontend



\*\*Technology:\*\* React + Vite



\*\*Location:\*\* `admin-web/`



The Administrator Frontend provides the administrative interface.



Main responsibilities include:



\* Administrator login.

\* Dashboard information.

\* Reservation management.

\* Resource management.

\* Resource availability management.

\* Check-in monitoring.

\* User management.



The frontend communicates with the Flask REST API.



\---



\### 2.3 Flask REST API



\*\*Technology:\*\* Python + Flask



\*\*Location:\*\* `backend/`



The Flask application provides the central application programming interface.



Responsibilities include:



\* Processing HTTP requests.

\* Authentication and authorization.

\* Request validation.

\* Business logic.

\* Resource management.

\* Reservation management.

\* Check-in processing.

\* Administrative operations.

\* Database interaction.

\* Returning JSON responses to frontend clients.



The API is exposed under the `/api` prefix.



\---



\### 2.4 Authentication and Authorization



\*\*Technology:\*\* Flask-JWT-Extended



The authentication component manages authenticated access to protected endpoints.



Responsibilities include:



\* Validating login credentials.

\* Generating JWT access tokens.

\* Protecting authenticated endpoints.

\* Identifying the authenticated user.

\* Restricting administrator functionality to users with the `ADMIN` role.



\---



\### 2.5 Resource Management Component



\*\*Implementation:\*\* `backend/app/routes/resource.py`



Responsibilities include:



\* Listing resources.

\* Retrieving resource details.

\* Creating resources.

\* Updating resources.

\* Updating resource availability.

\* Deleting resources.



It interacts with the `Resource` model and MySQL database.



\---



\### 2.6 Reservation Management Component



\*\*Implementation:\*\* `backend/app/routes/reservation.py`



Responsibilities include:



\* Creating reservations.

\* Listing a student's reservations.

\* Retrieving reservation details.

\* Cancelling reservations.

\* Managing reservation status.



It interacts with the `Reservation`, `User`, and `Resource` models.



\---



\### 2.7 Check-In Component



\*\*Implementation:\*\* `backend/app/routes/check\_in.py`



Responsibilities include:



\* Creating reservation check-in records.

\* Retrieving check-in information.

\* Processing QR-token check-ins.

\* Recording check-in timestamps.

\* Preventing duplicate check-ins.

\* Maintaining check-in status.



It interacts with the `Reservation` and `CheckIn` models.



\---



\### 2.8 Administration Component



\*\*Implementation:\*\* `backend/app/routes/admin.py`



Responsibilities include:



\* Viewing all reservations.

\* Viewing check-in records.

\* Viewing users.

\* Updating resources.

\* Updating resource availability.

\* Deleting resources.

\* Updating reservation status.



Administrative operations require administrator authorization.



\---



\### 2.9 Database



\*\*Technology:\*\* MySQL Community Server 8.0



\*\*Database:\*\* `campus\_reservation`



The database provides persistent storage for:



\* Users.

\* Resources.

\* Reservations.

\* Check-ins.



The Flask application accesses the database through Flask-SQLAlchemy.



\---



\## 3. Component Dependencies



The main dependency flow is:



```text

Student

&#x20;  |

&#x20;  v

Student Frontend

&#x20;  |

&#x20;  | HTTP/JSON + JWT

&#x20;  v

Flask REST API

&#x20;  |

&#x20;  +--------------------+

&#x20;  |                    |

&#x20;  v                    v

Authentication      Application Routes

&#x20;                   |    |    |    |

&#x20;                   |    |    |    +--> Admin

&#x20;                   |    |    +-------> Check-In

&#x20;                   |    +------------> Reservation

&#x20;                   +-----------------> Resource

&#x20;                             |

&#x20;                             v

&#x20;                      SQLAlchemy ORM

&#x20;                             |

&#x20;                             v

&#x20;                        MySQL Database

```



The administrator follows the same API architecture:



```text

Administrator

&#x20;     |

&#x20;     v

Admin Frontend

&#x20;     |

&#x20;     | HTTP/JSON + JWT

&#x20;     v

Flask REST API

&#x20;     |

&#x20;     v

Admin / Resource / Reservation / Check-In Routes

&#x20;     |

&#x20;     v

SQLAlchemy ORM

&#x20;     |

&#x20;     v

MySQL Database

```



\---



\## 4. Formal Component Diagram



```mermaid id="m2q2rj"

flowchart LR

&#x20;   Student(\[Student])

&#x20;   Admin(\[Administrator])



&#x20;   StudentUI\["Student Frontend<br/>React + Vite"]

&#x20;   AdminUI\["Admin Frontend<br/>React + Vite"]



&#x20;   API\["Flask REST API<br/>/api"]



&#x20;   Auth\["Authentication<br/>Flask-JWT-Extended"]



&#x20;   Resource\["Resource Management<br/>resource.py"]

&#x20;   Reservation\["Reservation Management<br/>reservation.py"]

&#x20;   CheckIn\["Check-In Management<br/>check\_in.py"]

&#x20;   AdminRoutes\["Administration<br/>admin.py"]



&#x20;   Models\["SQLAlchemy Models"]

&#x20;   DB\[(MySQL<br/>campus\_reservation)]



&#x20;   Student --> StudentUI

&#x20;   Admin --> AdminUI



&#x20;   StudentUI -->|HTTP/JSON| API

&#x20;   AdminUI -->|HTTP/JSON| API



&#x20;   API --> Auth

&#x20;   API --> Resource

&#x20;   API --> Reservation

&#x20;   API --> CheckIn

&#x20;   API --> AdminRoutes



&#x20;   Resource --> Models

&#x20;   Reservation --> Models

&#x20;   CheckIn --> Models

&#x20;   AdminRoutes --> Models



&#x20;   Models -->|SQLAlchemy ORM| DB

```



\---



\## 5. Component Interfaces



| Component              | Interface / Communication      |

| ---------------------- | ------------------------------ |

| Student Frontend       | HTTP/JSON requests to REST API |

| Admin Frontend         | HTTP/JSON requests to REST API |

| Authentication         | JWT authentication             |

| Resource Management    | REST resource endpoints        |

| Reservation Management | REST reservation endpoints     |

| Check-In Management    | REST check-in endpoints        |

| Administration         | Protected REST admin endpoints |

| SQLAlchemy Models      | ORM interface to MySQL         |

| MySQL Database         | Persistent data storage        |



\---



\## 6. API Component Groups



The REST API is organized into Flask route modules:



```text

backend/app/routes/

│

├── health.py

├── auth.py

├── protected.py

├── resource.py

├── reservation.py

├── check\_in.py

└── admin.py

```



\### Route Responsibilities



| Route Module     | Responsibility                  |

| ---------------- | ------------------------------- |

| `health.py`      | API health check                |

| `auth.py`        | Registration and authentication |

| `protected.py`   | Protected endpoint testing      |

| `resource.py`    | Resource operations             |

| `reservation.py` | Reservation operations          |

| `check\_in.py`    | Reservation and QR check-in     |

| `admin.py`       | Administrator operations        |



\---



\## 7. Data Model Components



The persistence layer contains four primary domain models:



```text

User

&#x20; |

&#x20; +----< Reservation >---- Resource

&#x20;                |

&#x20;                +---- CheckIn

```



The model components are:



| Model         | Table          |

| ------------- | -------------- |

| `User`        | `users`        |

| `Resource`    | `resources`    |

| `Reservation` | `reservations` |

| `CheckIn`     | `check\_ins`    |



\---



\## 8. Security Boundaries



The system contains an authentication boundary between public and protected operations.



\### Public Operations



Examples include:



\* Health check.

\* User registration.

\* User login.

\* Public resource retrieval where applicable.



\### Protected Operations



Protected operations require a valid JWT.



Examples include:



\* Creating reservations.

\* Viewing a student's reservations.

\* Cancelling reservations.

\* Performing reservation check-in.

\* Administrative operations.



\### Administrator Operations



Administrative endpoints additionally require the authenticated user's role to be `ADMIN`.



\---



\## 9. Frontend-to-Backend Communication



The frontends communicate with the backend using the configured API base URL:



```text

http://127.0.0.1:5000/api

```



The communication pattern is:



```text

Frontend

&#x20;  |

&#x20;  | HTTP Request

&#x20;  | Authorization: Bearer <JWT>

&#x20;  v

Flask REST API

&#x20;  |

&#x20;  | Application processing

&#x20;  v

SQLAlchemy

&#x20;  |

&#x20;  | SQL

&#x20;  v

MySQL

&#x20;  |

&#x20;  | Result

&#x20;  v

SQLAlchemy

&#x20;  |

&#x20;  v

Flask REST API

&#x20;  |

&#x20;  | JSON Response

&#x20;  v

Frontend

```



\---



\## 10. Deployment-Oriented View



During local development, the major runtime components are:



```text

┌─────────────────────────────┐

│        User Browser         │

│                             │

│  Student UI / Admin UI      │

└──────────────┬──────────────┘

&#x20;              │

&#x20;              │ HTTP

&#x20;              ▼

┌─────────────────────────────┐

│       Flask Backend         │

│                             │

│ REST API + JWT + SQLAlchemy │

└──────────────┬──────────────┘

&#x20;              │

&#x20;              │ MySQL connection

&#x20;              ▼

┌─────────────────────────────┐

│      MySQL Server 8.0       │

│                             │

│    campus\_reservation       │

└─────────────────────────────┘

```



The development frontend servers use Vite, while the Flask backend runs on port `5000`.



\---



\## 11. IBL 3300 Alignment



The Component Diagram demonstrates:



\* High-level system architecture.

\* Separation of frontend and backend responsibilities.

\* REST API architecture.

\* Authentication and authorization boundaries.

\* Modular backend route organization.

\* Database persistence.

\* Component dependencies.

\* Separation of student and administrator interfaces.

\* Traceability from architectural components to implemented source files.



The diagram complements the Class, Sequence, and Activity Diagrams by providing the system's structural component-level view.



\---



\## 12. Implementation Traceability



| UML Component          | Implementation                      |

| ---------------------- | ----------------------------------- |

| Student Frontend       | `student-mobile/`                   |

| Admin Frontend         | `admin-web/`                        |

| Flask REST API         | `backend/app/`                      |

| Authentication         | `backend/app/routes/auth.py`        |

| Resource Management    | `backend/app/routes/resource.py`    |

| Reservation Management | `backend/app/routes/reservation.py` |

| Check-In               | `backend/app/routes/check\_in.py`    |

| Administration         | `backend/app/routes/admin.py`       |

| Domain Models          | `backend/app/models/`               |

| Database               | MySQL `campus\_reservation`          |

| Database Schema        | `database/schema.sql`               |



\---



\## 13. Visual Diagram Requirement



For the final IBL 3300 submission, the Mermaid representation should be recreated or exported as a formal component diagram using draw.io or another suitable UML diagramming tool.



The final visual diagram should clearly show:



\* Student actor.

\* Administrator actor.

\* Student frontend.

\* Administrator frontend.

\* Flask REST API.

\* Authentication component.

\* Resource, reservation, check-in, and administration components.

\* SQLAlchemy/model layer.

\* MySQL database.

\* Communication/dependency relationships.



The visual diagram should remain consistent with the implemented system and the documented architecture.



