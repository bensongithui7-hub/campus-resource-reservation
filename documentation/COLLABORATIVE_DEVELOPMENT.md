# Collaborative Development, Team Roles and Code Review

> Current-state evidence for CampusReserve. Responsibility assignments describe the project structure and do not fabricate historical commits, pull requests, reviews, stand-ups, or individual contribution records.

## 1. Team

| Member | Registration Number | Assigned Responsibility |
|---|---|---|
| Felistus Mbinya Mutiso | SCCJ/05862P/2024 | Project Management, Requirements, Documentation and QA Coordination |
| Benson Githui | SCCJ/00627/2023 | Backend/API, Database Integration, Authentication and System Integration |
| Ogeto Francis | SCCJ/05678P/2025S | Frontend, UI Integration and User-Facing Functionality |

## 2. Responsibility Areas

### Felistus Mbinya Mutiso

- Project coordination
- Requirements and SRS
- Backlog and user-story coordination
- Documentation coordination
- QA/UAT coordination
- Project reporting

### Benson Githui

- Flask backend
- REST API
- Authentication and authorization
- SQLAlchemy/database integration
- Reservation processing
- Check-in processing
- Notification backend functionality
- Backend testing
- System integration
- Deployment/backend configuration

### Ogeto Francis

- React/Vite frontend development
- Student-facing interface
- Administrator-facing interface
- UI components and layouts
- Frontend/API integration
- Responsive web interface
- Frontend quality checks

## 3. Repository Structure

The main implementation areas are:

- backend/
- student-mobile/
- admin-web/
- database/
- documentation/
- .github/

The student-mobile directory contains the React/Vite responsive student web application. It is not a Flutter/Dart native application.

## 4. Version Control

The project is maintained using Git and hosted on GitHub.

Primary branch: master

The repository contains the implementation, tests, documentation and CI configuration.

## 5. Branching Strategy

For significant changes, the recommended workflow is:

master
  |
  +-- feature/<feature-name>
  |
  +-- fix/<issue-name>

Workflow:

1. Create a feature or fix branch.
2. Implement the change.
3. Test the change.
4. Review the change.
5. Merge into master.
6. Confirm automated CI checks.

Direct commits to master may be used for urgent maintenance or small documentation changes.

## 6. Code Review Checklist

Before integrating a significant change:

- [ ] Requirement is identified.
- [ ] Existing architecture is preserved.
- [ ] No unnecessary scope is introduced.
- [ ] Authentication and authorization remain correct.
- [ ] Database integrity is preserved.
- [ ] Error handling is appropriate.
- [ ] Existing functionality remains operational.
- [ ] Relevant tests pass.
- [ ] ESLint passes for frontend changes.
- [ ] Frontend production builds pass.
- [ ] Documentation is updated where necessary.
- [ ] No secrets or credentials are committed.

## 7. Quality Verification

| Check | Result |
|---|---|
| Backend Pytest | 112 passed |
| Backend coverage | 96% |
| Student frontend ESLint | Passed |
| Student frontend build | Passed |
| Admin frontend ESLint | Passed |
| Admin frontend build | Passed |
| Backend GitHub Actions | Passed |
| Frontend GitHub Actions | Passed |

## 8. Code Ownership Matrix

| Component | Primary Responsibility | Supporting Responsibility |
|---|---|---|
| Requirements / SRS | Felistus | Benson, Ogeto |
| Project Documentation | Felistus | Benson, Ogeto |
| QA / UAT Coordination | Felistus | Benson, Ogeto |
| Flask Backend | Benson | Felistus |
| REST API | Benson | Felistus |
| Authentication | Benson | Felistus |
| Database Integration | Benson | Felistus |
| Reservations | Benson | Ogeto |
| Check-in | Benson | Ogeto |
| Notifications | Benson | Ogeto |
| Student Frontend | Ogeto | Benson |
| Admin Frontend | Ogeto | Benson |
| Frontend/API Integration | Ogeto | Benson |
| Automated Backend Testing | Benson | Felistus |
| CI/CD | Benson | Ogeto |
| Deployment | Benson | Felistus, Ogeto |

## 9. Evidence Integrity

This document records the current team responsibility structure and development practices.

It does not claim that every listed responsibility was historically completed by the assigned member, and it does not fabricate historical pull requests, code reviews, stand-ups, commits or individual contribution records.

Where historical collaborative evidence is unavailable, the current responsibility structure is presented as current-state project evidence.
