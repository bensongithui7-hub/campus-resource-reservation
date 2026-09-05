\# CampusReserve Database Design



\## 1. Overview



CampusReserve uses a relational MySQL database named `campus\_reservation`.



The database stores the core information required to operate the campus facility and lab equipment reservation system.



The database contains four primary tables:



1\. `users`

2\. `resources`

3\. `reservations`

4\. `check\_ins`



The relationships between these tables support user authentication, resource management, reservations, and reservation check-in.



\---



\## 2. Database Technology



The database technology is:



\* MySQL Community Server 8.0.46

\* Database name: `campus\_reservation`



The Flask backend communicates with the database through SQLAlchemy and PyMySQL.



The frontend applications do not connect directly to the database.



\---



\# 3. Entity Relationship Diagram



The logical relationship between the four entities is:



```text

+----------------------+

|        USERS         |

+----------------------+

| PK id                |

|    name              |

|    student\_id        |

|    email             |

|    password\_hash     |

|    role              |

|    created\_at        |

+----------+-----------+

&#x20;          |

&#x20;          | 1

&#x20;          |

&#x20;          | many

&#x20;          v

+----------------------+       +----------------------+

|    RESERVATIONS      |       |      RESOURCES       |

+----------------------+       +----------------------+

| PK id                |       | PK id                |

| FK user\_id           |       |    name              |

| FK resource\_id       |-------|    type              |

|    reservation\_date  | many  |    description       |

|    start\_time        |   1   |    location          |

|    end\_time          |       |    capacity          |

|    purpose           |       |    status            |

|    status            |       |    created\_at        |

|    created\_at        |       +----------------------+

+----------+-----------+

&#x20;          |

&#x20;          | 1

&#x20;          |

&#x20;          | 0..1

&#x20;          v

+----------------------+

|      CHECK\_INS       |

+----------------------+

| PK id                |

| FK reservation\_id    |

|    qr\_token          |

|    checked\_in\_at     |

|    status            |

+----------------------+

```



\---



\# 4. Users Table



Table name:



```text

users

```



The `users` table stores student and administrator accounts.



\## 4.1 Columns



| Column          | Type         | Constraints                 | Description            |

| --------------- | ------------ | --------------------------- | ---------------------- |

| `id`            | INT          | Primary Key, Auto Increment | Unique user identifier |

| `name`          | VARCHAR(100) | NOT NULL                    | User's name            |

| `student\_id`    | VARCHAR(50)  | UNIQUE                      | Student identifier     |

| `email`         | VARCHAR(120) | NOT NULL, UNIQUE            | User email address     |

| `password\_hash` | VARCHAR(255) | NOT NULL                    | Stored password hash   |

| `role`          | ENUM         | NOT NULL, Default `STUDENT` | User role              |

| `created\_at`    | TIMESTAMP    | Default current timestamp   | Account creation time  |



\## 4.2 Role Values



The `role` column supports:



```text

STUDENT

ADMIN

```



The default role for a newly created account is:



```text

STUDENT

```



\## 4.3 Constraints



The table enforces:



\* `id` as the primary key.

\* Unique student IDs.

\* Unique email addresses.

\* Non-null name.

\* Non-null email.

\* Non-null password hash.

\* A valid role value.



\---



\# 5. Resources Table



Table name:



```text

resources

```



The `resources` table stores campus facilities and equipment that can be reserved.



\## 5.1 Columns



| Column        | Type         | Constraints                   | Description                |

| ------------- | ------------ | ----------------------------- | -------------------------- |

| `id`          | INT          | Primary Key, Auto Increment   | Unique resource identifier |

| `name`        | VARCHAR(100) | NOT NULL                      | Resource name              |

| `type`        | ENUM         | NOT NULL                      | Resource category          |

| `description` | TEXT         | Optional                      | Resource description       |

| `location`    | VARCHAR(150) | NOT NULL                      | Physical location          |

| `capacity`    | INT          | Default `1`                   | Resource capacity          |

| `status`      | ENUM         | NOT NULL, Default `AVAILABLE` | Resource availability      |

| `created\_at`  | TIMESTAMP    | Default current timestamp     | Creation time              |



\## 5.2 Resource Types



The `type` column supports:



```text

LABORATORY

STUDY\_ROOM

EQUIPMENT

```



\## 5.3 Resource Status



The `status` column supports:



```text

AVAILABLE

UNAVAILABLE

```



The default status is:



```text

AVAILABLE

```



\---



\# 6. Reservations Table



Table name:



```text

reservations

```



The `reservations` table records bookings made by users against resources.



\## 6.1 Columns



| Column             | Type         | Constraints                 | Description                   |

| ------------------ | ------------ | --------------------------- | ----------------------------- |

| `id`               | INT          | Primary Key, Auto Increment | Unique reservation identifier |

| `user\_id`          | INT          | NOT NULL, Foreign Key       | User who made the reservation |

| `resource\_id`      | INT          | NOT NULL, Foreign Key       | Reserved resource             |

| `reservation\_date` | DATE         | NOT NULL                    | Reservation date              |

| `start\_time`       | TIME         | NOT NULL                    | Reservation start time        |

| `end\_time`         | TIME         | NOT NULL                    | Reservation end time          |

| `purpose`          | VARCHAR(255) | Optional                    | Reservation purpose           |

| `status`           | ENUM         | NOT NULL                    | Reservation state             |

| `created\_at`       | TIMESTAMP    | Default current timestamp   | Reservation creation time     |



\## 6.2 Reservation Status



The `status` column supports:



```text

PENDING

CONFIRMED

CANCELLED

COMPLETED

```



The database default is:



```text

CONFIRMED

```



\---



\# 7. Check-ins Table



Table name:



```text

check\_ins

```



The `check\_ins` table stores check-in information associated with reservations.



\## 7.1 Columns



| Column           | Type         | Constraints                   | Description                |

| ---------------- | ------------ | ----------------------------- | -------------------------- |

| `id`             | INT          | Primary Key, Auto Increment   | Unique check-in identifier |

| `reservation\_id` | INT          | NOT NULL, UNIQUE, Foreign Key | Associated reservation     |

| `qr\_token`       | VARCHAR(255) | NOT NULL, UNIQUE              | Check-in token             |

| `checked\_in\_at`  | TIMESTAMP    | Nullable                      | Check-in timestamp         |

| `status`         | ENUM         | NOT NULL                      | Check-in state             |



\## 7.2 Check-in Status



The `status` column supports:



```text

NOT\_CHECKED\_IN

CHECKED\_IN

```



The default status is:



```text

NOT\_CHECKED\_IN

```



\---



\# 8. Primary Keys



Each table has an auto-incrementing integer primary key.



```text

users.id

resources.id

reservations.id

check\_ins.id

```



Primary keys uniquely identify individual records.



\---



\# 9. Foreign Keys



The database defines three foreign-key relationships.



\## 9.1 User to Reservation



```text

reservations.user\_id

&#x20;       |

&#x20;       v

users.id

```



This identifies the user who created a reservation.



A user can have multiple reservations.



Relationship:



```text

USERS 1 ---- many RESERVATIONS

```



\---



\## 9.2 Resource to Reservation



```text

reservations.resource\_id

&#x20;       |

&#x20;       v

resources.id

```



This identifies the resource being reserved.



A resource can be associated with multiple reservations over time.



Relationship:



```text

RESOURCES 1 ---- many RESERVATIONS

```



\---



\## 9.3 Reservation to Check-in



```text

check\_ins.reservation\_id

&#x20;       |

&#x20;       v

reservations.id

```



This identifies the reservation associated with a check-in.



The `reservation\_id` column in `check\_ins` is also declared `UNIQUE`.



Therefore, the database structure allows at most one check-in record for each reservation.



Relationship:



```text

RESERVATIONS 1 ---- 0..1 CHECK\_INS

```



\---



\# 10. Referential Integrity



Foreign keys maintain relationships between related records.



The database defines:



```text

FOREIGN KEY (user\_id) REFERENCES users(id)

```



in the `reservations` table.



It also defines:



```text

FOREIGN KEY (resource\_id) REFERENCES resources(id)

```



in the `reservations` table.



The `check\_ins` table defines:



```text

FOREIGN KEY (reservation\_id) REFERENCES reservations(id)

```



These constraints help prevent orphaned related records.



\---



\# 11. Uniqueness Constraints



The database uses unique constraints to prevent duplicate values where uniqueness is required.



\## Users



```text

student\_id UNIQUE

email UNIQUE

```



\## Check-ins



```text

reservation\_id UNIQUE

qr\_token UNIQUE

```



These constraints support account integrity and duplicate check-in prevention.



\---



\# 12. Enumerated Values



The database uses MySQL `ENUM` fields for controlled state values.



\### User roles



```text

STUDENT

ADMIN

```



\### Resource types



```text

LABORATORY

STUDY\_ROOM

EQUIPMENT

```



\### Resource statuses



```text

AVAILABLE

UNAVAILABLE

```



\### Reservation statuses



```text

PENDING

CONFIRMED

CANCELLED

COMPLETED

```



\### Check-in statuses



```text

NOT\_CHECKED\_IN

CHECKED\_IN

```



Using controlled values prevents unsupported state values from being stored through the database schema.



\---



\# 13. Database Defaults



The schema defines the following default values.



\### User role



```text

STUDENT

```



\### Resource capacity



```text

1

```



\### Resource status



```text

AVAILABLE

```



\### Reservation status



```text

CONFIRMED

```



\### Check-in status



```text

NOT\_CHECKED\_IN

```



The `created\_at` fields for users, resources, and reservations default to the current timestamp.



\---



\# 14. Timestamp Fields



The schema uses timestamps for creation and check-in tracking.



\### Users



```text

created\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP

```



\### Resources



```text

created\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP

```



\### Reservations



```text

created\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP

```



\### Check-ins



```text

checked\_in\_at TIMESTAMP NULL

```



The check-in timestamp can remain `NULL` until the actual check-in occurs.



\---



\# 15. Reservation Data Relationships



A reservation contains two foreign keys:



```text

user\_id

resource\_id

```



This creates the following relationship:



```text

&#x20;            +---------+

&#x20;            |  USERS  |

&#x20;            +----+----+

&#x20;                 |

&#x20;                 | user\_id

&#x20;                 |

&#x20;                 v

&#x20;         +---------------+

&#x20;         | RESERVATIONS  |

&#x20;         +-------+-------+

&#x20;                 ^

&#x20;                 |

&#x20;                 | resource\_id

&#x20;                 |

&#x20;            +----+-------+

&#x20;            | RESOURCES  |

&#x20;            +------------+

```



Therefore, every reservation identifies both:



1\. The user making the reservation.

2\. The resource being reserved.



\---



\# 16. Check-in Relationship



The check-in structure is:



```text

RESERVATION

&#x20;    |

&#x20;    | reservation\_id

&#x20;    v

&#x20;CHECK\_IN

```



Because `check\_ins.reservation\_id` is unique, a reservation cannot have multiple check-in records under the database schema.



The check-in record can transition from:



```text

NOT\_CHECKED\_IN

```



to:



```text

CHECKED\_IN

```



The `checked\_in\_at` field records the time at which the check-in is completed.



\---



\# 17. Database Support for Application Workflows



The database structure directly supports the major CampusReserve workflows.



\## 17.1 Authentication



The `users` table stores:



\* Email

\* Password hash

\* Role

\* Student ID



These values support registration, login, and authorization.



\## 17.2 Resource Discovery



The `resources` table stores:



\* Resource name

\* Resource type

\* Location

\* Capacity

\* Availability status



These values support resource browsing and selection.



\## 17.3 Reservation



The `reservations` table connects a user with a resource and records:



\* Date

\* Start time

\* End time

\* Purpose

\* Status



\## 17.4 Check-in



The `check\_ins` table connects a check-in record to a reservation and stores:



\* QR token

\* Check-in timestamp

\* Check-in status



\---



\# 18. Database-to-Application Mapping



The Flask backend maps database entities to application models.



```text

Database Table       Application Model

\---------------------------------------

users                User

resources            Resource

reservations         Reservation

check\_ins            CheckIn

```



The models are located in:



```text

backend/app/models/

```



The application uses SQLAlchemy to interact with these models.



\---



\# 19. Database Initialization



The database schema is defined in:



```text

database/schema.sql

```



The script creates the database if it does not already exist:



```sql

CREATE DATABASE IF NOT EXISTS campus\_reservation;

```



It then selects the database:



```sql

USE campus\_reservation;

```



The four application tables are subsequently created.



\---



\# 20. Security Considerations



The database stores password hashes rather than plaintext passwords.



Database credentials are not part of the frontend application.



Database connection information is supplied through backend environment configuration.



Sensitive configuration values must not be committed to source control.



Production database credentials should use secure secret-management or environment configuration.



\---



\# 21. Database Design Constraints



The current database design establishes the following constraints:



1\. Every user has a unique primary key.

2\. User email addresses are unique.

3\. Student IDs are unique when provided.

4\. Every resource has a unique primary key.

5\. Every reservation must reference an existing user.

6\. Every reservation must reference an existing resource.

7\. Reservation status values are restricted to the defined enumeration.

8\. Every check-in must reference an existing reservation.

9\. Each reservation can have at most one check-in record.

10\. Each QR token must be unique.

11\. Resource types are restricted to the defined enumeration.

12\. Resource statuses are restricted to the defined enumeration.

13\. Check-in statuses are restricted to the defined enumeration.



\---



\# 22. Database Design Summary



The database can be summarized as:



```text

USERS

&#x20; |

&#x20; | 1:M

&#x20; v

RESERVATIONS

&#x20; |

&#x20; | M:1

&#x20; v

RESOURCES



RESERVATIONS

&#x20; |

&#x20; | 1:0..1

&#x20; v

CHECK\_INS

```



The central entity is `reservations`, which connects users to resources and provides the parent record for check-in operations.



This structure provides the persistent data foundation for CampusReserve's authentication, resource reservation, and check-in functionality.



\---



\# 23. Current Database Status



The database schema is implemented for the current CampusReserve project scope.



The schema contains:



```text

4 tables

```



The primary entities are:



```text

users

resources

reservations

check\_ins

```



The schema provides primary keys, foreign keys, uniqueness constraints, enumerated values, defaults, and timestamps required by the current application.



\---



\# 24. Future Database Considerations



Future versions of CampusReserve may introduce additional entities or constraints if project requirements expand.



Possible future additions could include:



\* Audit records

\* Notifications

\* Recurring reservations

\* Equipment-specific attributes

\* Reservation conflict constraints

\* More detailed user profiles



Such changes should only be introduced when supported by an actual project requirement and should preserve existing relationships and application behavior where possible.



\---



\# 25. Conclusion



The CampusReserve relational database provides a structured foundation for managing users, resources, reservations, and check-ins.



The schema uses primary keys, foreign keys, uniqueness constraints, enumerated values, defaults, and timestamps to maintain data integrity.



The design supports the existing Flask API and React applications while keeping database access centralized within the backend.



