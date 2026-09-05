\# CampusReserve UML Use-Case Model



\## Campus Smart Facility \& Lab Equipment Reservation System



\*\*Project:\*\* CampusReserve

\*\*Course:\*\* IBL 3300 Software Engineering Studio

\*\*UML Deliverable:\*\* Use-Case Model

\*\*Version:\*\* 1.0



\---



\# 1. Purpose



This document defines the UML use-case model for CampusReserve.



The use-case model identifies the system's primary actors, their interactions with the system, and the major functional capabilities implemented by the CampusReserve application.



The model is derived from:



\* The approved project proposal.

\* The Software Requirements Specification.

\* The implemented Flask REST API.

\* The implemented student frontend.

\* The implemented administrator frontend.



\---



\# 2. System Boundary



The system boundary is the \*\*CampusReserve System\*\*.



The system consists of:



\* Student web/mobile-responsive interface.

\* Administrator web interface.

\* Flask REST API.

\* MySQL persistence layer.

\* Authentication and authorization services.

\* Reservation management.

\* Resource management.

\* Check-in functionality.



External actors interact with CampusReserve through the appropriate frontend or API interface.



\---



\# 3. Primary Actors



\## 3.1 Student



The Student is the primary end user of CampusReserve.



The Student can:



\* Register an account.

\* Log in.

\* View available resources.

\* View resource details.

\* Create reservations.

\* View personal reservations.

\* View reservation details.

\* Cancel eligible reservations.

\* Access reservation check-in information.

\* Complete reservation check-in.



\---



\## 3.2 Administrator



The Administrator manages the CampusReserve system.



The Administrator can:



\* Log in.

\* View system reservations.

\* Manage resources.

\* Update resource availability.

\* Delete resources.

\* Update reservation status.

\* View check-in records.

\* View registered users.



Administrator operations are protected by role-based authorization.



\---



\# 4. Supporting System Services



The following are internal system services rather than primary human actors:



\### Authentication Service



Responsible for:



\* User authentication.

\* JWT generation.

\* Protected-request authentication.



\### Database



Responsible for persistent storage of:



\* Users.

\* Resources.

\* Reservations.

\* Check-ins.



These are represented as system components in architectural diagrams rather than human actors in the use-case model.



\---



\# 5. Student Use Cases



\## UC-01 — Register Account



\*\*Primary Actor:\*\* Student



\*\*Goal:\*\* Create a CampusReserve account.



\### Main Flow



1\. Student opens the registration interface.

2\. Student enters name.

3\. Student enters student ID.

4\. Student enters email.

5\. Student enters password.

6\. Student submits registration.

7\. System validates required information.

8\. System checks for duplicate email/student ID.

9\. System creates the student account.

10\. System returns a successful registration response.



\### Alternative Flows



\* Required information is missing.

\* Email already exists.

\* Student ID already exists.



\---



\## UC-02 — Log In



\*\*Primary Actor:\*\* Student or Administrator



\*\*Goal:\*\* Authenticate to CampusReserve.



\### Main Flow



1\. User enters email and password.

2\. System validates the credentials.

3\. System authenticates the user.

4\. System generates an authentication token.

5\. User accesses protected functionality.



\### Alternative Flows



\* Invalid credentials.

\* Missing login information.

\* User does not have permission for the requested operation.



\---



\## UC-03 — View Resources



\*\*Primary Actor:\*\* Student



\*\*Goal:\*\* Discover campus facilities and equipment.



\### Main Flow



1\. Student opens the resource section.

2\. System retrieves available resources.

3\. System displays resource information.

4\. Student reviews available resources.



Resource information may include:



\* Name.

\* Type.

\* Description.

\* Location.

\* Capacity.

\* Status.



\---



\## UC-04 — View Resource Details



\*\*Primary Actor:\*\* Student



\*\*Goal:\*\* Inspect a specific campus resource before making a reservation.



\### Main Flow



1\. Student selects a resource.

2\. System retrieves the resource.

3\. System displays its details.



\### Alternative Flow



If the resource does not exist, the system returns an appropriate not-found response.



\---



\## UC-05 — Create Reservation



\*\*Primary Actor:\*\* Student



\*\*Goal:\*\* Reserve an available campus facility or equipment item.



\### Main Flow



1\. Student selects an available resource.

2\. Student provides reservation date.

3\. Student provides start time.

4\. Student provides end time.

5\. Student provides reservation purpose where applicable.

6\. System validates the request.

7\. System confirms that the resource exists.

8\. System confirms that the resource is available.

9\. System validates the date and time.

10\. System creates the reservation.

11\. System returns the created reservation.



\### Alternative Flows



\* User is not authenticated.

\* Resource does not exist.

\* Resource is unavailable.

\* Required information is missing.

\* Invalid date.

\* Invalid time.

\* Start time is not before end time.



\---



\## UC-06 — View My Reservations



\*\*Primary Actor:\*\* Student



\*\*Goal:\*\* View reservations belonging to the authenticated student.



\### Main Flow



1\. Student opens the reservations section.

2\. System authenticates the request.

3\. System retrieves reservations belonging to the student.

4\. System displays the reservation records.



The student does not receive another student's reservations through the normal authenticated reservation listing.



\---



\## UC-07 — View Reservation Details



\*\*Primary Actor:\*\* Student



\*\*Goal:\*\* View details of a specific reservation.



\### Main Flow



1\. Student selects a reservation.

2\. System authenticates the request.

3\. System retrieves the reservation.

4\. System verifies that the student is authorized to access it.

5\. System returns the reservation details.



\### Alternative Flows



\* Reservation does not exist.

\* Reservation belongs to another user.



\---



\## UC-08 — Cancel Reservation



\*\*Primary Actor:\*\* Student



\*\*Goal:\*\* Cancel an eligible reservation.



\### Main Flow



1\. Student selects one of their reservations.

2\. Student requests cancellation.

3\. System authenticates the student.

4\. System verifies reservation ownership.

5\. System checks that the reservation exists.

6\. System updates the reservation status to `CANCELLED`.

7\. System returns the updated result.



\### Alternative Flows



\* Reservation does not exist.

\* Reservation belongs to another student.

\* Reservation is already cancelled.



\---



\## UC-09 — Access Check-In



\*\*Primary Actor:\*\* Student



\*\*Goal:\*\* Obtain check-in information for a reservation.



\### Main Flow



1\. Student selects the relevant reservation.

2\. System authenticates the student.

3\. System verifies reservation ownership.

4\. System retrieves the associated check-in information.

5\. System displays the check-in information.



\---



\## UC-10 — Complete Check-In



\*\*Primary Actor:\*\* Student



\*\*Goal:\*\* Check into a reservation using the supported QR/check-in mechanism.



\### Main Flow



1\. Student accesses the reservation check-in facility.

2\. Student submits the QR/check-in token.

3\. System validates the token.

4\. System identifies the associated reservation.

5\. System validates the reservation and check-in conditions.

6\. System records the check-in.

7\. System sets the check-in status to `CHECKED\_IN`.

8\. System records the check-in timestamp.

9\. System returns a successful check-in response.



\### Alternative Flows



\* QR/check-in token is invalid.

\* Reservation cannot be found.

\* Reservation is not eligible for check-in.

\* User is not authorized.

\* Reservation has already been checked in.



\---



\# 6. Administrator Use Cases



\## UC-11 — View All Reservations



\*\*Primary Actor:\*\* Administrator



\*\*Goal:\*\* Monitor reservations across the system.



\### Main Flow



1\. Administrator logs in.

2\. Administrator opens the reservations section.

3\. System verifies administrator authorization.

4\. System retrieves reservation records.

5\. System displays the records.



\---



\## UC-12 — Manage Resources



\*\*Primary Actor:\*\* Administrator



\*\*Goal:\*\* Maintain campus resources.



Administrator resource management includes:



\* Creating resources.

\* Updating resource information.

\* Updating resource status.

\* Deleting resources.



Resource information includes:



\* Name.

\* Type.

\* Description.

\* Location.

\* Capacity.

\* Status.



\---



\## UC-13 — Update Resource



\*\*Primary Actor:\*\* Administrator



\*\*Goal:\*\* Modify an existing resource.



\### Main Flow



1\. Administrator selects a resource.

2\. Administrator provides updated information.

3\. System verifies administrator authorization.

4\. System validates the supplied information.

5\. System updates the resource.

6\. System returns the updated resource.



\### Alternative Flows



\* Resource does not exist.

\* Request body is missing.

\* Resource type is invalid.

\* Capacity is invalid.

\* Resource status is invalid.



\---



\## UC-14 — Update Resource Availability



\*\*Primary Actor:\*\* Administrator



\*\*Goal:\*\* Control whether a resource can be reserved.



\### Main Flow



1\. Administrator selects a resource.

2\. Administrator selects the desired status.

3\. System validates the administrator's authorization.

4\. System validates the status.

5\. System updates the resource status.



Supported statuses are:



\* `AVAILABLE`

\* `UNAVAILABLE`



\---



\## UC-15 — Delete Resource



\*\*Primary Actor:\*\* Administrator



\*\*Goal:\*\* Remove a resource from the system.



\### Main Flow



1\. Administrator selects a resource.

2\. Administrator requests deletion.

3\. System verifies administrator authorization.

4\. System verifies that the resource exists.

5\. System deletes the resource.

6\. System returns the operation result.



\---



\## UC-16 — Manage Reservation Status



\*\*Primary Actor:\*\* Administrator



\*\*Goal:\*\* Update the status of a reservation.



\### Main Flow



1\. Administrator selects a reservation.

2\. Administrator selects a new status.

3\. System verifies administrator authorization.

4\. System validates the status.

5\. System updates the reservation.

6\. System returns the updated reservation.



Supported reservation statuses are:



\* `PENDING`

\* `CONFIRMED`

\* `CANCELLED`

\* `COMPLETED`



\---



\## UC-17 — View Check-In Records



\*\*Primary Actor:\*\* Administrator



\*\*Goal:\*\* Monitor reservation check-ins.



\### Main Flow



1\. Administrator opens the check-in section.

2\. System verifies administrator authorization.

3\. System retrieves check-in records.

4\. System displays the records.



Check-in information includes the associated reservation, token information, status, and check-in timestamp where available.



\---



\## UC-18 — View Users



\*\*Primary Actor:\*\* Administrator



\*\*Goal:\*\* View registered CampusReserve users.



\### Main Flow



1\. Administrator opens the users section.

2\. System verifies administrator authorization.

3\. System retrieves registered users.

4\. System displays the user records.



\---



\# 7. Use-Case Relationships



The major relationships are summarized below.



\### Authentication Dependency



Protected student and administrator use cases require authentication.



```text

Register Account

&#x20;      |

&#x20;      v

&#x20;   Log In

&#x20;      |

&#x20;      +--------------------+

&#x20;      |                    |

&#x20;      v                    v

Student Functions     Administrator Functions

```



\### Reservation Dependency



```text

View Resources

&#x20;     |

&#x20;     v

View Resource Details

&#x20;     |

&#x20;     v

Create Reservation

&#x20;     |

&#x20;     v

View My Reservations

&#x20;     |

&#x20;     +------------------> Cancel Reservation

&#x20;     |

&#x20;     v

Access Check-In

&#x20;     |

&#x20;     v

Complete Check-In

```



\### Administration Dependency



```text

Administrator Login

&#x20;      |

&#x20;      +----> View All Reservations

&#x20;      |

&#x20;      +----> Manage Resources

&#x20;      |          |

&#x20;      |          +----> Update Resource

&#x20;      |          +----> Update Availability

&#x20;      |          +----> Delete Resource

&#x20;      |

&#x20;      +----> Manage Reservation Status

&#x20;      |

&#x20;      +----> View Check-In Records

&#x20;      |

&#x20;      +----> View Users

```



\---



\# 8. Text Representation of the Use-Case Diagram



The following structure should be reproduced as a UML use-case diagram in draw.io.



```text

&#x20;                        +--------------------------------------+

&#x20;                        |          CAMPUSRESERVE SYSTEM       |

&#x20;                        |                                      |

Student ---------------->| (Register Account)                  |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (Log In)                             |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (View Resources)                    |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (View Resource Details)             |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (Create Reservation)                |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (View My Reservations)              |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (View Reservation Details)           |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (Cancel Reservation)                |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (Access Check-In)                   |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (Complete Check-In)                 |

&#x20;                        |                                      |

&#x20;                        |                                      |

Administrator ---------->| (Log In)                             |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (View All Reservations)              |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (Manage Resources)                  |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (Update Resource)                   |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (Update Resource Availability)      |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (Delete Resource)                   |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (Manage Reservation Status)          |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (View Check-In Records)             |

&#x20;  |                     |                                      |

&#x20;  +-------------------->| (View Users)                        |

&#x20;                        |                                      |

&#x20;                        +--------------------------------------+

```



\---



\# 9. Recommended Draw.io Layout



The final visual UML diagram should contain:



\### Left side



\*\*Student\*\* actor.



\### Right side



\*\*Administrator\*\* actor.



\### Centre



A large rectangle labelled:



\*\*CampusReserve System\*\*



Inside the boundary, place the use cases as UML ovals.



Group student functions toward the left/centre and administrator functions toward the right/centre.



Authentication should be placed near the upper-middle portion of the system boundary.



Reservation and check-in use cases should be grouped together in the middle/lower portion.



Administrative management functions should be grouped separately.



Use standard UML actor stick figures and use-case ellipses.



\---



\# 10. Proposal Alignment



The use-case model directly represents the functional outputs identified in the project proposal.



| Proposal Requirement | Use Case                                |

| -------------------- | --------------------------------------- |

| Successful login     | UC-02                                   |

| Student dashboard    | UC-02 and student application functions |

| Available resources  | UC-03                                   |

| Booking/reservation  | UC-05                                   |

| Booking confirmation | UC-05                                   |

| Booking history      | UC-06                                   |

| Booking cancellation | UC-08                                   |

| QR code/check-in     | UC-09 and UC-10                         |

| Admin dashboard      | Administrator authenticated functions   |

| Resource management  | UC-12                                   |

| Booking management   | UC-11 and UC-16                         |

| Availability updates | UC-14                                   |

| Check-in management  | UC-17                                   |

| User management      | UC-18                                   |



\---



\# 11. IBL 3300 Alignment



This deliverable addresses the UML requirements introduced in the IBL 3300 Software Engineering Studio implementation plan.



It supports:



\* Requirements analysis.

\* Requirements specification.

\* Use-case modeling.

\* Object-oriented analysis.

\* Traceability between requirements and implementation.

\* Preparation for class, sequence, activity, component, and deployment diagrams.



The use-case model will serve as the basis for the subsequent UML design artifacts.



\---



\# 12. Traceability Principle



Every major use case in this document should correspond to an implemented system capability or a directly supported system operation.



No additional business functionality should be introduced solely for diagram completeness.



The UML model therefore represents the current CampusReserve scope rather than an imagined future system.



