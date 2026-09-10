\# UML DEPLOYMENT DIAGRAM



\## 1. Purpose



The deployment diagram shows how the CampusReserve system is deployed across its development and production environments. It identifies the client device, frontend applications, backend application server, REST API, and database infrastructure, together with the communication paths between them.



The production deployment uses:



\* Vercel for the Student Frontend

\* Vercel for the Administrator Frontend

\* Render for the Flask REST API

\* Gunicorn as the production WSGI server

\* Aiven for the production MySQL database



The logical application architecture remains:



\*\*Client → React/Vite Frontend → Flask REST API → Application Logic → MySQL Database\*\*



The production deployment changes the hosting environment but does not change the application's logical architecture or business processes.



\---



\## 2. Deployment Nodes



\### Node 1 — User Client / Web Browser



The system is accessed through a web browser running on a user's computer or other supported client device.



The browser provides access to:



\* Student Frontend

\* Administrator Frontend



The browser communicates with the deployed frontend applications over HTTPS.



\---



\### Node 2 — Student Frontend



Technology:



\* React

\* Vite

\* JavaScript



Production hosting:



\*\*Vercel\*\*



Production address:



`https://campus-resource-reservation.vercel.app/`



Production API configuration:



`VITE\_API\_BASE\_URL=https://campus-resource-reservation.onrender.com/api`



The Student Frontend provides:



\* Registration

\* Login

\* Resource browsing

\* Resource details

\* Reservation creation

\* Reservation history

\* Reservation cancellation

\* Reservation check-in

\* Notifications



The frontend does not connect directly to the production database. All application data is accessed through the Flask REST API.



\---



\### Node 3 — Administrator Frontend



Technology:



\* React

\* Vite

\* JavaScript



Production hosting:



\*\*Vercel\*\*



Production address:



`https://campus-resource-reservation-2vz5.vercel.app/`



Production API configuration:



`VITE\_API\_BASE\_URL=https://campus-resource-reservation.onrender.com/api`



The Administrator Frontend provides:



\* Administrator login

\* Dashboard

\* Resource management

\* Reservation management

\* Check-in monitoring

\* User management



The Administrator Frontend communicates with the Flask REST API over HTTPS and does not access the production database directly.



\---



\### Node 4 — Render Application Platform



The production backend is hosted on \*\*Render\*\*.



Backend technology:



\* Python 3.14.2

\* Flask 3.1.3

\* Flask-CORS

\* Flask-JWT-Extended

\* Flask-SQLAlchemy

\* SQLAlchemy

\* PyMySQL



Production WSGI server:



\* Gunicorn



Production backend address:



`https://campus-resource-reservation.onrender.com`



Production API base URL:



`https://campus-resource-reservation.onrender.com/api`



The backend provides the REST API and handles:



\* Authentication

\* Authorization

\* JWT token processing

\* Resource management

\* Reservation management

\* Check-in processing

\* Notification processing

\* Administrative operations

\* Request validation

\* Business logic

\* Database access



The backend is the security and application boundary between the frontend clients and the production database.



\---



\### Node 5 — Production MySQL Database



The production database is hosted by \*\*Aiven\*\*.



Database technology:



\* MySQL



Production MySQL version:



\* MySQL 8.4.x



The production database stores:



\* Users

\* Resources

\* Reservations

\* Check-ins

\* Notifications



The Flask backend communicates with the production database through:



\* Flask-SQLAlchemy

\* SQLAlchemy ORM

\* PyMySQL



The production database connection is configured through the backend `DATABASE\_URL` environment variable.



Database credentials are stored server-side and are not exposed to either frontend application.



Communication between the production backend and Aiven MySQL uses SSL-secured database communication.



\---



\## 3. Production Communication Paths



\### Browser → Student Frontend



Protocol:



`HTTPS`



The user accesses the deployed Student Frontend through the Vercel production URL.



\---



\### Browser → Administrator Frontend



Protocol:



`HTTPS`



The administrator accesses the deployed Administrator Frontend through the Vercel production URL.



\---



\### Student Frontend → Flask REST API



Protocol:



`HTTPS / JSON`



Production API:



`https://campus-resource-reservation.onrender.com/api`



Authenticated requests use a Bearer JWT token.



\---



\### Administrator Frontend → Flask REST API



Protocol:



`HTTPS / JSON`



Administrative requests use JWT-based authentication and authorization.



The backend verifies the authenticated user's permissions before allowing protected administrative operations.



\---



\### Flask REST API → Aiven MySQL



Protocol:



`MySQL over SSL`



The Flask application uses:



\* Flask-SQLAlchemy

\* SQLAlchemy ORM

\* PyMySQL



to communicate with the production MySQL database.



The frontend applications never communicate directly with the database.



\---



\## 4. Production Deployment Diagram



```mermaid

flowchart TB



&#x20;   USER\["User Client Device<br/>Web Browser"]



&#x20;   subgraph VERCEL\["Vercel — Frontend Hosting"]

&#x20;       STUDENT\["Student Frontend<br/>React + Vite<br/>campus-resource-reservation.vercel.app"]



&#x20;       ADMIN\["Administrator Frontend<br/>React + Vite<br/>campus-resource-reservation-2vz5.vercel.app"]

&#x20;   end



&#x20;   subgraph RENDER\["Render — Production Application Platform"]

&#x20;       GUNICORN\["Gunicorn<br/>Production WSGI Server"]



&#x20;       FLASK\["Flask Application<br/>Python 3.14.2"]



&#x20;       API\["REST API<br/>/api"]



&#x20;       AUTH\["JWT Authentication<br/>Authorization"]



&#x20;       LOGIC\["Application Logic<br/>Validation + Business Rules"]



&#x20;       ORM\["SQLAlchemy ORM<br/>PyMySQL"]

&#x20;   end



&#x20;   subgraph AIVEN\["Aiven — Production Database"]

&#x20;       MYSQL\["MySQL 8.4.x"]



&#x20;       DB\["CampusReserve Production Database"]



&#x20;       TABLES\["users<br/>resources<br/>reservations<br/>check\_ins<br/>notifications"]

&#x20;   end



&#x20;   USER -->|"HTTPS"| STUDENT

&#x20;   USER -->|"HTTPS"| ADMIN



&#x20;   STUDENT -->|"HTTPS / JSON<br/>Bearer JWT"| API

&#x20;   ADMIN -->|"HTTPS / JSON<br/>Bearer JWT"| API



&#x20;   API --> GUNICORN

&#x20;   GUNICORN --> FLASK



&#x20;   FLASK --> AUTH

&#x20;   FLASK --> LOGIC

&#x20;   LOGIC --> ORM



&#x20;   ORM -->|"MySQL over SSL"| MYSQL

&#x20;   MYSQL --> DB

&#x20;   DB --> TABLES

```



\---



\## 5. Production Deployment Traceability



| Deployment Element          | Project Implementation                       |

| --------------------------- | -------------------------------------------- |

| Student Frontend            | `student-mobile/`                            |

| Administrator Frontend      | `admin-web/`                                 |

| Backend Application         | `backend/`                                   |

| REST API                    | Flask blueprints under `backend/app/routes/` |

| Authentication              | Flask-JWT-Extended                           |

| ORM                         | Flask-SQLAlchemy / SQLAlchemy                |

| Database Driver             | PyMySQL                                      |

| Production Frontend Hosting | Vercel                                       |

| Production Backend Hosting  | Render                                       |

| Production WSGI Server      | Gunicorn                                     |

| Production Database Hosting | Aiven                                        |

| Production Database         | MySQL 8.4.x                                  |

| User Data                   | `users` table                                |

| Resource Data               | `resources` table                            |

| Reservation Data            | `reservations` table                         |

| Check-In Data               | `check\_ins` table                            |

| Notification Data           | `notifications` table                        |



\---



\## 6. Production URLs



\### Student Frontend



`https://campus-resource-reservation.vercel.app/`



\### Administrator Frontend



`https://campus-resource-reservation-2vz5.vercel.app/`



\### Production Backend



`https://campus-resource-reservation.onrender.com`



\### Production API



`https://campus-resource-reservation.onrender.com/api`



\### Production Health Endpoint



`https://campus-resource-reservation.onrender.com/api/health`



\---



\## 7. Security Boundary



The frontend applications communicate with protected backend endpoints using JWT bearer authentication.



The backend is responsible for:



\* Authentication

\* Authorization

\* Request validation

\* Business logic

\* Database access



The production database is not accessed directly by either frontend application.



The production security boundary is therefore:



\*\*Client → HTTPS → Frontend → HTTPS/REST API → Application Logic → SSL-secured Database\*\*



Production CORS configuration restricts cross-origin access to the deployed CampusReserve frontend origins.



Production database credentials remain on the backend and are supplied through server-side environment variables.



\---



\## 8. Production Environment



The current production environment consists of:



\* User web browsers

\* Student React/Vite application hosted on Vercel

\* Administrator React/Vite application hosted on Vercel

\* Flask REST API hosted on Render

\* Gunicorn production WSGI server

\* Aiven MySQL production database



The production deployment is operational and represents the current hosted CampusReserve architecture.



\---



\## 9. Development Deployment



The production deployment is the primary deployment model, while local development remains available for development and testing.



The local development environment consists of:



\* A web browser

\* Vite development servers

\* Flask development server

\* Local MySQL Community Server



Typical local development addresses are:



\### Student Frontend



`http://localhost:5174`



\### Administrator Frontend



`http://localhost:5173`



\### Local Flask Backend



`http://127.0.0.1:5000`



\### Local API



`http://127.0.0.1:5000/api`



The local development environment uses the same logical application architecture as production but replaces cloud hosting services with local development servers and a local MySQL instance.



\---



\## 10. Development vs Production Deployment



| Layer                  | Development                     | Production                       |

| ---------------------- | ------------------------------- | -------------------------------- |

| Student Frontend       | Vite development server         | Vercel                           |

| Administrator Frontend | Vite development server         | Vercel                           |

| Backend                | Flask development server        | Render + Gunicorn                |

| API                    | `127.0.0.1:5000/api`            | Render HTTPS API                 |

| Database               | MySQL Community Server 8.0.46   | Aiven MySQL 8.4.x                |

| Frontend → Backend     | HTTP                            | HTTPS                            |

| Backend → Database     | Local MySQL connection          | SSL-secured MySQL connection     |

| Configuration          | Local environment configuration | Deployment environment variables |



\---



\## 11. Architectural Traceability



The deployment architecture preserves the system's layered/client-server REST design.



\### Presentation Layer



Implemented by:



\* Student React/Vite frontend

\* Administrator React/Vite frontend



Hosted in production on Vercel.



\### Application Layer



Implemented by:



\* Flask REST API

\* Authentication and authorization

\* Reservation logic

\* Resource management

\* Check-in processing

\* Notification processing

\* Administrative operations



Hosted in production on Render using Gunicorn.



\### Data Layer



Implemented by:



\* MySQL database

\* SQLAlchemy ORM

\* PyMySQL database driver



Hosted in production on Aiven.



The deployment infrastructure therefore supports the existing application architecture without introducing microservices or changing the system's functional design.



\---



\## 12. Deployment Environment Summary



The CampusReserve system is deployed as a three-tier web application:



```text

User Browser

&#x20;    |

&#x20;    | HTTPS

&#x20;    v

Vercel Frontends

(Student + Administrator)

&#x20;    |

&#x20;    | HTTPS / REST / JSON

&#x20;    v

Render

Flask REST API + Gunicorn

&#x20;    |

&#x20;    | MySQL over SSL

&#x20;    v

Aiven

MySQL Production Database

```



This deployment separates presentation, application, and data responsibilities while maintaining a single centralized REST backend and production relational database.



\---



\## 13. Deployment Status



The current deployment configuration is:



\* Student frontend — deployed on Vercel

\* Administrator frontend — deployed on Vercel

\* Flask backend — deployed on Render

\* Gunicorn — configured as the production WSGI server

\* Production MySQL — hosted on Aiven

\* Production environment configuration — implemented

\* Production CORS — restricted to deployed frontend origins

\* HTTPS frontend-to-backend communication — implemented

\* SSL-secured backend-to-database communication — implemented



The deployed system has been manually exercised through the student and administrator applications, with the production frontend, backend, and database working together as the deployed CampusReserve system.



\---



\## 14. Deployment Conclusion



The CampusReserve production deployment uses:



\*\*Vercel → Render → Aiven\*\*



for the frontend, application, and database layers respectively.



The deployment preserves the project's established:



\*\*Client → Frontend → REST API → Application Logic → Database\*\*



architecture.



No microservices architecture or native mobile deployment is required for the implemented system. The Student Frontend is a React/Vite responsive web application that is accessible through a web browser.



The local development deployment remains documented separately so that development and production environments are clearly distinguished.



