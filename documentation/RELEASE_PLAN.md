# Version Management and Release Plan

> Current-state release evidence for CampusReserve. This document records the implemented release process and does not fabricate historical release activity.

## 1. Version Control

CampusReserve uses Git for source-code version control and GitHub as the remote repository.

Primary branch:

master

Release artifacts include:

- source code;
- backend API;
- student frontend;
- administrator frontend;
- database schema;
- automated tests;
- CI configuration;
- technical documentation.

## 2. Release Process

A release should follow these steps:

1. Complete the required implementation.
2. Run automated tests.
3. Verify backend coverage.
4. Run frontend linting.
5. Run frontend production builds.
6. Confirm GitHub Actions CI succeeds.
7. Update relevant documentation.
8. Create a Git release tag.
9. Push the tag to GitHub.
10. Verify the production deployment.

## 3. Current Release

Current release designation:

v1.0.0

Release status:

Production-ready academic project release.

## 4. Release Scope

The v1.0.0 release includes:

- student registration and login;
- administrator login;
- resource browsing and management;
- reservation creation;
- reservation viewing;
- reservation cancellation;
- reservation status management;
- reservation check-in;
- check-in token functionality;
- student notifications;
- JWT authentication;
- MySQL persistence;
- automated backend testing;
- frontend linting and builds;
- GitHub Actions CI;
- Vercel frontend deployment;
- Render backend deployment;
- Aiven MySQL production database.

## 5. Release Quality Gates

| Gate | Result |
|---|---|
| Backend tests | 112 passed |
| Backend coverage | 96% |
| Student frontend lint | Passed |
| Student frontend build | Passed |
| Admin frontend lint | Passed |
| Admin frontend build | Passed |
| Backend CI | Passed |
| Frontend CI | Passed |
| API verification | Passed |
| QA/UAT-oriented checks | Passed |
| Production deployment | Completed |

## 6. Rollback

If a future release introduces a critical defect:

1. Identify the defective release/tag.
2. Restore the last known working version.
3. Redeploy the backend/frontend as applicable.
4. Verify API health.
5. Verify the affected user workflow.
6. Document the defect and corrective action.

## 7. Release Evidence

The Git tag associated with this release provides a stable reference to the version of the project submitted for academic evaluation.
