# CampusReserve Database Design

## 1. Overview

CampusReserve uses a relational MySQL database to store the persistent data required by the campus facility and lab equipment reservation system.

The database contains four primary tables:

1. `users`
2. `resources`
3. `reservations`
4. `check_ins`

These tables support:

* User authentication and authorization
* Resource management
* Reservation management
* Reservation cancellation
* Reservation check-in
* QR/token-based check-in

The Flask backend is the only application component that communicates directly with the database.

The React frontend applications communicate with the Flask REST API and never connect directly to MySQL.

---

# 2. Database Technology

CampusReserve uses MySQL as its relational database management system.

The production database is hosted on **Aiven**.

The production environment uses:

```text
Aiven MySQL
```

The local development environment uses:

```text
MySQL Community Server 8.0.46
```

The production database server currently uses MySQL 8.4.

The Flask backend communicates with MySQL through:

* Flask-SQLAlchemy
* SQLAlchemy
* PyMySQL

The database connection is configured through the backend environment variable:

```text
DATABASE_URL
```

Database credentials are not exposed to the frontend applications.

---

# 3. Database Architecture

The database is positioned behind the Flask backend.

The production data flow is:

```text
+-----------------------+
| Student Frontend      |
| React + Vite / Vercel |
+-----------+-----------+
            |
            | HTTPS / JSON
            v
+-----------------------+
| Administrator         |
| Frontend              |
| React + Vite / Vercel |
+-----------+-----------+
            |
            |
            v
+-----------------------+
| Flask REST API        |
| Render                |
+-----------+-----------+
            |
            | SQL / SSL
            v
+-----------------------+
| MySQL Database        |
| Aiven                 |
+-----------------------+
```

The frontend applications do not have direct database access.

All database operations pass through the backend API.

---

# 4. Database Name

The application database is logically identified as:

```text
campus_reservation
```

The local development database uses:

```text
campus_reservation
```

The production Aiven MySQL service uses the Aiven-provided database environment and connection configuration.

The application does not rely on frontend code to select or access the database.

---

# 5. Entity Relationship Overview

CampusReserve contains four primary entities:

```text
+----------------------+
|        USERS         |
+----------+-----------+
           |
           | 1
           |
           | many
           v
+----------------------+
|    RESERVATIONS      |
+----------+-----------+
           |
           | many
           |
           | 1
           v
+----------------------+
|      RESOURCES       |
+----------------------+


+----------------------+
|    RESERVATIONS      |
+----------+-----------+
           |
           | 1
           |
           | 0..1
           v
+----------------------+
|      CHECK_INS       |
+----------------------+
```

The principal relationships are:

```text
USERS       1 ---- many ---- RESERVATIONS

RESOURCES   1 ---- many ---- RESERVATIONS

RESERVATIONS 1 ---- 0..1 ---- CHECK_INS
```

The `reservations` table is the central transactional entity connecting users and resources.

---

# 6. Users Table

Table name:

```text
users
```

The `users` table stores student and administrator accounts.

## 6.1 Columns

| Column          | Type         | Constraints                 | Description            |
| --------------- | ------------ | --------------------------- | ---------------------- |
| `id`            | INT          | Primary Key, Auto Increment | Unique user identifier |
| `name`          | VARCHAR(100) | NOT NULL                    | User's name            |
| `student_id`    | VARCHAR(50)  | UNIQUE                      | Student identifier     |
| `email`         | VARCHAR(120) | NOT NULL, UNIQUE            | User email address     |
| `password_hash` | VARCHAR(255) | NOT NULL                    | Stored password hash   |
| `role`          | ENUM         | NOT NULL, Default `STUDENT` | User role              |
| `created_at`    | TIMESTAMP    | Default current timestamp   | Account creation time  |

## 6.2 Role Values

The `role` column supports:

```text
STUDENT
ADMIN
```

Newly registered accounts use:

```text
STUDENT
```

unless an authorized administrative process establishes an administrator account.

## 6.3 Constraints

The table enforces:

* `id` as the primary key
* Unique student IDs
* Unique email addresses
* Non-null names
* Non-null email addresses
* Non-null password hashes
* Valid role values

Passwords are stored as password hashes rather than plaintext passwords.

---

# 7. Resources Table

Table name:

```text
resources
```

The `resources` table stores campus facilities and equipment that can be reserved.

## 7.1 Columns

| Column        | Type         | Constraints                   | Description                |
| ------------- | ------------ | ----------------------------- | -------------------------- |
| `id`          | INT          | Primary Key, Auto Increment   | Unique resource identifier |
| `name`        | VARCHAR(100) | NOT NULL                      | Resource name              |
| `type`        | ENUM         | NOT NULL                      | Resource category          |
| `description` | TEXT         | Optional                      | Resource description       |
| `location`    | VARCHAR(150) | NOT NULL                      | Physical location          |
| `capacity`    | INT          | Default `1`                   | Resource capacity          |
| `status`      | ENUM         | NOT NULL, Default `AVAILABLE` | Resource availability      |
| `created_at`  | TIMESTAMP    | Default current timestamp     | Creation time              |

## 7.2 Resource Types

The `type` column supports:

```text
LABORATORY
STUDY_ROOM
EQUIPMENT
```

## 7.3 Resource Status

The `status` column supports:

```text
AVAILABLE
UNAVAILABLE
```

The default status is:

```text
AVAILABLE
```

---

# 8. Reservations Table

Table name:

```text
reservations
```

The `reservations` table records bookings made by users against resources.

## 8.1 Columns

| Column             | Type         | Constraints                 | Description                   |
| ------------------ | ------------ | --------------------------- | ----------------------------- |
| `id`               | INT          | Primary Key, Auto Increment | Unique reservation identifier |
| `user_id`          | INT          | NOT NULL, Foreign Key       | User who made the reservation |
| `resource_id`      | INT          | NOT NULL, Foreign Key       | Reserved resource             |
| `reservation_date` | DATE         | NOT NULL                    | Reservation date              |
| `start_time`       | TIME         | NOT NULL                    | Reservation start time        |
| `end_time`         | TIME         | NOT NULL                    | Reservation end time          |
| `purpose`          | VARCHAR(255) | Optional                    | Reservation purpose           |
| `status`           | ENUM         | NOT NULL                    | Reservation state             |
| `created_at`       | TIMESTAMP    | Default current timestamp   | Reservation creation time     |

## 8.2 Reservation Status

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

The application may update the status through the appropriate reservation or administrative workflow.

---

# 9. Check-ins Table

Table name:

```text
check_ins
```

The `check_ins` table stores check-in information associated with reservations.

## 9.1 Columns

| Column           | Type         | Constraints                   | Description                |
| ---------------- | ------------ | ----------------------------- | -------------------------- |
| `id`             | INT          | Primary Key, Auto Increment   | Unique check-in identifier |
| `reservation_id` | INT          | NOT NULL, UNIQUE, Foreign Key | Associated reservation     |
| `qr_token`       | VARCHAR(255) | NOT NULL, UNIQUE              | Check-in token             |
| `checked_in_at`  | TIMESTAMP    | Nullable                      | Check-in timestamp         |
| `status`         | ENUM         | NOT NULL                      | Check-in state             |

## 9.2 Check-in Status

The `status` column supports:

```text
NOT_CHECKED_IN
CHECKED_IN
```

The default status is:

```text
NOT_CHECKED_IN
```

---

# 10. Primary Keys

Each table has an auto-incrementing integer primary key.

```text
users.id
resources.id
reservations.id
check_ins.id
```

Primary keys uniquely identify individual records.

---

# 11. Foreign Keys

The database defines three primary foreign-key relationships.

## 11.1 User to Reservation

```text
reservations.user_id
        |
        v
users.id
```

This identifies the user who created a reservation.

Relationship:

```text
USERS 1 ---- many RESERVATIONS
```

A user can have multiple reservations.

---

## 11.2 Resource to Reservation

```text
reservations.resource_id
        |
        v
resources.id
```

This identifies the resource being reserved.

Relationship:

```text
RESOURCES 1 ---- many RESERVATIONS
```

A resource can be associated with multiple reservations over time.

---

## 11.3 Reservation to Check-in

```text
check_ins.reservation_id
        |
        v
reservations.id
```

This identifies the reservation associated with a check-in.

Because `reservation_id` is unique in the `check_ins` table, a reservation can have at most one check-in record.

Relationship:

```text
RESERVATIONS 1 ---- 0..1 CHECK_INS
```

---

# 12. Referential Integrity

Foreign keys maintain relationships between related records.

The `reservations` table defines:

```sql
FOREIGN KEY (user_id) REFERENCES users(id)
```

The `reservations` table also defines:

```sql
FOREIGN KEY (resource_id) REFERENCES resources(id)
```

The `check_ins` table defines:

```sql
FOREIGN KEY (reservation_id) REFERENCES reservations(id)
```

These constraints ensure that related records reference existing parent records.

They help prevent orphaned reservations and check-in records.

---

# 13. Uniqueness Constraints

The database uses unique constraints where duplicate values are not permitted.

## Users

```text
student_id UNIQUE
email UNIQUE
```

## Check-ins

```text
reservation_id UNIQUE
qr_token UNIQUE
```

The unique `reservation_id` constraint ensures that a reservation cannot have multiple check-in records.

The unique `qr_token` constraint prevents duplicate check-in tokens.

---

# 14. Enumerated Values

The database uses MySQL `ENUM` fields for controlled state and category values.

## User roles

```text
STUDENT
ADMIN
```

## Resource types

```text
LABORATORY
STUDY_ROOM
EQUIPMENT
```

## Resource statuses

```text
AVAILABLE
UNAVAILABLE
```

## Reservation statuses

```text
PENDING
CONFIRMED
CANCELLED
COMPLETED
```

## Check-in statuses

```text
NOT_CHECKED_IN
CHECKED_IN
```

Using controlled values helps prevent unsupported state values from being stored in these fields.

---

# 15. Database Defaults

The schema defines the following defaults.

## User role

```text
STUDENT
```

## Resource capacity

```text
1
```

## Resource status

```text
AVAILABLE
```

## Reservation status

```text
CONFIRMED
```

## Check-in status

```text
NOT_CHECKED_IN
```

The `created_at` fields for users, resources, and reservations default to the current timestamp.

---

# 16. Timestamp Fields

The schema uses timestamps for creation and check-in tracking.

## Users

```text
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

## Resources

```text
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

## Reservations

```text
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

## Check-ins

```text
checked_in_at TIMESTAMP NULL
```

The check-in timestamp can remain `NULL` until the actual check-in occurs.

---

# 17. Reservation Data Relationships

A reservation contains two foreign keys:

```text
user_id
resource_id
```

The relationship can be represented as:

```text
             +---------+
             |  USERS  |
             +----+----+
                  |
                  | user_id
                  |
                  v
          +---------------+
          | RESERVATIONS  |
          +-------+-------+
                  ^
                  |
                  | resource_id
                  |
             +----+-------+
             | RESOURCES  |
             +------------+
```

Every reservation identifies:

1. The user making the reservation.
2. The resource being reserved.

---

# 18. Check-in Relationship

The check-in structure is:

```text
RESERVATION
     |
     | reservation_id
     v
CHECK_IN
```

Because `check_ins.reservation_id` is unique, a reservation cannot have multiple check-in records under the database schema.

The check-in state can transition from:

```text
NOT_CHECKED_IN
```

to:

```text
CHECKED_IN
```

The `checked_in_at` field records the time associated with completed check-in.

---

# 19. Database Support for Application Workflows

The database structure directly supports the major CampusReserve workflows.

## 19.1 Authentication

The `users` table stores:

* Email
* Password hash
* Role
* Student ID

These values support registration, login, and authorization.

---

## 19.2 Resource Discovery

The `resources` table stores:

* Resource name
* Resource type
* Location
* Capacity
* Availability status

These values support resource browsing and selection.

---

## 19.3 Reservation

The `reservations` table connects a user with a resource and records:

* Date
* Start time
* End time
* Purpose
* Status

---

## 19.4 Check-in

The `check_ins` table connects a check-in record to a reservation and stores:

* QR/token value
* Check-in timestamp
* Check-in status

---

# 20. Database-to-Application Mapping

The Flask backend maps database entities to application models.

```text
Database Table       Application Model
---------------------------------------
users                User
resources            Resource
reservations         Reservation
check_ins            CheckIn
```

The models are located in:

```text
backend/app/models/
```

The application uses SQLAlchemy to interact with these models.

---

# 21. Database Schema Files

The database structure is defined in:

```text
database/schema.sql
```

Initial data is defined in:

```text
database/seed.sql
```

The schema contains the four application tables:

```text
users
resources
reservations
check_ins
```

The schema uses deployment-compatible table creation statements so that it can be applied to an existing database environment.

The database creation script is not responsible for exposing database credentials or application configuration.

---

# 22. Schema Initialization and Deployment

The database schema can be initialized using the project's SQL files.

The schema file:

```text
database/schema.sql
```

creates the required application tables.

The seed file:

```text
database/seed.sql
```

provides the initial resource data used by the application.

The deployment-ready schema does not depend on a hard-coded database name being selected inside the SQL script.

Instead, the target database is selected by the database connection used to execute the schema.

This allows the same schema structure to be applied to the configured production database environment.

---

# 23. Seeded Resources

The project seed data includes the following initial resources:

| ID | Name           | Type       | Location  | Capacity | Status    |
| -: | -------------- | ---------- | --------- | -------: | --------- |
|  1 | Computer Lab 1 | LABORATORY | ICT Block |       30 | AVAILABLE |
|  2 | Computer Lab 2 | LABORATORY | ICT Block |       25 | AVAILABLE |
|  3 | Study Room A   | STUDY_ROOM | Library   |        8 | AVAILABLE |
|  4 | Projector 1    | EQUIPMENT  | ICT Store |        1 | AVAILABLE |

These records provide initial reservable resources for the application.

Additional resources can be created or managed through the administrative functionality.

---

# 24. Production Database

The production CampusReserve database is hosted on Aiven.

The production architecture is:

```text
Vercel Frontends
       |
       | HTTPS
       v
Render Flask API
       |
       | SQL / SSL
       v
Aiven MySQL
```

The backend uses the production database connection supplied through:

```text
DATABASE_URL
```

The database connection is handled exclusively by the backend.

The frontend applications have no access to the production database credentials.

---

# 25. Local Development Database

During local development, the backend can communicate with a local MySQL installation.

The local environment uses:

```text
MySQL Community Server 8.0.46
```

The local database is:

```text
campus_reservation
```

The local backend API runs at:

```text
http://127.0.0.1:5000/api
```

The local frontend applications communicate with the local Flask API rather than directly with MySQL.

---

# 26. Production Database Connection

The production backend is hosted on Render.

The Render backend connects to the Aiven MySQL database using the configured `DATABASE_URL`.

The backend configuration converts the Aiven MySQL connection to the PyMySQL SQLAlchemy driver when necessary.

The production database connection uses SSL-secured communication.

The frontend applications do not receive or process the database connection string.

---

# 27. Database Security

The database security architecture follows several principles.

### Password protection

Passwords are stored as password hashes.

Plaintext passwords are not stored in the database.

### Backend-only database access

Only the Flask backend communicates with MySQL.

### Environment-based credentials

Database connection information is supplied through environment configuration.

### Secret protection

Sensitive values such as:

```text
DATABASE_URL
SECRET_KEY
JWT_SECRET_KEY
```

must remain outside source control.

### Production encryption

Communication between the production backend and Aiven MySQL uses SSL.

### Frontend isolation

Neither React frontend contains production database credentials.

---

# 28. Database Testing Architecture

The backend automated tests use an isolated SQLite database for test execution.

This prevents automated tests from modifying the development or production MySQL database.

The test application is created through the same Flask application factory used by the main application.

The testing architecture is therefore:

```text
pytest
  |
  v
Flask Test Application
  |
  v
SQLite In-Memory Database
```

The production architecture remains:

```text
Flask Application
  |
  v
SQLAlchemy / PyMySQL
  |
  v
Aiven MySQL
```

The separation allows application behavior to be tested safely without depending on the production database.

---

# 29. Database Design Constraints

The current database design establishes the following constraints:

1. Every table has a unique primary key.
2. User email addresses are unique.
3. Student IDs are unique when provided.
4. Every reservation must reference an existing user.
5. Every reservation must reference an existing resource.
6. Reservation status values are restricted to the defined enumeration.
7. Every check-in must reference an existing reservation.
8. Each reservation can have at most one check-in record.
9. Each QR token must be unique.
10. Resource types are restricted to the defined enumeration.
11. Resource statuses are restricted to the defined enumeration.
12. Check-in statuses are restricted to the defined enumeration.
13. Default values are defined for applicable role, status, capacity, and timestamp fields.

---

# 30. Database Integrity and Application Validation

Database constraints provide structural data integrity, while the Flask API provides application-level validation.

The backend validates conditions including:

* Required fields
* Valid resource identifiers
* Resource availability
* Reservation dates
* Reservation times
* Reservation status values
* User authentication
* User authorization
* Reservation ownership
* Check-in eligibility
* Duplicate check-in attempts

The database then enforces structural constraints such as:

* Primary keys
* Foreign keys
* Unique values
* ENUM values
* NOT NULL requirements
* Default values

This creates two complementary layers of data protection:

```text
Application Validation
        |
        v
Database Constraints
        |
        v
Persistent Data
```

---

# 31. Database Access Architecture

Database access follows the following path:

```text
React Frontend
      |
      | HTTP / HTTPS
      v
Flask REST API
      |
      v
Route Validation
      |
      v
SQLAlchemy Model
      |
      v
PyMySQL
      |
      v
MySQL
```

The database is therefore isolated from the presentation layer.

No frontend component is designed to execute SQL directly.

---

# 32. Database-to-API Relationship

The database supports the REST API resources exposed by the Flask backend.

The general mapping is:

```text
users
   |
   +---- Authentication / User APIs

resources
   |
   +---- Resource APIs

reservations
   |
   +---- Reservation APIs

check_ins
   |
   +---- Check-in APIs
```

Administrative API operations use the same underlying database entities but apply additional administrator authorization.

---

# 33. Database Lifecycle

The database lifecycle consists of:

```text
Schema Definition
       |
       v
Database Initialization
       |
       v
Seed Data
       |
       v
Application Operations
       |
       v
Reservations / Check-ins / Updates
```

The schema is maintained in the repository.

Seed data provides the initial application resources.

Application operations are performed through the Flask API.

The frontend applications do not directly modify database records.

---

# 34. Database Design Summary

The CampusReserve database can be summarized as:

```text
USERS
  |
  | 1:M
  v
RESERVATIONS
  |
  | M:1
  v
RESOURCES


RESERVATIONS
  |
  | 1:0..1
  v
CHECK_INS
```

The central transactional entity is:

```text
reservations
```

It connects users to resources and provides the parent record for check-in operations.

The four-table design provides the persistent data foundation for:

* Authentication
* Authorization
* Resource management
* Reservations
* Reservation cancellation
* Check-in
* QR/token-based check-in
* Administrative management

---

# 35. Current Database Status

The CampusReserve database schema is implemented for the current project scope.

The schema contains:

```text
4 tables
```

The primary entities are:

```text
users
resources
reservations
check_ins
```

The production database is hosted on Aiven and is connected to the Flask backend running on Render.

The database has been initialized with the project's schema and seed resource data.

The deployed application has successfully used the production database for student and administrator workflows, including:

* Authentication
* Resource retrieval
* Reservation creation
* Reservation cancellation
* Check-in
* Administrator reservation viewing
* Administrator check-in viewing
* Administrator user viewing

---

# 36. Future Database Considerations

Future versions of CampusReserve may introduce additional entities or constraints if project requirements expand.

Possible future additions include:

* Audit records
* Notifications
* Recurring reservations
* Equipment-specific attributes
* More advanced reservation conflict constraints
* More detailed user profiles

Such changes should only be introduced when supported by an actual project requirement.

Future schema changes should preserve existing relationships and application behavior where possible.

---

# 37. Conclusion

The CampusReserve relational database provides a structured persistent foundation for managing users, resources, reservations, and check-ins.

The schema uses:

* Primary keys
* Foreign keys
* Unique constraints
* ENUM values
* NOT NULL constraints
* Default values
* Timestamps

to maintain data integrity.

The database is accessed exclusively through the Flask backend using SQLAlchemy and PyMySQL.

The production database is hosted on Aiven, while the Flask API is deployed on Render and the React frontend applications are deployed on Vercel.

This architecture keeps database credentials and database operations on the server side while allowing the student and administrator applications to interact with the system through the REST API.

The four-table relational design is sufficient for the current CampusReserve academic project scope and provides a maintainable foundation for future enhancements.
