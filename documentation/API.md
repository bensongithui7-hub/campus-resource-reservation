\# CampusReserve API Documentation



\## 1. Overview



CampusReserve provides a REST-style HTTP API for managing campus facilities, lab equipment, reservations, and reservation check-ins.



The backend is implemented using Flask and exposes its API under the `/api` prefix.



\### Base URL



```text

http://127.0.0.1:5000/api

```



For deployment, the base URL should be changed to the deployed backend URL.



\---



\## 2. Technology



The API uses:



\* Python 3.14.2

\* Flask 3.1.3

\* Flask-SQLAlchemy 3.1.1

\* Flask-JWT-Extended 4.7.4

\* Flask-CORS 6.0.5

\* PyMySQL 1.2.0

\* MySQL 8.0.46



Authentication is implemented using JSON Web Tokens (JWT).



\---



\## 3. Authentication



\### 3.1 Registration



\*\*Endpoint\*\*



```http

POST /api/auth/register

```



\*\*Purpose\*\*



Creates a new student account.



\*\*Request body\*\*



```json

{

&#x20; "name": "Example Student",

&#x20; "student\_id": "STU100",

&#x20; "email": "student@example.com",

&#x20; "password": "password"

}

```



\*\*Successful response\*\*



The API returns a successful account-creation response.



Registration validates required account information and prevents duplicate email addresses and student IDs.



\---



\### 3.2 Login



\*\*Endpoint\*\*



```http

POST /api/auth/login

```



\*\*Purpose\*\*



Authenticates a registered user and returns a JWT access token.



\*\*Request body\*\*



```json

{

&#x20; "email": "student@example.com",

&#x20; "password": "password"

}

```



The returned access token is required for protected endpoints.



\---



\## 4. Authorization



Protected requests use the JWT access token in the HTTP Authorization header.



```http

Authorization: Bearer <access\_token>

```



The system distinguishes between:



\* `STUDENT`

\* `ADMIN`



Administrative endpoints require an authenticated administrator.



A student attempting to access an administrator-only endpoint is rejected.



\---



\# 5. Health API



\## 5.1 Health Check



```http

GET /api/health

```



\*\*Purpose\*\*



Checks whether the backend API is running.



\*\*Authentication\*\*



Not required.



\*\*Successful response\*\*



```json

{

&#x20; "status": "ok"

}

```



\---



\# 6. Resource API



Resources represent campus facilities or equipment that can be reserved.



Supported resource types are:



\* `LABORATORY`

\* `STUDY\_ROOM`

\* `EQUIPMENT`



Supported resource statuses are:



\* `AVAILABLE`

\* `UNAVAILABLE`



\---



\## 6.1 List Resources



```http

GET /api/resources

```



\*\*Purpose\*\*



Returns the resources available in the system.



\*\*Authentication\*\*



Not required.



\---



\## 6.2 Get Resource



```http

GET /api/resources/<id>

```



\*\*Purpose\*\*



Returns information for one resource.



\*\*Path parameter\*\*



| Parameter | Description |

| --------- | ----------- |

| `id`      | Resource ID |



\*\*Authentication\*\*



Not required.



If the resource does not exist, the API returns an appropriate not-found response.



\---



\## 6.3 Create Resource



```http

POST /api/resources

```



\*\*Purpose\*\*



Creates a new campus resource.



\*\*Authentication\*\*



Required.



\*\*Authorization\*\*



Administrator only.



\*\*Request body\*\*



```json

{

&#x20; "name": "Computer Lab 3",

&#x20; "type": "LABORATORY",

&#x20; "description": "Computer laboratory",

&#x20; "location": "Main Campus",

&#x20; "capacity": 30,

&#x20; "status": "AVAILABLE"

}

```



The resource type must be one of the supported resource types.



Capacity must be a valid positive value.



\---



\# 7. Reservation API



Reservations associate a student with a resource for a specified date and time period.



Supported reservation statuses are:



\* `PENDING`

\* `CONFIRMED`

\* `CANCELLED`

\* `COMPLETED`



\---



\## 7.1 Create Reservation



```http

POST /api/reservations

```



\*\*Purpose\*\*



Creates a reservation for the authenticated student.



\*\*Authentication\*\*



Required.



The reservation request validates:



\* Required reservation fields

\* Resource existence

\* Resource availability

\* Reservation date

\* Start time

\* End time

\* Valid chronological ordering of the reservation period



The start time must occur before the end time.



\---



\## 7.2 List Current User Reservations



```http

GET /api/reservations

```



\*\*Purpose\*\*



Returns reservations belonging to the authenticated user.



\*\*Authentication\*\*



Required.



Students can therefore view their own reservation history without accessing another user's reservations.



\---



\## 7.3 Get Reservation



```http

GET /api/reservations/<id>

```



\*\*Purpose\*\*



Returns details for a specific reservation.



\*\*Authentication\*\*



Required.



A student can access their own reservation.



Users cannot use this endpoint to access another student's reservation.



\---



\## 7.4 Cancel Reservation



```http

DELETE /api/reservations/<id>

```



\*\*Purpose\*\*



Cancels a reservation owned by the authenticated student.



\*\*Authentication\*\*



Required.



A reservation cannot be cancelled by another student.



Already-cancelled reservations are handled appropriately by the API.



\---



\# 8. Check-in API



CampusReserve supports reservation check-in using reservation-specific check-in data and QR/token-based check-in.



A reservation must satisfy the system's check-in requirements before check-in is accepted.



\---



\## 8.1 Check In to Reservation



```http

POST /api/reservations/<reservation\_id>/check-in

```



\*\*Purpose\*\*



Checks the authenticated student into a specific reservation.



\*\*Authentication\*\*



Required.



The endpoint validates reservation ownership and reservation status before creating the check-in record.



Duplicate check-ins are prevented.



\---



\## 8.2 Get Reservation Check-in



```http

GET /api/reservations/<reservation\_id>/check-in

```



\*\*Purpose\*\*



Returns the check-in information associated with a reservation.



\*\*Authentication\*\*



Required.



\---



\## 8.3 QR/Token Check-in



```http

POST /api/check-in/<qr\_token>

```



\*\*Purpose\*\*



Processes check-in using the reservation's QR/token value.



The token identifies the reservation check-in operation.



The endpoint prevents invalid or already-completed check-in operations.



\---



\# 9. Administrator API



Administrator endpoints provide management functionality for reservations, resources, users, and check-ins.



All administrator endpoints require an authenticated administrator.



\---



\## 9.1 List All Reservations



```http

GET /api/admin/reservations

```



\*\*Purpose\*\*



Returns reservation information for administrative management.



\*\*Authentication\*\*



Required.



\*\*Authorization\*\*



Administrator only.



\---



\## 9.2 Update Reservation Status



```http

PUT /api/admin/reservations/<id>/status

```



\*\*Purpose\*\*



Allows an administrator to update the status of a reservation.



\*\*Authentication\*\*



Required.



\*\*Authorization\*\*



Administrator only.



\*\*Request body\*\*



```json

{

&#x20; "status": "CONFIRMED"

}

```



The status must be one of the supported reservation statuses.



\---



\## 9.3 Update Resource



```http

PUT /api/admin/resources/<id>

```



\*\*Purpose\*\*



Updates an existing resource.



\*\*Authentication\*\*



Required.



\*\*Authorization\*\*



Administrator only.



Resource information that can be managed includes the resource's descriptive and operational fields, subject to validation.



\---



\## 9.4 Update Resource Status



```http

PUT /api/admin/resources/<id>/status

```



\*\*Purpose\*\*



Changes the availability status of an existing resource.



\*\*Authentication\*\*



Required.



\*\*Authorization\*\*



Administrator only.



Supported statuses:



```text

AVAILABLE

UNAVAILABLE

```



\---



\## 9.5 Delete Resource



```http

DELETE /api/admin/resources/<id>

```



\*\*Purpose\*\*



Removes a resource from the system.



\*\*Authentication\*\*



Required.



\*\*Authorization\*\*



Administrator only.



\---



\## 9.6 List Check-ins



```http

GET /api/admin/check-ins

```



\*\*Purpose\*\*



Returns check-in records for administrative monitoring.



\*\*Authentication\*\*



Required.



\*\*Authorization\*\*



Administrator only.



\---



\## 9.7 List Users



```http

GET /api/admin/users

```



\*\*Purpose\*\*



Returns user information for administrative management.



\*\*Authentication\*\*



Required.



\*\*Authorization\*\*



Administrator only.



\---



\# 10. Endpoint Summary



| Method | Endpoint                                      | Authentication | Access             |

| ------ | --------------------------------------------- | -------------- | ------------------ |

| GET    | `/api/health`                                 | No             | Public             |

| POST   | `/api/auth/register`                          | No             | Public             |

| POST   | `/api/auth/login`                             | No             | Public             |

| GET    | `/api/resources`                              | No             | Public             |

| GET    | `/api/resources/<id>`                         | No             | Public             |

| POST   | `/api/resources`                              | Yes            | Admin              |

| POST   | `/api/reservations`                           | Yes            | Student            |

| GET    | `/api/reservations`                           | Yes            | Student            |

| GET    | `/api/reservations/<id>`                      | Yes            | Owner              |

| DELETE | `/api/reservations/<id>`                      | Yes            | Owner              |

| POST   | `/api/reservations/<reservation\_id>/check-in` | Yes            | Student/Owner      |

| GET    | `/api/reservations/<reservation\_id>/check-in` | Yes            | Authorized user    |

| POST   | `/api/check-in/<qr\_token>`                    | Yes            | Authenticated user |

| GET    | `/api/admin/reservations`                     | Yes            | Admin              |

| PUT    | `/api/admin/reservations/<id>/status`         | Yes            | Admin              |

| PUT    | `/api/admin/resources/<id>`                   | Yes            | Admin              |

| PUT    | `/api/admin/resources/<id>/status`            | Yes            | Admin              |

| DELETE | `/api/admin/resources/<id>`                   | Yes            | Admin              |

| GET    | `/api/admin/check-ins`                        | Yes            | Admin              |

| GET    | `/api/admin/users`                            | Yes            | Admin              |



\---



\# 11. Common HTTP Responses



The API uses standard HTTP status codes to communicate the result of requests.



Common categories include:



| Status | Meaning                                            |

| ------ | -------------------------------------------------- |

| `200`  | Request completed successfully                     |

| `201`  | Resource successfully created                      |

| `400`  | Invalid request or validation failure              |

| `401`  | Authentication required or authentication failed   |

| `403`  | Authenticated user does not have permission        |

| `404`  | Requested resource or record does not exist        |

| `409`  | Request conflicts with an existing record or state |



Exact response bodies depend on the endpoint and error condition.



\---



\# 12. Validation and Business Rules



The API implements validation at the backend rather than relying only on frontend validation.



Important rules include:



1\. Required fields must be supplied.

2\. Duplicate user email addresses are rejected.

3\. Duplicate student IDs are rejected.

4\. Resources must exist before they can be reserved.

5\. Resources must be available for reservation.

6\. Reservation start time must precede end time.

7\. Users can only manage their own student reservations.

8\. Administrative operations require administrator authorization.

9\. Reservation statuses must use supported values.

10\. Resource types must use supported values.

11\. Resource capacity must be valid.

12\. Duplicate check-ins are prevented.

13\. Check-in ownership and reservation status are validated.

14\. Invalid resource and reservation IDs are handled without creating invalid records.



\---



\# 13. Database Entities



The API operates on four primary database entities:



\### Users



Stores student and administrator accounts.



Important information includes:



\* User ID

\* Name

\* Student ID

\* Email

\* Password hash

\* Role



\### Resources



Stores reservable facilities and equipment.



Important information includes:



\* Resource ID

\* Name

\* Type

\* Description

\* Location

\* Capacity

\* Status



\### Reservations



Stores bookings made against resources.



Important information includes:



\* Reservation ID

\* User

\* Resource

\* Reservation date

\* Start time

\* End time

\* Status



\### Check-ins



Stores reservation check-in information.



Important information includes:



\* Check-in ID

\* Reservation

\* Check-in status

\* Check-in timestamp

\* QR/token information used by the check-in workflow



\---



\# 14. Client Integration



The student frontend communicates with the API through service modules for:



\* Authentication

\* Resources

\* Reservations

\* Check-in



The administrator frontend communicates with the same backend API for administrative operations.



The frontend API base URL used during local development is:



```text

http://127.0.0.1:5000/api

```



The backend must be running before either frontend can successfully perform API operations.



\---



\# 15. Security Considerations



The API uses JWT authentication for protected operations.



Security requirements include:



\* Passwords must not be stored as plaintext.

\* JWT-protected endpoints must validate the access token.

\* Administrative endpoints must enforce administrator authorization.

\* Users must not be able to access other users' private reservations.

\* Environment secrets must remain outside source control.

\* Production deployments must use secure secret values.

\* Production deployments should use HTTPS.

\* Client applications must use the deployed API URL rather than the local development URL.



No passwords or environment secrets are included in this documentation.



\---



\# 16. Testing



The backend API has automated pytest coverage.



Current verified test result:



```text

108 passed

```



Overall backend application coverage:



```text

99%

```



The test suite covers:



\* Authentication

\* Registration

\* Login

\* Protected routes

\* Resource management

\* Resource validation

\* Reservation creation

\* Reservation retrieval

\* Reservation cancellation

\* Reservation authorization

\* Administrator operations

\* Check-in

\* Duplicate check-in prevention

\* Error handling

\* Access control



Backend tests are located in:



```text

backend/tests/

```



The test suite can be executed with:



```cmd

cd backend

python -m pytest --cov=app --cov-report=term-missing -q

```



\---



\# 17. Continuous Integration



Backend CI is configured through:



```text

.github/workflows/backend-ci.yml

```



The workflow installs the backend dependencies and runs the automated pytest suite with coverage.



Frontend CI is configured through:



```text

.github/workflows/frontend-ci.yml

```



The frontend workflow installs dependencies using the committed lock files and runs:



\* ESLint

\* Production build



for both:



```text

admin-web

student-mobile

```



\---



\# 18. Local Development



\### Start the backend



From the backend directory with the virtual environment activated:



```cmd

python run.py

```



The development API is normally available at:



```text

http://127.0.0.1:5000

```



\### Start the admin frontend



From `admin-web`:



```cmd

npm run dev

```



The Vite development server uses the configured local development port.



\### Start the student frontend



From `student-mobile`:



```cmd

npm run dev

```



The student application uses the configured Vite development port.



\---



\# 19. API Development Principles



Future API changes should follow these principles:



1\. Preserve existing verified endpoints unless a requirement requires a change.

2\. Preserve existing database relationships.

3\. Maintain JWT authentication for protected operations.

4\. Maintain role-based authorization.

5\. Validate user input on the backend.

6\. Return appropriate HTTP status codes.

7\. Add automated tests for new behavior.

8\. Update this API document when endpoints or contracts change.

9\. Do not commit environment secrets.

10\. Run the backend test suite before committing backend changes.



\---



\# 20. Current API Quality Status



The API has been implemented and tested as part of the CampusReserve project.



The current backend automated test suite contains 108 passing tests with 99% overall application coverage.



The backend and frontend projects also have GitHub Actions CI workflows.



This documentation describes the currently implemented API contract and should be updated whenever the API implementation changes.



\---



\# 21. Conclusion



The CampusReserve API provides the backend services required for student authentication, resource discovery and management, reservations, check-in, and administrator operations.



The API is designed to support the CampusReserve student and administrator applications while enforcing authentication, authorization, validation, ownership, and reservation business rules.



