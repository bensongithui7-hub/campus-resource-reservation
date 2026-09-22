# CampusReserve

## Campus Smart Facility & Lab Equipment Reservation System

CampusReserve is a responsive web-based facility and equipment reservation system developed for the **IBL 3300 — Software Engineering Studio** course at the **Technical University of Kenya**.

The system allows students to browse available campus facilities and equipment, make and manage reservations, receive reservation notifications, and check in to confirmed reservations. Administrators can manage resources, users, reservations, and check-ins.

## Features

### Student
- Student registration and login
- Browse facilities and equipment
- Submit reservations
- View and cancel reservations
- Receive reservation notifications
- Check in to confirmed reservations using the implemented check-in/QR-token functionality

### Administrator
- Administrator login
- View and manage reservations
- Confirm or cancel reservations
- Manage facilities and equipment
- View registered users
- View check-in records

## Technology Stack

| Component | Technology |
|---|---|
| Student Frontend | React + Vite |
| Admin Frontend | React + Vite |
| Backend API | Python + Flask |
| Database | MySQL |
| Authentication | JWT |
| API Communication | REST API |
| Version Control | Git + GitHub |
| Backend Deployment Target | Render |
| Frontend Deployment Target | Vercel |

## System Architecture

```text
Student Web App ──┐
                  ├──> Flask REST API ──> MySQL Database
Admin Web App ────┘
```

The system uses separate React/Vite interfaces for students and administrators, with both communicating with the Flask REST API. The API manages authentication, reservations, resources, notifications, and check-ins while MySQL stores the application data.

## Project Structure

```text
campus-resource-reservation/
├── admin-web/          # Administrator React/Vite application
├── student-mobile/     # Student React/Vite responsive web application
├── backend/            # Flask REST API
├── database/           # Database scripts/schema
├── documentation/      # Project and QA/UAT documentation
└── .github/workflows/  # GitHub Actions CI workflows
```

## Running Locally

### Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m flask run
```

The backend runs by default at:

```text
http://127.0.0.1:5000
```

### Student Frontend

```powershell
cd student-mobile
npm install
npm run dev
```

### Admin Frontend

```powershell
cd admin-web
npm install
npm run dev
```

The frontend applications require the backend API to be running and configured with the appropriate API base URL.

## Testing

The project includes backend and frontend CI workflows using **GitHub Actions**. Backend testing uses `pytest` with coverage reporting, while frontend CI verifies the application build.

A detailed QA and UAT report is available in:

```text
documentation/QA_UAT_REPORT.md
```

## Documentation

Additional project documentation, UML diagrams, QA/UAT evidence, and other supporting materials are available in the `documentation/` directory.

## Team

**IBL 3300 — Software Engineering Studio**

Technical University of Kenya

- Benson Githui Muriithi
- Felistus Mbinya Mutiso
- Ogeto Francis

## Project Status

CampusReserve is a functional academic software engineering project with implemented student, administrator, reservation, resource management, notification, and check-in functionality.
