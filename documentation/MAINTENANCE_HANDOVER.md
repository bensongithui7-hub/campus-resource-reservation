# Maintenance and Handover Plan

> Current-state maintenance and handover documentation for CampusReserve.

## 1. System Overview

CampusReserve is a web-based and mobile-responsive campus facility and equipment reservation system.

Architecture:

React/Vite Student Frontend
        |
React/Vite Admin Frontend
        |
     Flask REST API
        |
     MySQL Database

Production deployment:

- Student frontend: Vercel
- Administrator frontend: Vercel
- Backend API: Render
- Production database: Aiven MySQL

## 2. Maintenance Responsibilities

| Area | Primary Responsibility |
|---|---|
| Backend/API | Benson |
| Database | Benson |
| Authentication | Benson |
| Student Frontend | Ogeto |
| Admin Frontend | Ogeto |
| Requirements/Documentation | Felistus |
| QA/UAT coordination | Felistus |
| Deployment/Integration | Benson |
| Project coordination | Felistus |

## 3. Corrective Maintenance

Corrective maintenance addresses defects discovered after release.

Process:

1. Reproduce the defect.
2. Identify the affected component.
3. Implement the smallest appropriate correction.
4. Run relevant automated tests.
5. Run frontend lint/build checks where applicable.
6. Verify the affected workflow.
7. Commit the correction to Git.
8. Allow CI to verify the change.
9. Deploy when appropriate.

## 4. Adaptive Maintenance

Adaptive maintenance may be required when:

- hosting platforms change;
- database configuration changes;
- dependency versions require updates;
- browser compatibility requirements change;
- environment variables change;
- deployment configuration changes.

Changes should preserve the existing client-server layered architecture unless a future project revision formally changes the scope.

## 5. Preventive Maintenance

Preventive maintenance includes:

- keeping dependencies reasonably current;
- monitoring CI failures;
- maintaining automated tests;
- maintaining backend test coverage;
- maintaining ESLint checks;
- reviewing application logs;
- removing obsolete configuration;
- keeping technical documentation synchronized with the implementation.

## 6. Database Maintenance

The production database uses MySQL.

Core tables include:

- users
- resources
- reservations
- check_ins
- notifications

Database maintenance should include:

- regular backups where supported;
- monitoring database availability;
- checking data integrity;
- reviewing schema changes before deployment;
- testing database-related changes before production release.

## 7. Security Maintenance

Security maintenance includes:

- protecting environment variables and credentials;
- rotating credentials when necessary;
- reviewing authentication and authorization;
- keeping dependencies updated;
- avoiding secrets in Git;
- maintaining HTTPS for production communication;
- reviewing administrator access.

## 8. Deployment Maintenance

Production components:

- Vercel — frontend hosting
- Render — Flask backend hosting
- Aiven — MySQL hosting

Deployment changes should be verified through:

1. GitHub Actions.
2. Backend health endpoint.
3. Frontend availability.
4. Authentication.
5. Core reservation workflow.

## 9. Troubleshooting Guide

### Backend unavailable

Check:

- Render service status;
- application logs;
- /api/health;
- database connectivity;
- environment variables.

### Frontend cannot reach API

Check:

- frontend API environment variable;
- Render backend availability;
- browser network errors;
- CORS configuration.

### Authentication failure

Check:

- email and password;
- backend availability;
- JWT configuration;
- user account and role.

### Reservation failure

Check:

- resource availability;
- authenticated user;
- reservation request;
- database connectivity;
- backend logs.

## 10. Handover Checklist

A future maintainer should receive:

- source repository;
- database schema;
- API documentation;
- architecture documentation;
- UML documentation;
- user manual;
- QA documentation;
- CI configuration;
- deployment documentation;
- maintenance plan;
- release/version information.

## 11. Important Project Constraints

Future maintenance should preserve the current scope unless formally changed.

Do not introduce:

- microservices;
- native Flutter application requirements;
- unsupported notification channels;
- unimplemented QR camera scanning;
- unnecessary architectural replacement.

The implemented student application is a React/Vite responsive web application.

## 12. Current Release

Release:

v1.0.0

Git tag:

v1.0.0

The release represents the current production-ready academic implementation.

## 13. Handover Status

| Handover Item | Status |
|---|---|
| Source code | Complete |
| Database schema | Complete |
| API documentation | Complete |
| Architecture documentation | Complete |
| UML documentation | Complete |
| User manual | Complete |
| QA documentation | Complete |
| CI/CD configuration | Complete |
| Deployment documentation | Complete |
| Release plan | Complete |
| Maintenance plan | Complete |
| Version tag | v1.0.0 |

## 14. Handover Conclusion

CampusReserve has documented the technical information required for continued maintenance, testing, deployment and future enhancement.

The repository and documentation should be treated as the authoritative implementation reference for the v1.0.0 release.
