\# UML Class Diagram — CampusReserve



\## 1. Purpose



The UML Class Diagram describes the main domain classes implemented in the CampusReserve backend and the relationships between them.



The diagram represents the persistent entities used by the reservation system:



\* `User`

\* `Resource`

\* `Reservation`

\* `CheckIn`



The model corresponds to the database structure and the implemented Flask-SQLAlchemy models.



\---



\## 2. System Domain Classes



\### 2.1 User



\*\*Class:\*\* `User`



Represents a registered CampusReserve user, either a student or system administrator.



\*\*Attributes:\*\*



\* `id: Integer`

\* `name: String`

\* `student\_id: String`

\* `email: String`

\* `password\_hash: String`

\* `role: String`

\* `created\_at: DateTime`



\*\*Responsibilities:\*\*



\* Store user identity information.

\* Store authentication information through a password hash.

\* Identify whether the user is a `STUDENT` or `ADMIN`.

\* Own reservations created by the user.



\---



\### 2.2 Resource



\*\*Class:\*\* `Resource`



Represents a reservable campus facility or piece of equipment.



\*\*Attributes:\*\*



\* `id: Integer`

\* `name: String`

\* `type: String`

\* `description: Text`

\* `location: String`

\* `capacity: Integer`

\* `status: String`

\* `created\_at: DateTime`



\*\*Resource Types:\*\*



\* `LABORATORY`

\* `STUDY\_ROOM`

\* `EQUIPMENT`



\*\*Resource Statuses:\*\*



\* `AVAILABLE`

\* `UNAVAILABLE`



\*\*Responsibilities:\*\*



\* Store information about reservable campus resources.

\* Indicate the type and location of a resource.

\* Store capacity information.

\* Indicate whether the resource is currently available for reservation.



\---



\### 2.3 Reservation



\*\*Class:\*\* `Reservation`



Represents a booking made by a user for a resource.



\*\*Attributes:\*\*



\* `id: Integer`

\* `user\_id: Integer`

\* `resource\_id: Integer`

\* `reservation\_date: Date`

\* `start\_time: Time`

\* `end\_time: Time`

\* `purpose: String`

\* `status: String`

\* `created\_at: DateTime`



\*\*Reservation Statuses:\*\*



\* `PENDING`

\* `CONFIRMED`

\* `CANCELLED`

\* `COMPLETED`



\*\*Responsibilities:\*\*



\* Record which user made a reservation.

\* Record which resource was reserved.

\* Store reservation date and time.

\* Store the purpose of the reservation.

\* Track the reservation lifecycle.



\---



\### 2.4 CheckIn



\*\*Class:\*\* `CheckIn`



Represents the check-in record associated with a reservation.



\*\*Attributes:\*\*



\* `id: Integer`

\* `reservation\_id: Integer`

\* `qr\_token: String`

\* `checked\_in\_at: DateTime`

\* `status: String`



\*\*Check-In Statuses:\*\*



\* `NOT\_CHECKED\_IN`

\* `CHECKED\_IN`



\*\*Responsibilities:\*\*



\* Associate a check-in record with a reservation.

\* Store the QR token used for check-in.

\* Record when the user checks in.

\* Track whether the reservation has been checked into.



\---



\## 3. Relationships



\### User — Reservation



A `User` can create many `Reservation` records.



Each `Reservation` belongs to exactly one `User`.



\*\*Cardinality:\*\*



`User 1 ───────── 0..\* Reservation`



Database relationship:



`reservations.user\_id → users.id`



\---



\### Resource — Reservation



A `Resource` can have many `Reservation` records over time.



Each `Reservation` is associated with exactly one `Resource`.



\*\*Cardinality:\*\*



`Resource 1 ───────── 0..\* Reservation`



Database relationship:



`reservations.resource\_id → resources.id`



\---



\### Reservation — CheckIn



A `Reservation` can have zero or one associated `CheckIn`.



Each `CheckIn` belongs to exactly one `Reservation`.



\*\*Cardinality:\*\*



`Reservation 1 ───────── 0..1 CheckIn`



Database relationship:



`check\_ins.reservation\_id → reservations.id`



The `reservation\_id` field in `check\_ins` is unique, enforcing the one-check-in-record-per-reservation relationship.



\---



\## 4. Overall Class Relationship



```text

┌──────────────────────────┐

│          User            │

├──────────────────────────┤

│ id                       │

│ name                     │

│ student\_id               │

│ email                    │

│ password\_hash            │

│ role                     │

│ created\_at               │

└────────────┬─────────────┘

&#x20;            │

&#x20;            │ 1

&#x20;            │

&#x20;            │ 0..\*

&#x20;            ▼

┌──────────────────────────┐

│       Reservation        │

├──────────────────────────┤

│ id                       │

│ user\_id                  │

│ resource\_id              │

│ reservation\_date         │

│ start\_time               │

│ end\_time                 │

│ purpose                  │

│ status                   │

│ created\_at               │

└───────┬──────────────┬───┘

&#x20;       │              │

&#x20;       │              │ 1

&#x20;       │              │

&#x20;       │              │ 0..1

&#x20;       │              ▼

&#x20;       │     ┌──────────────────────┐

&#x20;       │     │       CheckIn        │

&#x20;       │     ├──────────────────────┤

&#x20;       │     │ id                   │

&#x20;       │     │ reservation\_id       │

&#x20;       │     │ qr\_token             │

&#x20;       │     │ checked\_in\_at        │

&#x20;       │     │ status               │

&#x20;       │     └──────────────────────┘

&#x20;       │

&#x20;       │ 0..\*

&#x20;       │

&#x20;       │

&#x20;       ▼

┌──────────────────────────┐

│        Resource          │

├──────────────────────────┤

│ id                       │

│ name                     │

│ type                     │

│ description              │

│ location                 │

│ capacity                 │

│ status                   │

│ created\_at               │

└──────────────────────────┘

```



\---



\## 5. Association Summary



| Source Class | Relationship        | Target Class | Cardinality |

| ------------ | ------------------- | ------------ | ----------- |

| User         | creates             | Reservation  | 1 : 0..\*    |

| Resource     | is reserved through | Reservation  | 1 : 0..\*    |

| Reservation  | has                 | CheckIn      | 1 : 0..1    |



\---



\## 6. Important Constraints



\### User Constraints



\* `email` is unique.

\* `student\_id` is unique when supplied.

\* Passwords are stored as password hashes rather than plaintext passwords.

\* `role` identifies `STUDENT` or `ADMIN`.



\### Resource Constraints



\* `type` is restricted to the implemented resource types.

\* `status` is restricted to `AVAILABLE` or `UNAVAILABLE`.

\* `capacity` stores the resource capacity.



\### Reservation Constraints



\* Every reservation must reference an existing user.

\* Every reservation must reference an existing resource.

\* A reservation contains a date, start time, and end time.

\* Reservation status represents its current lifecycle state.



\### Check-In Constraints



\* Every check-in references an existing reservation.

\* `reservation\_id` is unique.

\* `qr\_token` is unique.

\* A check-in can transition from `NOT\_CHECKED\_IN` to `CHECKED\_IN`.



\---



\## 7. UML Diagram Recommendation



The visual UML Class Diagram should be created in draw.io or another UML-compatible diagramming tool.



Recommended layout:



```text

&#x20;                 ┌──────────────┐

&#x20;                 │     User     │

&#x20;                 └──────┬───────┘

&#x20;                        │

&#x20;                      1 │

&#x20;                        │ 0..\*

&#x20;                        ▼

&#x20;                 ┌──────────────┐

&#x20;                 │ Reservation  │

&#x20;                 └──────┬───────┘

&#x20;                        │

&#x20;             ┌──────────┴──────────┐

&#x20;             │                     │

&#x20;           1 │                     │ 0..1

&#x20;             ▼                     ▼

&#x20;      ┌──────────────┐      ┌──────────────┐

&#x20;      │   Resource   │      │   CheckIn    │

&#x20;      └──────────────┘      └──────────────┘

```



Each class box should contain:



1\. Class name

2\. Attributes

3\. Data types where appropriate

4\. Key relationships

5\. Multiplicity indicators



The visual diagram should remain consistent with the implemented database and backend models.



\---



\## 8. Implementation Traceability



| UML Class   | Database Table | Backend Model               |

| ----------- | -------------- | --------------------------- |

| User        | `users`        | `app/models/user.py`        |

| Resource    | `resources`    | `app/models/resource.py`    |

| Reservation | `reservations` | `app/models/reservation.py` |

| CheckIn     | `check\_ins`    | `app/models/check\_in.py`    |



This provides traceability between the requirements/design models, database implementation, and application code.



\---



\## 9. IBL 3300 Alignment



The Class Diagram supports the Software Engineering Studio requirements by documenting:



\* Object-oriented domain modelling.

\* Classes and their responsibilities.

\* Associations between domain objects.

\* Relationship cardinalities.

\* Database-to-object traceability.

\* The structural design of the reservation and check-in system.



The model also supports later sequence and activity diagrams because the four domain classes represent the primary objects involved in the system's core workflows.



