\# UML Activity Diagrams — CampusReserve



\## 1. Purpose



The UML Activity Diagrams describe the workflows and decision points of the CampusReserve system.



They model the flow of actions from the user's initial interaction through validation, processing, database operations, and completion or error handling.



The activities documented are based on the implemented CampusReserve functionality and the system requirements.



\---



\## 2. Student Registration and Login



\### Activity Flow



1\. Student opens the CampusReserve application.

2\. Student chooses registration or login.

3\. For registration, the student enters the required account information.

4\. The system validates the submitted information.

5\. The system checks for duplicate email or student ID.

6\. If valid, the account is created.

7\. The student can then log in.

8\. For login, the student submits email and password.

9\. The authentication system verifies the credentials.

10\. If authentication succeeds, a JWT is issued.

11\. The student is taken to the authenticated dashboard.

12\. If authentication fails, an error is displayed.



\### Activity Diagram



```mermaid

flowchart TD

&#x20;   A(\[Start]) --> B\[Open CampusReserve]

&#x20;   B --> C{Register or Login?}



&#x20;   C -->|Register| D\[Enter registration details]

&#x20;   D --> E\[Validate required fields]

&#x20;   E --> F{Valid details?}

&#x20;   F -->|No| G\[Display validation error]

&#x20;   G --> D

&#x20;   F -->|Yes| H\[Check duplicate email/student ID]

&#x20;   H --> I{Account already exists?}

&#x20;   I -->|Yes| J\[Display duplicate account error]

&#x20;   J --> D

&#x20;   I -->|No| K\[Create user account]

&#x20;   K --> L\[Proceed to Login]



&#x20;   C -->|Login| M\[Enter email and password]

&#x20;   L --> M

&#x20;   M --> N\[Send login request]

&#x20;   N --> O\[Verify credentials]

&#x20;   O --> P{Credentials valid?}

&#x20;   P -->|No| Q\[Display login error]

&#x20;   Q --> M

&#x20;   P -->|Yes| R\[Generate JWT]

&#x20;   R --> S\[Store authenticated session]

&#x20;   S --> T\[Display dashboard]

&#x20;   T --> U(\[End])

```



\---



\## 3. Browse Resources



\### Activity Flow



1\. Student opens the resources section.

2\. Frontend requests available resources from the backend.

3\. Backend retrieves resources from the database.

4\. Resource information is returned.

5\. Student views the resource list.

6\. Student may select a resource to view its details.



\### Activity Diagram



```mermaid

flowchart TD

&#x20;   A(\[Start]) --> B\[Open Resources]

&#x20;   B --> C\[Request resource list]

&#x20;   C --> D\[GET /api/resources]

&#x20;   D --> E\[Retrieve resources from database]

&#x20;   E --> F\[Return resource records]

&#x20;   F --> G\[Display resource list]

&#x20;   G --> H{View resource details?}

&#x20;   H -->|Yes| I\[Select resource]

&#x20;   I --> J\[Request resource details]

&#x20;   J --> K\[GET /api/resources/{id}]

&#x20;   K --> L\[Display resource details]

&#x20;   L --> M(\[End])

&#x20;   H -->|No| M

```



\---



\## 4. Create Reservation



\### Activity Flow



1\. Student selects a resource.

2\. Student enters reservation date.

3\. Student enters start and end times.

4\. Student enters the reservation purpose where applicable.

5\. Frontend sends the reservation request with authentication.

6\. Backend validates the authenticated user.

7\. Backend validates the submitted reservation data.

8\. Backend retrieves the requested resource.

9\. Resource availability is checked.

10\. Date and time values are validated.

11\. The reservation is created.

12\. Confirmation is returned to the student.

13\. If validation fails, an appropriate error is displayed.



\### Activity Diagram



```mermaid

flowchart TD

&#x20;   A(\[Start]) --> B\[Select resource]

&#x20;   B --> C\[Enter reservation date]

&#x20;   C --> D\[Enter start and end time]

&#x20;   D --> E\[Enter reservation purpose]

&#x20;   E --> F\[Submit reservation]

&#x20;   F --> G\[Authenticate student]

&#x20;   G --> H{Authenticated?}



&#x20;   H -->|No| I\[Return authentication error]

&#x20;   I --> Z(\[End])



&#x20;   H -->|Yes| J\[Validate reservation fields]

&#x20;   J --> K{Fields valid?}

&#x20;   K -->|No| L\[Display validation error]

&#x20;   L --> Z



&#x20;   K -->|Yes| M\[Retrieve resource]

&#x20;   M --> N{Resource exists?}

&#x20;   N -->|No| O\[Display resource not found]

&#x20;   O --> Z



&#x20;   N -->|Yes| P{Resource available?}

&#x20;   P -->|No| Q\[Display unavailable resource error]

&#x20;   Q --> Z



&#x20;   P -->|Yes| R\[Validate reservation date and time]

&#x20;   R --> S{Date/time valid?}

&#x20;   S -->|No| T\[Display date/time error]

&#x20;   T --> Z



&#x20;   S -->|Yes| U\[Create reservation]

&#x20;   U --> V\[Store reservation]

&#x20;   V --> W\[Return confirmation]

&#x20;   W --> X\[Display reservation confirmation]

&#x20;   X --> Z

```



\---



\## 5. View and Cancel Reservation



\### Activity Flow



1\. Student opens My Reservations.

2\. System retrieves the student's reservations.

3\. Student views reservation history.

4\. Student selects a reservation.

5\. Student chooses whether to cancel it.

6\. The system verifies ownership.

7\. The reservation is checked for cancellation eligibility.

8\. The reservation status is changed to `CANCELLED`.

9\. Updated reservation information is returned.

10\. The student sees the updated reservation status.



\### Activity Diagram



```mermaid

flowchart TD

&#x20;   A(\[Start]) --> B\[Open My Reservations]

&#x20;   B --> C\[Request current student's reservations]

&#x20;   C --> D\[Display reservation history]

&#x20;   D --> E{Cancel reservation?}



&#x20;   E -->|No| F(\[End])

&#x20;   E -->|Yes| G\[Select reservation]

&#x20;   G --> H\[Send cancellation request]

&#x20;   H --> I\[Authenticate student]

&#x20;   I --> J{Authenticated?}



&#x20;   J -->|No| K\[Display authentication error]

&#x20;   K --> F



&#x20;   J -->|Yes| L\[Retrieve reservation]

&#x20;   L --> M{Reservation exists?}

&#x20;   M -->|No| N\[Display not found error]

&#x20;   N --> F



&#x20;   M -->|Yes| O{Student owns reservation?}

&#x20;   O -->|No| P\[Display authorization error]

&#x20;   P --> F



&#x20;   O -->|Yes| Q{Already cancelled?}

&#x20;   Q -->|Yes| R\[Display already cancelled message]

&#x20;   R --> F



&#x20;   Q -->|No| S\[Set status to CANCELLED]

&#x20;   S --> T\[Save updated reservation]

&#x20;   T --> U\[Return cancellation confirmation]

&#x20;   U --> V\[Display updated reservation]

&#x20;   V --> F

```



\---



\## 6. QR Check-In



\### Activity Flow



1\. Student opens the check-in function.

2\. Student selects or accesses the reservation check-in.

3\. The system authenticates the student.

4\. The reservation is retrieved.

5\. Ownership and check-in eligibility are verified.

6\. The system processes the check-in.

7\. Check-in status becomes `CHECKED\_IN`.

8\. Check-in timestamp is recorded.

9\. Confirmation is displayed.



The system also supports QR-token-based check-in.



\### Activity Diagram



```mermaid

flowchart TD

&#x20;   A(\[Start]) --> B\[Open check-in]

&#x20;   B --> C{Check-in method?}



&#x20;   C -->|Reservation Check-In| D\[Select reservation]

&#x20;   C -->|QR Token| E\[Provide QR token]



&#x20;   D --> F\[Send reservation check-in request]

&#x20;   E --> G\[Send QR token check-in request]



&#x20;   F --> H\[Authenticate student]

&#x20;   G --> I\[Find check-in by QR token]



&#x20;   H --> J{Authenticated?}

&#x20;   J -->|No| K\[Display authentication error]

&#x20;   K --> Z(\[End])



&#x20;   J -->|Yes| L\[Retrieve reservation]

&#x20;   L --> M{Reservation valid and eligible?}

&#x20;   M -->|No| N\[Display check-in error]

&#x20;   N --> Z



&#x20;   M -->|Yes| O\[Retrieve or create check-in record]

&#x20;   I --> P{QR token valid?}

&#x20;   P -->|No| Q\[Display invalid QR token error]

&#x20;   Q --> Z

&#x20;   P -->|Yes| O



&#x20;   O --> R{Already checked in?}

&#x20;   R -->|Yes| S\[Reject duplicate check-in]

&#x20;   S --> Z



&#x20;   R -->|No| T\[Set status to CHECKED\_IN]

&#x20;   T --> U\[Record check-in timestamp]

&#x20;   U --> V\[Save check-in]

&#x20;   V --> W\[Return check-in confirmation]

&#x20;   W --> X\[Display successful check-in]

&#x20;   X --> Z

```



\---



\## 7. Administrator Resource Management



\### Activity Flow



1\. Administrator logs into the admin portal.

2\. Administrator opens resource management.

3\. The system retrieves resource records.

4\. Administrator selects a resource.

5\. Administrator chooses an operation.

6\. The system validates the administrator's authorization.

7\. The selected resource is updated or deleted.

8\. The system returns the result.

9\. The admin portal displays the updated resource list.



\### Activity Diagram



```mermaid

flowchart TD

&#x20;   A(\[Start]) --> B\[Admin logs in]

&#x20;   B --> C\[Authenticate credentials]

&#x20;   C --> D{Authentication successful?}



&#x20;   D -->|No| E\[Display login error]

&#x20;   E --> Z(\[End])



&#x20;   D -->|Yes| F\[Open Resource Management]

&#x20;   F --> G\[Retrieve resources]

&#x20;   G --> H\[Display resource list]

&#x20;   H --> I\[Select resource]

&#x20;   I --> J{Select operation?}



&#x20;   J -->|Update| K\[Enter updated resource information]

&#x20;   K --> L\[Validate update]

&#x20;   L --> M{Valid update?}

&#x20;   M -->|No| N\[Display validation error]

&#x20;   N --> H

&#x20;   M -->|Yes| O\[Update resource]

&#x20;   O --> P\[Save changes]

&#x20;   P --> H



&#x20;   J -->|Change Availability| Q\[Select availability status]

&#x20;   Q --> R\[Update resource status]

&#x20;   R --> S\[Save status]

&#x20;   S --> H



&#x20;   J -->|Delete| T\[Request resource deletion]

&#x20;   T --> U\[Delete resource]

&#x20;   U --> V\[Save deletion]

&#x20;   V --> H



&#x20;   H --> W(\[End])

```



\---



\## 8. Administrator Reservation Management



\### Activity Flow



1\. Administrator opens reservation management.

2\. The system retrieves all reservations.

3\. Administrator views reservation records.

4\. Administrator selects a reservation.

5\. Administrator selects a new reservation status.

6\. Backend validates the administrator's authorization.

7\. Backend validates the requested status.

8\. Reservation status is updated.

9\. Updated information is returned.



\### Activity Diagram



```mermaid

flowchart TD

&#x20;   A(\[Start]) --> B\[Open Reservation Management]

&#x20;   B --> C\[Request all reservations]

&#x20;   C --> D\[Authenticate administrator]

&#x20;   D --> E{Administrator authorized?}



&#x20;   E -->|No| F\[Display authorization error]

&#x20;   F --> Z(\[End])



&#x20;   E -->|Yes| G\[Retrieve reservations]

&#x20;   G --> H\[Display reservation list]

&#x20;   H --> I\[Select reservation]

&#x20;   I --> J\[Select new status]

&#x20;   J --> K\[Validate requested status]

&#x20;   K --> L{Status valid?}



&#x20;   L -->|No| M\[Display invalid status error]

&#x20;   M --> Z



&#x20;   L -->|Yes| N\[Update reservation status]

&#x20;   N --> O\[Save changes]

&#x20;   O --> P\[Return updated reservation]

&#x20;   P --> Q\[Display updated status]

&#x20;   Q --> Z

```



\---



\## 9. Activity Diagram Summary



| Activity                | Actor         | Main Outcome                        |

| ----------------------- | ------------- | ----------------------------------- |

| Registration/Login      | Student       | Authenticated user session          |

| Browse Resources        | Student       | Resource information displayed      |

| Create Reservation      | Student       | Reservation created                 |

| View/Cancel Reservation | Student       | Reservation history or cancellation |

| QR Check-In             | Student       | Reservation marked as checked in    |

| Resource Management     | Administrator | Resource records managed            |

| Reservation Management  | Administrator | Reservation status managed          |



\---



\## 10. Implementation Traceability



| Activity                 | Relevant Implementation                            |

| ------------------------ | -------------------------------------------------- |

| Registration             | `POST /api/auth/register`                          |

| Login                    | `POST /api/auth/login`                             |

| Browse Resources         | `GET /api/resources`                               |

| Resource Details         | `GET /api/resources/<id>`                          |

| Create Reservation       | `POST /api/reservations`                           |

| View Reservations        | `GET /api/reservations`                            |

| View Reservation         | `GET /api/reservations/<id>`                       |

| Cancel Reservation       | `DELETE /api/reservations/<id>`                    |

| Reservation Check-In     | `POST /api/reservations/<reservation\_id>/check-in` |

| QR Check-In              | `POST /api/check-in/<qr\_token>`                    |

| Admin Reservations       | `GET /api/admin/reservations`                      |

| Admin Resource Update    | `PUT /api/admin/resources/<id>`                    |

| Admin Resource Status    | `PUT /api/admin/resources/<id>/status`             |

| Admin Resource Delete    | `DELETE /api/admin/resources/<id>`                 |

| Admin Reservation Status | `PUT /api/admin/reservations/<id>/status`          |



\---



\## 11. IBL 3300 Alignment



The Activity Diagrams demonstrate:



\* Workflow modelling.

\* System decision points.

\* Normal and alternative flows.

\* User and administrator interactions.

\* Validation and authorization.

\* Reservation lifecycle behaviour.

\* Resource management.

\* QR-based check-in.

\* Traceability between UML design and implemented functionality.



The diagrams complement the Use-Case, Class, and Sequence Diagrams and provide a behavioural view of the CampusReserve system.



\---



\## 12. Visual Diagram Requirement



For the final IBL 3300 documentation, the Mermaid diagrams should be recreated or exported as formal visual UML activity diagrams using draw.io or another suitable diagramming tool.



The final visual diagrams should clearly show:



\* Initial nodes.

\* Actions.

\* Decision nodes.

\* Alternative/error paths.

\* Flow arrows.

\* Final nodes.

\* Actor or responsibility separation where appropriate.



The visual diagrams must remain consistent with the implemented system documented in the SRS, API documentation, database documentation, and source code.



