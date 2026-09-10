# Design Patterns and Architectural Styles

## 1. Flask Application Factory Pattern

CampusReserve implements the Flask Application Factory pattern through create_app() in:

ackend/app/__init__.py

The factory:

- creates the Flask application;
- loads configuration;
- initializes SQLAlchemy;
- initializes JWT;
- configures CORS;
- registers Flask blueprints;
- allows separate test configuration.

The same factory is used by the running application and automated tests.

This improves testability, configuration management, maintainability, and separation between application creation and application execution.

## 2. Flask Blueprint Modularization

API routes are organized into Flask Blueprints:

- pp/routes/health.py
- pp/routes/auth.py
- pp/routes/resource.py
- pp/routes/reservation.py
- pp/routes/check_in.py
- pp/routes/admin.py

This separates functional areas and reduces coupling between route modules.

Blueprints are documented as a Flask modularization mechanism, not as a GoF design pattern.

## 3. Architectural Styles

### Client-Server

The system consists of:

React/Vite Student Client → Flask REST API → MySQL

and

React/Vite Admin Client → Flask REST API → MySQL

### Layered Architecture

The system separates:

- presentation;
- API/routes;
- application/authentication logic;
- data models;
- database persistence.

### REST-style API

The backend exposes HTTP endpoints under /api using:

- GET
- POST
- PUT
- DELETE

## 4. Patterns Not Claimed

The project does not claim implementation of the following GoF patterns unless directly represented in the source code:

- Observer
- Strategy
- Singleton
- Factory Method

The Flask Application Factory is specifically a Flask application pattern and is not presented as the GoF Factory Method pattern.

## 5. Traceability

| Pattern / Style | Implementation Evidence | Purpose |
|---|---|---|
| Application Factory | ackend/app/__init__.py | Application creation and testability |
| Flask Blueprints | ackend/app/routes/ | Modular API organization |
| Client-Server | React/Vite clients + Flask API | Client/server separation |
| Layered Architecture | Frontend → API → persistence | Separation of responsibilities |
| REST | /api/* endpoints | HTTP-based resource interaction |

## 6. Conclusion

CampusReserve uses a client-server, layered REST architecture with Flask Application Factory and Blueprint modularization.

Only patterns and architectural styles supported by the implemented system are claimed.
