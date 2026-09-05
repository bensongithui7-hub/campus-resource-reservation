\# CampusReserve User Manual



\## Campus Smart Facility \& Lab Equipment Reservation System



\*\*Project:\*\* CampusReserve

\*\*Course:\*\* IBL 3300 Software Engineering Studio

\*\*Institution:\*\* Technical University of Kenya

\*\*Version:\*\* 1.0



\---



\# Table of Contents



1\. Introduction

2\. System Access

3\. Student User Guide

4\. Administrator User Guide

5\. Reservation Workflow

6\. Check-In Workflow

7\. Common Errors and Solutions

8\. Security and Account Guidelines

9\. System Requirements

10\. Support and Maintenance



\---



\# 1. Introduction



\## 1.1 Purpose



CampusReserve is a web-based campus resource reservation system designed to allow students to view available campus facilities and equipment, make reservations, manage their reservations, and complete reservation check-ins.



The system also provides administrators with tools for managing resources, reservations, users, and check-in records.



\## 1.2 Main User Roles



CampusReserve has two primary user roles:



\### Student



Students can:



\* Register for an account.

\* Log into the system.

\* View available resources.

\* View resource details.

\* Create reservations.

\* View their reservation history.

\* Cancel eligible reservations.

\* Access check-in information for their reservations.

\* Complete reservation check-in.



\### Administrator



Administrators can:



\* Log into the administrator portal.

\* View system statistics and activity.

\* View and manage reservations.

\* Manage campus resources.

\* Monitor check-in records.

\* View registered users.

\* Update reservation statuses.

\* Update resource availability/status.



\---



\# 2. System Access



CampusReserve consists of two frontend applications supported by a Flask backend API.



\## 2.1 Student Application



The student application provides the student-facing reservation interface.



During local development, it is served through the Vite development server on:



`http://localhost:5174`



The backend API is served on:



`http://127.0.0.1:5000/api`



\## 2.2 Administrator Application



The administrator application provides the administrative interface.



During local development, it is served through the Vite development server on:



`http://localhost:5173`



The administrator application communicates with the same backend API.



\## 2.3 Backend



The Flask backend provides authentication, resource management, reservation processing, check-in functionality, and administrative operations.



Local backend address:



`http://127.0.0.1:5000`



API prefix:



`/api`



\---



\# 3. Student User Guide



\## 3.1 Registering an Account



A new student can create an account through the student application.



\### Steps



1\. Open the CampusReserve student application.

2\. Select the registration option.

3\. Enter the required information:



&#x20;  \* Name

&#x20;  \* Student ID

&#x20;  \* Email address

&#x20;  \* Password

4\. Submit the registration form.

5\. If the information is valid and the email/student ID is not already registered, the account is created.

6\. Log in using the newly created account.



\### Registration Requirements



The system validates required registration information and prevents duplicate email addresses and duplicate student IDs.



\---



\# 3.2 Logging In



\### Steps



1\. Open the student application.

2\. Enter the registered email address.

3\. Enter the account password.

4\. Submit the login form.

5\. On successful authentication, the student is taken to the application dashboard.



The application maintains the authenticated session using a JWT access token stored in browser local storage.



\---



\# 3.3 Student Dashboard



After logging in, the student can access the main application functions.



Typical functions include:



\* Viewing available resources.

\* Creating reservations.

\* Viewing existing reservations.

\* Cancelling eligible reservations.

\* Accessing check-in information.



The dashboard provides the main navigation point for student activities.



\---



\# 3.4 Viewing Resources



Students can browse campus facilities and equipment available for reservation.



Resources are categorized as:



\* Laboratory

\* Study Room

\* Equipment



Each resource may provide information such as:



\* Resource name

\* Resource type

\* Description

\* Location

\* Capacity

\* Availability status



\### Steps



1\. Log into the student application.

2\. Open the resources section.

3\. Browse the available resources.

4\. Select a resource to view its details.



Only resources that are available for reservation should be selected when creating a new reservation.



\---



\# 3.5 Creating a Reservation



Students can create reservations for available resources.



\### Steps



1\. Log into CampusReserve.

2\. Open the resource list.

3\. Select the desired resource.

4\. Choose the reservation date.

5\. Enter a start time.

6\. Enter an end time.

7\. Enter the purpose of the reservation where applicable.

8\. Submit the reservation.

9\. Review the result displayed by the system.



The backend validates the reservation information before creating the reservation.



\### Reservation Validation



The system checks that:



\* The student is authenticated.

\* The requested resource exists.

\* The resource is available.

\* Required reservation information is supplied.

\* The reservation date and time are valid.

\* The start time occurs before the end time.

\* The request follows the application's reservation rules.



\---



\# 3.6 Viewing My Reservations



Students can view reservations associated with their account.



\### Steps



1\. Log into CampusReserve.

2\. Open the reservations or "My Reservations" section.

3\. Review the displayed reservations.



Reservation information can include:



\* Reservation ID

\* Resource

\* Date

\* Start time

\* End time

\* Purpose

\* Status



Reservation statuses include:



\* `PENDING`

\* `CONFIRMED`

\* `CANCELLED`

\* `COMPLETED`



\---



\# 3.7 Cancelling a Reservation



Students can cancel eligible reservations belonging to their account.



\### Steps



1\. Open "My Reservations".

2\. Locate the reservation to be cancelled.

3\. Select the cancellation option.

4\. Confirm the action if prompted.

5\. The reservation status is updated to `CANCELLED`.



A student cannot cancel another student's reservation.



Reservations that are already cancelled cannot be cancelled again.



\---



\# 3.8 Checking In



CampusReserve supports reservation check-in.



A check-in record is associated with a specific reservation.



\### Student Check-In Process



1\. Log into the student application.

2\. Open the relevant confirmed reservation.

3\. Access the check-in information.

4\. Use the available QR/check-in token mechanism.

5\. Submit the check-in request.

6\. The system validates the reservation and check-in request.

7\. A successful check-in changes the check-in status to `CHECKED\_IN`.



A reservation can only have one check-in record.



Duplicate check-in attempts are rejected by the system.



\---



\# 3.9 Check-In Status



A check-in can have one of the following statuses:



\* `NOT\_CHECKED\_IN`

\* `CHECKED\_IN`



The system records the time at which a successful check-in occurs.



\---



\# 4. Administrator User Guide



\## 4.1 Administrator Login



Administrators use the administrator application.



\### Steps



1\. Open the CampusReserve administrator application.

2\. Enter administrator credentials.

3\. Submit the login form.

4\. The system authenticates the administrator.

5\. On successful authentication, the administrator dashboard is displayed.



Administrative API operations require an authenticated administrator account.



\---



\# 4.2 Administrator Dashboard



The administrator dashboard provides an overview of system activity.



The interface contains navigation areas including:



\* Dashboard

\* Reservations

\* Resources

\* Check-ins

\* Users



The dashboard is intended to give administrators a central point from which system operations can be managed.



\---



\# 4.3 Managing Resources



Administrators can manage campus resources.



Resources contain information such as:



\* Name

\* Type

\* Description

\* Location

\* Capacity

\* Status



Supported resource types are:



\* `LABORATORY`

\* `STUDY\_ROOM`

\* `EQUIPMENT`



Supported resource statuses are:



\* `AVAILABLE`

\* `UNAVAILABLE`



\## Updating a Resource



\### Steps



1\. Open the Resources section.

2\. Locate the resource.

3\. Select the resource management/edit option.

4\. Update the required information.

5\. Save the changes.

6\. Confirm that the updated resource information is displayed.



\## Changing Resource Availability



An administrator can change the status of a resource between:



\* `AVAILABLE`

\* `UNAVAILABLE`



An unavailable resource should not be used for new reservations.



\## Deleting a Resource



Where permitted by the administrator interface, an administrator can delete a resource.



The system returns an appropriate error when an administrator attempts to operate on a resource that does not exist.



\---



\# 4.4 Managing Reservations



Administrators can view reservations across the system.



\### Steps



1\. Open the Reservations section.

2\. Review the reservation records.

3\. Select a reservation to view its details.

4\. Where necessary, update its status.



Reservation statuses are:



\* `PENDING`

\* `CONFIRMED`

\* `CANCELLED`

\* `COMPLETED`



Administrative reservation management allows the institution to monitor and control reservation activity.



\---



\# 4.5 Updating Reservation Status



Administrators can update the status of reservations.



\### Steps



1\. Open the Reservations section.

2\. Locate the required reservation.

3\. Select the status management option.

4\. Select the appropriate status.

5\. Save the change.



The backend validates the supplied status and rejects invalid status values.



\---



\# 4.6 Monitoring Check-Ins



Administrators can view check-in records.



The check-in management area allows administrators to monitor whether reservations have been checked into.



A check-in record contains information associated with:



\* Reservation

\* QR/check-in token

\* Check-in timestamp

\* Check-in status



The administrator can use this information to monitor resource usage and attendance.



\---



\# 4.7 Viewing Users



Administrators can access the user management area.



The users section provides information about registered system users.



Users have one of two roles:



\* `STUDENT`

\* `ADMIN`



Administrative access is protected and student accounts cannot perform administrator-only operations.



\---



\# 5. Reservation Workflow



The normal reservation lifecycle is:



```text

Student Login

&#x20;    |

&#x20;    v

Browse Resources

&#x20;    |

&#x20;    v

Select Available Resource

&#x20;    |

&#x20;    v

Choose Date and Time

&#x20;    |

&#x20;    v

Submit Reservation

&#x20;    |

&#x20;    v

Reservation Created

&#x20;    |

&#x20;    v

Reservation Confirmed

&#x20;    |

&#x20;    v

Check In

&#x20;    |

&#x20;    v

Reservation Completed

```



A reservation may instead be cancelled:



```text

Reservation

&#x20;    |

&#x20;    v

Cancel Reservation

&#x20;    |

&#x20;    v

CANCELLED

```



Administrators can also manage reservation statuses where required.



\---



\# 6. Check-In Workflow



The check-in workflow is:



```text

Confirmed Reservation

&#x20;       |

&#x20;       v

Access Check-In

&#x20;       |

&#x20;       v

Submit QR/Check-In Token

&#x20;       |

&#x20;       v

Validate Reservation

&#x20;       |

&#x20;       +---- Invalid/Unauthorized ----> Reject Request

&#x20;       |

&#x20;       v

Create/Update Check-In

&#x20;       |

&#x20;       v

CHECKED\_IN

```



The system prevents duplicate check-ins for the same reservation.



\---



\# 7. Common Errors and Solutions



\## 7.1 Invalid Login Credentials



\*\*Problem:\*\* Login fails.



\*\*Possible causes:\*\*



\* Incorrect email.

\* Incorrect password.

\* Account does not exist.



\*\*Solution:\*\* Confirm the account credentials and register an account if necessary.



\---



\## 7.2 Duplicate Registration



\*\*Problem:\*\* Registration is rejected because information is already in use.



\*\*Possible causes:\*\*



\* Email address is already registered.

\* Student ID is already registered.



\*\*Solution:\*\* Use the existing account or provide unique registration information.



\---



\## 7.3 Resource Not Found



\*\*Problem:\*\* A requested resource cannot be found.



\*\*Solution:\*\* Return to the resource list and select an existing resource.



\---



\## 7.4 Resource Unavailable



\*\*Problem:\*\* A reservation cannot be created for a resource.



\*\*Possible cause:\*\* The resource is currently marked `UNAVAILABLE`.



\*\*Solution:\*\* Select another available resource or wait until the resource becomes available.



\---



\## 7.5 Invalid Reservation Time



\*\*Problem:\*\* Reservation creation fails because of the selected times.



\*\*Possible causes:\*\*



\* Missing time information.

\* Invalid date/time format.

\* Start time is equal to or later than the end time.



\*\*Solution:\*\* Enter a valid reservation date and ensure the start time occurs before the end time.



\---



\## 7.6 Unauthorized Operation



\*\*Problem:\*\* The system rejects an operation because the user is not authorized.



\*\*Possible causes:\*\*



\* The user is not logged in.

\* The user does not own the requested reservation.

\* A student is attempting an administrator-only operation.



\*\*Solution:\*\* Log in using the correct account and perform only operations permitted for that account role.



\---



\## 7.7 Duplicate Check-In



\*\*Problem:\*\* A check-in attempt is rejected because the reservation has already been checked into.



\*\*Solution:\*\* No further check-in is required for that reservation.



\---



\# 8. Security and Account Guidelines



Users should follow normal account security practices.



\## 8.1 Password Protection



Users should:



\* Keep passwords private.

\* Avoid sharing account credentials.

\* Avoid storing passwords in publicly accessible documents.

\* Use strong passwords.



Passwords are stored by the backend as password hashes rather than plain-text passwords.



\## 8.2 Authentication



Protected API operations require JWT authentication.



The frontend stores the authenticated student session information in browser local storage.



\## 8.3 Role-Based Access



CampusReserve distinguishes between students and administrators.



Administrator operations are protected from ordinary student accounts.



\## 8.4 Secrets



Application secrets such as:



\* Database credentials

\* Flask secret keys

\* JWT secret keys



must not be committed to the public source repository.



Environment configuration should be supplied through environment variables or an appropriate deployment configuration.



\---



\# 9. System Requirements



\## 9.1 Student/Administrator Browser



A modern web browser is required.



Recommended browsers include current versions of:



\* Google Chrome

\* Microsoft Edge

\* Mozilla Firefox



\## 9.2 Development Environment



For local development, the project uses:



\* Python 3.14.2

\* Flask 3.1.3

\* MySQL Community Server 8.0.46

\* Node.js 24.20.0

\* npm 11.19.0

\* React

\* Vite 8.2.2



\## 9.3 Database



CampusReserve uses MySQL for its persistent production/development database.



The database is named:



`campus\_reservation`



The database contains:



\* `users`

\* `resources`

\* `reservations`

\* `check\_ins`



\---



\# 10. Support and Maintenance



\## 10.1 Starting the Backend Locally



From the project backend directory:



```cmd

cd backend

venv\\Scripts\\activate

python run.py

```



The backend should become available at:



`http://127.0.0.1:5000`



\## 10.2 Starting the Student Application



From the student frontend directory:



```cmd

cd student-mobile

npm install

npm run dev

```



The Vite development server normally provides the student application on port `5174`.



\## 10.3 Starting the Administrator Application



From the administrator frontend directory:



```cmd

cd admin-web

npm install

npm run dev

```



The Vite development server normally provides the administrator application on port `5173`.



\## 10.4 Running Backend Tests



From the backend directory:



```cmd

cd backend

venv\\Scripts\\activate

python -m pytest --cov=app --cov-report=term-missing -q

```



The automated backend test suite covers authentication, resources, reservations, check-ins, administration, protected routes, and application setup.



\## 10.5 Frontend Quality Checks



From `admin-web`:



```cmd

npm run lint

npm run build

```



From `student-mobile`:



```cmd

npm run lint

npm run build

```



These checks are also executed by the project's GitHub Actions frontend CI workflow.



\## 10.6 Continuous Integration



The repository contains GitHub Actions workflows for:



\* Backend testing and coverage.

\* Student frontend linting and building.

\* Administrator frontend linting and building.



The workflows run automatically for pushes and pull requests.



\---



\# 11. Application API Reference



The frontend applications communicate with the backend through the REST API.



The main API groups are:



\### Authentication



```text

POST /api/auth/register

POST /api/auth/login

```



\### Health



```text

GET /api/health

```



\### Resources



```text

GET /api/resources

GET /api/resources/<id>

POST /api/resources

```



\### Reservations



```text

POST /api/reservations

GET /api/reservations

GET /api/reservations/<id>

DELETE /api/reservations/<id>

```



\### Check-In



```text

POST /api/reservations/<reservation\_id>/check-in

GET /api/reservations/<reservation\_id>/check-in

POST /api/check-in/<qr\_token>

```



\### Administration



```text

GET /api/admin/reservations

GET /api/admin/check-ins

GET /api/admin/users

PUT /api/admin/resources/<id>

DELETE /api/admin/resources/<id>

PUT /api/admin/resources/<id>/status

PUT /api/admin/reservations/<id>/status

```



Detailed request and response information is provided in `documentation/API.md`.



\---



\# 12. Related Project Documentation



The following documents provide additional project information:



\* `SRS.md` — Software Requirements Specification

\* `API.md` — API documentation

\* `ARCHITECTURE.md` — System architecture

\* `DATABASE.md` — Database design and ERD documentation

\* `USER\_MANUAL.md` — This user manual



These documents are maintained as part of the project documentation set.



\---



\# 13. Conclusion



CampusReserve provides a centralized platform for managing campus facility and equipment reservations.



Students can use the system to discover resources, create and manage reservations, and complete check-ins.



Administrators can monitor system activity and manage resources, reservations, users, and check-in records.



The system combines a React/Vite frontend, Flask REST API, JWT-based authentication, and MySQL database to provide the required reservation functionality.



