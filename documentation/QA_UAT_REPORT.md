# CampusReserve — QA & UAT Report

## 1. Purpose

This report records the quality assurance, API integration, and user acceptance evidence completed for the CampusReserve — Campus Smart Facility & Lab Equipment Reservation System.

The report is based only on tests and results actually completed during development. No unperformed tests or fabricated evidence are included.

## 2. System Under Test

**Project:** CampusReserve — Campus Smart Facility & Lab Equipment Reservation System

**Architecture:** Layered/client-server REST architecture

**Frontend:** React + Vite  
**Backend:** Flask REST API  
**Database:** MySQL

## 3. Automated Test Results

| Metric | Result |
|---|---:|
| Tests executed | 112 |
| Tests passed | 112 |
| Tests failed | 0 |
| Coverage | 96% |
| Warnings | 3 |

The automated backend test suite achieved **112/112 passing tests** with **96% code coverage**.

The three warnings were existing `datetime.utcnow()` deprecation warnings. They did not cause test failures.

The achieved 96% coverage exceeds the approximately 70% project testing target.

## 4. API / Integration Testing

| ID | Test | Result | Status |
|---|---|---|---|
| API-01 | Health endpoint | HTTP 200 returned | PASS |
| API-02 | Student login | Login successful and token returned | PASS |
| API-03 | Resource listing | Four resources returned | PASS |
| API-04 | Create reservation | Reservation 14 created as PENDING | PASS |
| API-05 | Student reservations | Reservation 14 visible | PASS |
| API-06 | Admin login | Login successful and token returned | PASS |
| API-07 | Admin reservations | Reservation 14 visible | PASS |
| API-08 | Confirm reservation | Reservation 14 changed to CONFIRMED | PASS |
| API-09 | Notifications | Confirmation notification returned | PASS |
| API-10 | Mark notification read | HTTP 200; notification marked read | PASS |

## 5. End-to-End Reservation Workflow

1. Student authenticated successfully.
2. Student retrieved available resources.
3. Student created a reservation for Computer Lab 1.
4. Reservation was created with status **PENDING**.
5. Student retrieved their reservations.
6. Administrator authenticated successfully.
7. Administrator retrieved all reservations.
8. Administrator located Reservation 14.
9. Administrator confirmed the reservation.
10. Reservation status changed to **CONFIRMED**.
11. Student retrieved notifications.
12. A reservation-confirmation notification was generated.
13. Student marked the notification as read.
14. The notification endpoint returned a successful response.

## 6. User Acceptance Testing (UAT)

| ID | Acceptance Scenario | Result |
|---|---|---|
| UAT-01 | Student can register and authenticate | PASS |
| UAT-02 | Student can browse available facilities/equipment | PASS |
| UAT-03 | Student can submit a reservation request | PASS |
| UAT-04 | Administrator can view and approve a reservation | PASS |
| UAT-05 | Student receives an in-app notification after approval | PASS |
| UAT-06 | Student can view reservation status and notifications | PASS |
| UAT-07 | Reservation/check-in functionality is implemented and tested | PASS |

These acceptance checks are based on demonstrated functionality. They are not claimed as formal sign-offs by external UAT participants unless such evidence exists.

## 7. Defect / Issue Observed During Testing

During notification testing, the initial Postman request incorrectly used:

`{{base_url}}/api/notifications/4/read`

Because `base_url` already contained `/api`, this produced `/api/api/notifications/4/read` and returned HTTP 404.

The request was corrected to:

`{{base_url}}/notifications/4/read`

The corrected request returned HTTP 200 and successfully marked the notification as read.

**Resolution:** Postman request URL corrected. No application defect was identified.

## 8. Overall QA Assessment

- Backend automated tests: **PASS**
- Automated test pass rate: **100%**
- Backend coverage: **96%**
- Authentication workflow: **PASS**
- Resource retrieval: **PASS**
- Reservation creation: **PASS**
- Administrative approval: **PASS**
- Notification generation: **PASS**
- Notification read functionality: **PASS**
- Check-in functionality: **implemented and tested**
- Production deployment: **completed and verified**

### Overall Status

**QA STATUS: PASS**

The implemented core CampusReserve functionality is sufficiently tested for the project demonstration and presentation.

## 9. Evidence Integrity Statement

This report records only testing activities and results that were actually performed.

No fabricated screenshots, deployment results, test runs, coverage figures, or user acceptance results have been included.

## 10. Conclusion

CampusReserve has successfully passed the main automated and integration testing activities completed during development.

The combination of **112 passing automated tests, 96% backend coverage, successful Postman API testing, and successful end-to-end reservation approval workflow** provides evidence that the core implemented system is functioning as intended.

The system is ready for final presentation and demonstration, subject to completion of any remaining academic documentation requirements.
