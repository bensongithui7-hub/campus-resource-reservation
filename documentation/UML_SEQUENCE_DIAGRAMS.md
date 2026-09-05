\# UML Sequence Diagrams — CampusReserve



\## 1. Purpose



The UML Sequence Diagrams describe the chronological interactions between users, the CampusReserve frontend, backend API, authentication layer, database, and QR check-in functionality.



The diagrams focus on the system's principal workflows and demonstrate how the implemented components collaborate to complete each operation.



\---



\## 2. Student Login



\### Participants



\* Student

\* Student Frontend

\* Authentication API

\* User Database



\### Interaction



1\. Student enters email and password.

2\. Student Frontend sends login credentials to the authentication API.

3\. Authentication API validates the request.

4\. The API retrieves the user account from the database.

5\. The password is verified against the stored password hash.

6\. A JWT access token is generated.

7\. The token and user information are returned to the frontend.

8\. The frontend stores the authenticated session.

9\. Student is granted access to protected functionality.



\### Sequence Diagram



```mermaid

sequenceDiagram

&#x20;   actor Student

&#x20;   participant Frontend as Student Frontend

&#x20;   participant Auth as Authentication API

&#x20;   participant DB as User Database



&#x20;   Student->>Frontend: Enter email and password

&#x20;   Frontend->>Auth: POST /api/auth/login

&#x20;   Auth->>DB: Find user by email

&#x20;   DB-->>Auth: User record

&#x20;   Auth->>Auth: Verify password hash

&#x20;   Auth->>Auth: Generate JWT

&#x20;   Auth-->>Frontend: JWT + user information

&#x20;   Frontend->>Frontend: Store authenticated session

&#x20;   Frontend-->>Student: Display authenticated dashboard

```



\---



\## 3. Create Reservation



\### Participants



\* Student

\* Student Frontend

\* Reservation API

\* Resource Database

\* Reservation Database



\### Interaction



1\. Student selects a resource.

2\. Student enters reservation date, start time, end time, and purpose.

3\. Frontend sends the reservation request with the JWT.

4\. Reservation API authenticates the student.

5\. The requested resource is retrieved.

6\. The API validates the resource and reservation data.

7\. The reservation is created and stored.

8\. The created reservation is returned to the frontend.

9\. The frontend displays the reservation confirmation.



\### Sequence Diagram



```mermaid

sequenceDiagram

&#x20;   actor Student

&#x20;   participant Frontend as Student Frontend

&#x20;   participant API as Reservation API

&#x20;   participant ResourceDB as Resource Database

&#x20;   participant ReservationDB as Reservation Database



&#x20;   Student->>Frontend: Select resource and enter booking details

&#x20;   Frontend->>API: POST /api/reservations + JWT

&#x20;   API->>API: Authenticate student

&#x20;   API->>ResourceDB: Retrieve requested resource

&#x20;   ResourceDB-->>API: Resource record

&#x20;   API->>API: Validate resource and date/time

&#x20;   API->>ReservationDB: Create reservation

&#x20;   ReservationDB-->>API: Created reservation

&#x20;   API-->>Frontend: Reservation details

&#x20;   Frontend-->>Student: Display reservation confirmation

```



\### Alternative Outcomes



If validation fails, the API returns an appropriate error response instead of creating the reservation.



Examples include:



\* Required reservation information is missing.

\* Resource does not exist.

\* Resource is unavailable.

\* Reservation date or time is invalid.

\* Start time is not before end time.



\---



\## 4. Cancel Reservation



\### Participants



\* Student

\* Student Frontend

\* Reservation API

\* Reservation Database



\### Interaction



1\. Student opens their reservations.

2\. Student selects a reservation to cancel.

3\. Frontend sends the cancellation request with the JWT.

4\. API authenticates the student.

5\. API retrieves the requested reservation.

6\. Ownership is checked.

7\. Reservation status is changed to `CANCELLED`.

8\. The API returns a successful response.

9\. Frontend updates the reservation display.



\### Sequence Diagram



```mermaid

sequenceDiagram

&#x20;   actor Student

&#x20;   participant Frontend as Student Frontend

&#x20;   participant API as Reservation API

&#x20;   participant DB as Reservation Database



&#x20;   Student->>Frontend: Select reservation to cancel

&#x20;   Frontend->>API: DELETE /api/reservations/{id} + JWT

&#x20;   API->>API: Authenticate student

&#x20;   API->>DB: Retrieve reservation

&#x20;   DB-->>API: Reservation record

&#x20;   API->>API: Verify reservation ownership

&#x20;   API->>DB: Set status to CANCELLED

&#x20;   DB-->>API: Updated reservation

&#x20;   API-->>Frontend: Cancellation confirmation

&#x20;   Frontend-->>Student: Update reservation history

```



\### Alternative Outcomes



The cancellation operation fails when:



\* The reservation does not exist.

\* The authenticated student does not own the reservation.

\* The reservation has already been cancelled.



\---



\## 5. QR Check-In



\### Participants



\* Student

\* Student Frontend

\* Check-In API

\* Reservation Database

\* Check-In Database



\### Interaction



1\. Student accesses the check-in function for a reservation.

2\. The frontend sends the check-in request.

3\. Check-In API authenticates the student.

4\. The reservation is retrieved.

5\. The API verifies that the reservation belongs to the student.

6\. The reservation status and check-in eligibility are validated.

7\. The check-in record is created or updated.

8\. The check-in status becomes `CHECKED\_IN`.

9\. The check-in timestamp is recorded.

10\. The frontend displays successful check-in.



\### Sequence Diagram



```mermaid

sequenceDiagram

&#x20;   actor Student

&#x20;   participant Frontend as Student Frontend

&#x20;   participant API as Check-In API

&#x20;   participant ReservationDB as Reservation Database

&#x20;   participant CheckInDB as Check-In Database



&#x20;   Student->>Frontend: Open reservation check-in

&#x20;   Frontend->>API: POST /api/reservations/{id}/check-in + JWT

&#x20;   API->>API: Authenticate student

&#x20;   API->>ReservationDB: Retrieve reservation

&#x20;   ReservationDB-->>API: Reservation record

&#x20;   API->>API: Verify ownership and eligibility

&#x20;   API->>CheckInDB: Create/update check-in record

&#x20;   CheckInDB-->>API: CHECKED\_IN record

&#x20;   API-->>Frontend: Check-in confirmation

&#x20;   Frontend-->>Student: Display successful check-in

```



\### QR Token Check-In



The system also supports QR-token-based check-in:



```mermaid

sequenceDiagram

&#x20;   actor Student

&#x20;   participant Frontend as Student Frontend

&#x20;   participant API as Check-In API

&#x20;   participant DB as Check-In Database



&#x20;   Student->>Frontend: Scan/use QR token

&#x20;   Frontend->>API: POST /api/check-in/{qr\_token}

&#x20;   API->>DB: Find check-in record by QR token

&#x20;   DB-->>API: Check-in record

&#x20;   API->>API: Validate check-in eligibility

&#x20;   API->>DB: Update check-in status

&#x20;   DB-->>API: Updated check-in

&#x20;   API-->>Frontend: Check-in result

&#x20;   Frontend-->>Student: Display check-in status

```



\### Duplicate Check-In Protection



If the reservation has already been checked in, the API rejects the duplicate operation rather than creating another successful check-in.



\---



\## 6. Admin Manage Reservation



\### Participants



\* Administrator

\* Admin Frontend

\* Admin API

\* Reservation Database



\### Interaction



1\. Administrator logs into the admin portal.

2\. Administrator opens reservation management.

3\. Admin Frontend requests reservation records.

4\. Admin API authenticates and authorizes the administrator.

5\. Reservation records are retrieved.

6\. Administrator selects a reservation and changes its status.

7\. Frontend sends the update request.

8\. API validates the new status.

9\. Reservation status is updated.

10\. Updated information is returned to the frontend.



\### Sequence Diagram



```mermaid

sequenceDiagram

&#x20;   actor Admin as Administrator

&#x20;   participant Frontend as Admin Frontend

&#x20;   participant API as Admin API

&#x20;   participant DB as Reservation Database



&#x20;   Admin->>Frontend: Open reservation management

&#x20;   Frontend->>API: GET /api/admin/reservations + JWT

&#x20;   API->>API: Authenticate and authorize admin

&#x20;   API->>DB: Retrieve reservations

&#x20;   DB-->>API: Reservation records

&#x20;   API-->>Frontend: Reservation records

&#x20;   Frontend-->>Admin: Display reservations



&#x20;   Admin->>Frontend: Change reservation status

&#x20;   Frontend->>API: PUT /api/admin/reservations/{id}/status

&#x20;   API->>API: Authenticate and authorize admin

&#x20;   API->>DB: Retrieve reservation

&#x20;   DB-->>API: Reservation record

&#x20;   API->>API: Validate new status

&#x20;   API->>DB: Update reservation status

&#x20;   DB-->>API: Updated reservation

&#x20;   API-->>Frontend: Updated reservation

&#x20;   Frontend-->>Admin: Display updated status

```



\---



\## 7. Sequence Diagram Summary



| Diagram                  | Primary Actor | Main API           | Main Operation                  |

| ------------------------ | ------------- | ------------------ | ------------------------------- |

| Student Login            | Student       | Authentication API | Authenticate user and issue JWT |

| Create Reservation       | Student       | Reservation API    | Create resource reservation     |

| Cancel Reservation       | Student       | Reservation API    | Cancel owned reservation        |

| QR Check-In              | Student       | Check-In API       | Record reservation check-in     |

| Admin Manage Reservation | Administrator | Admin API          | View and update reservations    |



\---



\## 8. Implementation Traceability



The sequence diagrams correspond to the implemented API endpoints:



| Workflow                 | Implemented Endpoint                               |

| ------------------------ | -------------------------------------------------- |

| Student Login            | `POST /api/auth/login`                             |

| Create Reservation       | `POST /api/reservations`                           |

| View Reservations        | `GET /api/reservations`                            |

| Cancel Reservation       | `DELETE /api/reservations/<id>`                    |

| Reservation Check-In     | `POST /api/reservations/<reservation\_id>/check-in` |

| QR Check-In              | `POST /api/check-in/<qr\_token>`                    |

| Admin Reservations       | `GET /api/admin/reservations`                      |

| Admin Reservation Status | `PUT /api/admin/reservations/<id>/status`          |



\---



\## 9. UML Diagram Creation



The Mermaid diagrams above provide the logical sequence representations.



For the formal IBL 3300 submission, the diagrams should also be recreated as visual UML diagrams using draw.io or another UML-compatible diagramming tool.



Each visual diagram should show:



\* Actor

\* Frontend/client

\* Relevant API/controller

\* Database or persistence component

\* Ordered messages

\* Return messages

\* Authentication/authorization where applicable

\* Alternative/error outcomes where relevant



The visual diagrams should preserve the same interactions documented in this file.



\---



\## 10. IBL 3300 Alignment



The sequence diagrams demonstrate:



\* Dynamic system behaviour.

\* Interaction between actors and software components.

\* API request and response flow.

\* Authentication and authorization.

\* Database interaction.

\* Reservation lifecycle operations.

\* QR-based check-in.

\* Administrator operations.



Together with the Use-Case and Class Diagrams, these sequence diagrams provide traceability from requirements to system behaviour and implementation.



