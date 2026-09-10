# Sprint Planning and Definition of Done

> Current-state project evidence reconstructed from the implemented CampusReserve system. This document does not claim historical Scrum activities that were not recorded.

## 1. Sprint 1 Goal

Deliver the core CampusReserve reservation workflow:

- student registration and authentication;
- resource browsing;
- reservation creation;
- reservation viewing;
- reservation cancellation;
- administrator authentication;
- administrator resource management;
- administrator reservation management;
- database persistence;
- protected API access.

## 2. Sprint 1 Backlog

| ID | User Story / Task | Priority | Status |
|---|---|---|---|
| US-01 | Student can register an account | Must Have | Complete |
| US-02 | Student can log in | Must Have | Complete |
| US-03 | Student can browse available resources | Must Have | Complete |
| US-04 | Student can create a reservation | Must Have | Complete |
| US-05 | Student can view reservations | Must Have | Complete |
| US-06 | Student can cancel a reservation | Must Have | Complete |
| US-07 | Administrator can log in | Must Have | Complete |
| US-08 | Administrator can manage resources | Must Have | Complete |
| US-09 | Administrator can view and manage reservations | Must Have | Complete |
| US-10 | Reservation data persists in MySQL | Must Have | Complete |
| US-11 | Protected endpoints require authentication | Must Have | Complete |

## 3. Sprint 2 Backlog

| ID | User Story / Task | Priority | Status |
|---|---|---|---|
| US-12 | Student can check in to a confirmed reservation | Must Have | Complete |
| US-13 | System records check-in information | Must Have | Complete |
| US-14 | Student receives reservation notifications | Should Have | Complete |
| US-15 | Student can view and mark notifications as read | Should Have | Complete |
| US-16 | Automated backend tests cover core functionality | Must Have | Complete |
| US-17 | Frontend and backend quality checks run through CI | Must Have | Complete |
| US-18 | Application is deployed to production | Must Have | Complete |

## 4. Definition of Done

A backlog item is considered Done when:

- [ ] Required functionality is implemented.
- [ ] Code is integrated into the main branch.
- [ ] Relevant backend/frontend functionality works.
- [ ] Data is persisted correctly where applicable.
- [ ] Authentication and authorization requirements are satisfied where applicable.
- [ ] Relevant tests pass.
- [ ] No known critical defect prevents the feature from being used.
- [ ] Relevant documentation is updated.
- [ ] Production configuration is not broken by the change.
- [ ] CI checks pass where applicable.

## 5. Quality Gates

The completed system was evaluated against the following quality gates:

| Quality Gate | Result |
|---|---|
| Backend automated tests | 112 passed |
| Backend coverage | 96% |
| Frontend lint | Passed |
| Frontend production builds | Passed |
| Backend CI | Passed |
| Frontend CI | Passed |
| API workflow verification | Passed |
| Production deployment | Completed |
| QA/UAT-oriented acceptance checks | Passed |

## 6. Release Readiness

CampusReserve is considered release-ready when:

1. Core student and administrator workflows function.
2. Automated tests pass.
3. CI checks pass.
4. Production services are available.
5. API documentation exists.
6. User documentation exists.
7. QA evidence is recorded.
8. Deployment architecture is documented.

The current implementation satisfies these release-readiness conditions.

## 7. Traceability

The Sprint planning evidence connects implementation work to the course requirements for backlog planning, Definition of Done, iterative development, testing, CI/CD, and release readiness.
