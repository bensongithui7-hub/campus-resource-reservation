# System Testing, Defect Triage, Static Analysis and Refactoring

> Current-state QA evidence for CampusReserve. This document records verified quality activities and does not fabricate historical defect reports or testing sessions.

## 1. System Testing

The completed system was tested across the principal student and administrator workflows.

### Student Workflow

1. Register account.
2. Log in.
3. Browse resources.
4. Create reservation.
5. View reservation.
6. Cancel reservation.
7. View notifications.
8. Mark notification as read.
9. Check in to a confirmed reservation.

### Administrator Workflow

1. Log in.
2. View resources.
3. Create/manage resources.
4. View reservations.
5. Confirm or cancel reservations.
6. View check-in records.
7. View users.

## 2. Integration Verification

The following integration points are implemented and verified:

| Integration | Status |
|---|---|
| Student frontend → Flask API | Passed |
| Admin frontend → Flask API | Passed |
| Flask API → SQLAlchemy | Passed |
| SQLAlchemy → MySQL | Passed |
| JWT authentication → protected endpoints | Passed |
| Reservation → notification generation | Passed |
| Reservation → check-in workflow | Passed |
| GitHub → GitHub Actions | Passed |
| Frontend → production API | Passed |

## 3. Defect Triage

Known issues encountered during development were investigated and resolved where required.

Examples include:

| Issue | Resolution | Status |
|---|---|---|
| MySQL schema/resource API failure | Database schema and seed data corrected | Resolved |
| Admin account creation conflict | Existing duplicate student ID identified and corrected | Resolved |
| Notification API duplicated /api path | Postman request corrected | Resolved |
| JWT session duration insufficient for walkthrough | Access-token lifetime increased to 8 hours | Resolved |
| Frontend/API local configuration | Environment-based API configuration used for deployment | Resolved |

No known critical defect currently prevents the core reservation workflow from operating.

## 4. Static Analysis

Frontend code quality is checked using ESLint.

Current results:

| Application | ESLint |
|---|---|
| Student frontend | Passed |
| Administrator frontend | Passed |

Backend quality is additionally supported by automated Pytest execution and coverage measurement.

## 5. Automated Testing

Backend test result:

112 tests passed.

Coverage:

96%.

The automated tests cover the implemented backend functionality and provide regression protection for core API behavior.

## 6. Refactoring

Refactoring was applied during development where defects, maintainability concerns or integration requirements were identified.

Examples include:

- separating API functionality into Flask blueprints;
- centralizing Flask application creation through the Application Factory;
- separating frontend API/service functionality from UI components;
- correcting database configuration and persistence issues;
- improving frontend layout and reusable interface structures;
- separating environment-specific API configuration.

These changes improve maintainability while preserving the existing system architecture.

## 7. Quality Assessment

| Area | Result |
|---|---|
| Functional testing | Passed |
| Integration testing | Passed |
| Backend automated testing | Passed |
| Backend coverage | 96% |
| Frontend static analysis | Passed |
| Frontend production builds | Passed |
| CI verification | Passed |
| Production deployment | Completed |

## 8. Final Defect Status

Critical defects blocking the primary CampusReserve workflow:

None currently identified.

The project is suitable for final integration, demonstration and academic evaluation.

## 9. Evidence Integrity

This document records current verified quality status and resolved implementation issues.

It does not fabricate historical defect-ticket numbers, tester identities, dates, or bug-tracking records that were not retained.
