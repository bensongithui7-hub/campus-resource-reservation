\# UML DEPLOYMENT DIAGRAM



\## 1. Purpose



The deployment diagram shows how the CampusReserve system is deployed during development. It identifies the client devices, frontend applications, backend application server, API boundary, and MySQL database server, together with the communication paths between them.



This diagram represents the current local development deployment and does not claim production cloud deployment.



\---



\## 2. Deployment Nodes



\### Node 1 — User Client / Web Browser



The system is accessed through a web browser running on the user's computer or other client device.



The browser provides access to:



\* Student Frontend

\* Administrator Frontend



\### Node 2 — Student Frontend



Technology:



\* React

\* Vite

\* JavaScript



Development address:



`http://localhost:5174`



The Student Frontend provides:



\* Registration

\* Login

\* Resource browsing

\* Resource details

\* Reservation creation

\* Reservation history

\* Reservation cancellation

\* QR/check-in functionality



\### Node 3 — Administrator Frontend



Technology:



\* React

\* Vite

\* JavaScript



Development address:



`http://localhost:5173`



The Administrator Frontend provides:



\* Administrator login

\* Dashboard

\* Resource management

\* Reservation management

\* Check-in monitoring

\* User management



\### Node 4 — Flask Application Server



Technology:



\* Python 3.14.2

\* Flask 3.1.3

\* Flask-CORS

\* Flask-JWT-Extended

\* Flask-SQLAlchemy



Development address:



`http://127.0.0.1:5000`



The backend provides the REST API under:



`/api`



It handles:



\* Authentication and authorization

\* JWT token processing

\* Resource management

\* Reservation management

\* Check-in processing

\* Administrative operations

\* Database access



\### Node 5 — MySQL Database Server



Technology:



\* MySQL Community Server 8.0.46



Database:



`campus\_reservation`



The database stores:



\* Users

\* Resources

\* Reservations

\* Check-ins



The Flask backend communicates with MySQL through SQLAlchemy and the PyMySQL database driver.



\---



\## 3. Communication Paths



\### Browser → Student Frontend



Protocol:



`HTTP`



The student accesses the React/Vite application through the browser.



\### Browser → Administrator Frontend



Protocol:



`HTTP`



The administrator accesses the React/Vite application through the browser.



\### Student Frontend → Flask API



Protocol:



`HTTP/JSON`



Base API:



`http://127.0.0.1:5000/api`



Authenticated requests use a Bearer JWT token.



\### Administrator Frontend → Flask API



Protocol:



`HTTP/JSON`



Administrative requests are authenticated and authorized using JWT-based authentication.



\### Flask Application → MySQL



The Flask application uses:



\* Flask-SQLAlchemy

\* SQLAlchemy ORM

\* PyMySQL



to communicate with the `campus\_reservation` database.



\---



\## 4. Deployment Diagram



```mermaid

flowchart TB



&#x20;   USER\["User Client Device<br/>Web Browser"]



&#x20;   subgraph FRONTENDS\["Frontend Layer"]

&#x20;       STUDENT\["Student Frontend<br/>React + Vite<br/>Port 5174"]

&#x20;       ADMIN\["Administrator Frontend<br/>React + Vite<br/>Port 5173"]

&#x20;   end



&#x20;   subgraph SERVER\["Application Server"]

&#x20;       FLASK\["Flask Application Server<br/>Python 3.14.2<br/>127.0.0.1:5000"]



&#x20;       API\["REST API<br/>/api"]



&#x20;       AUTH\["JWT Authentication<br/>Authorization"]



&#x20;       ORM\["SQLAlchemy ORM<br/>PyMySQL"]

&#x20;   end



&#x20;   subgraph DATABASE\["Database Server"]

&#x20;       MYSQL\["MySQL Community Server 8.0.46"]

&#x20;       DB\["campus\_reservation"]



&#x20;       TABLES\["users<br/>resources<br/>reservations<br/>check\_ins"]

&#x20;   end



&#x20;   USER -->|"HTTP"| STUDENT

&#x20;   USER -->|"HTTP"| ADMIN



&#x20;   STUDENT -->|"HTTP / JSON<br/>Bearer JWT"| API

&#x20;   ADMIN -->|"HTTP / JSON<br/>Bearer JWT"| API



&#x20;   API --> FLASK

&#x20;   FLASK --> AUTH

&#x20;   FLASK --> ORM



&#x20;   ORM -->|"SQL"| MYSQL

&#x20;   MYSQL --> DB

&#x20;   DB --> TABLES

```



\---



\## 5. Deployment Traceability



| Deployment Element     | Project Implementation                       |

| ---------------------- | -------------------------------------------- |

| Student Frontend       | `student-mobile/`                            |

| Administrator Frontend | `admin-web/`                                 |

| Backend Application    | `backend/`                                   |

| REST API               | Flask blueprints under `backend/app/routes/` |

| Authentication         | Flask-JWT-Extended                           |

| ORM                    | Flask-SQLAlchemy / SQLAlchemy                |

| Database Driver        | PyMySQL                                      |

| Database               | MySQL `campus\_reservation`                   |

| User Data              | `users` table                                |

| Resource Data          | `resources` table                            |

| Reservation Data       | `reservations` table                         |

| Check-In Data          | `check\_ins` table                            |



\---



\## 6. Security Boundary



The frontend applications communicate with protected backend endpoints using JWT bearer authentication.



The backend is responsible for authentication, authorization, validation, business logic, and database access. The database is not accessed directly by the frontend applications.



Therefore, the deployment follows the architectural separation:



\*\*Client → Frontend → REST API → Application Logic → Database\*\*



\---



\## 7. Deployment Environment



The current implementation is deployed for local development and testing.



The development environment consists of:



\* A web browser running the client applications

\* Vite development servers for the React frontends

\* A Flask development server for the backend

\* A local MySQL Server instance



The diagram describes the verified development architecture and should not be interpreted as a production hosting architecture.



````



\*\*After pasting:\*\* save the file, close Notepad, and return to CMD. Then run:



```cmd

git status --short

````



Send me the output. We will then commit the deployment diagram and move immediately to the \*\*actual visual UML diagrams\*\*.



