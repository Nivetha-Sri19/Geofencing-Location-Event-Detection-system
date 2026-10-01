Geofencing & Location Event Detection System

Overview

The Geofencing & Location Event Detection System is a full-stack location monitoring platform designed to detect and manage device movement across defined geographic boundaries.

I built the system with a clear separation between the backend, geofencing engine, database layer, and frontend. The application supports device management, geofence management, GPS location processing, transition detection, event history, audit logging, authentication, and role-based access control.

The system supports circular and polygon geofences while keeping geographic calculations separate from event-transition logic.


Key Features

- JWT authentication and role-based access control

- Device registration and management

- Circular and polygon geofence management

- Configurable GPS boundary tolerance

- Haversine distance calculation

- Point-in-polygon detection

- Enter, exit, inside, and outside event detection

- Persistent device/geofence state tracking

- Duplicate and out-of-order location handling

- Multi-geofence evaluation

- Location and geofence event history

- Audit logging

- Pagination and filtering

- Centralized exception handling

- Request validation

- Database constraints, relationships, and indexes

- Swagger/OpenAPI documentation

- Docker and Docker Compose support

- Backend testing

- React dashboard

- Leaflet/OpenStreetMap visualization

- Device, geofence, location, event, user, and audit management

Technology Stack

Backend

- Python 3.12

- FastAPI

- SQLAlchemy 2.x

- Pydantic v2

- MySQL 8

- Alembic

- JWT authentication

- Redis

- Docker

- Docker Compose

Frontend

- React

- TypeScript

- Vite

- Material UI

- Axios

- React Router

- Leaflet

- OpenStreetMap

Development Tools

- Visual Studio Code

- MySQL Workbench

- Postman

- Swagger/OpenAPI

- Docker Desktop


- Git

Architecture

The project follows a layered architecture that separates API handling, business logic, database operations, geographic calculations, and presentation.


geofencing-system/

├── backend/

│   ├── app/

│   │   ├── api/

│   │   │   └── v1/

│   │   │       └── endpoints/

│   │   ├── core/

│   │   ├── models/

│   │   ├── schemas/

│   │   ├── repositories/

│   │   ├── services/

│   │   ├── geofencing/

│   │   │   ├── engine.py

│   │   │   ├── circle.py

│   │   │   ├── polygon.py

│   │   │   └── tolerance.py

│   │   ├── dependencies/


│   │   ├── middleware/

│   │   └── main.py

│   ├── alembic/

│   ├── tests/

│   ├── requirements.txt

│   ├── Dockerfile

│   └── .env.example

├── frontend/

│   ├── src/

│   │   ├── api/

│   │   ├── components/

│   │   ├── features/

│   │   ├── hooks/

│   │   ├── layouts/

│   │   ├── pages/


│   │   ├── routes/

│   │   ├── types/

│   │   ├── utils/

│   │   └── main.tsx

│   ├── Dockerfile

│   └── package.json

├── postman/

├── docker-compose.yml

├── README.md

└── .gitignore


Backend

The backend uses FastAPI with a layered structure.

API Layer

The API layer exposes versioned FastAPI routes and handles HTTP requests, authentication dependencies, request validation, and response serialization.

Schema Layer

Pydantic schemas define request and response structures and validate incoming data before it reaches the business layer.

Repository Layer

Repositories isolate database operations from application logic and keep SQLAlchemy-specific operations separated from services.

Service Layer

Services contain application-level business rules for authentication, devices, geofences, location processing, events, and auditing.

Geofencing Layer

The geofencing package contains the geographic calculations and the transition engine. Circular and polygon calculations are maintained separately from the state-transition logic.

Database Layer

SQLAlchemy manages the database models and asynchronous sessions, while Alembic manages schema migrations.

Geofencing Engine

The geofencing engine evaluates every incoming GPS location against active geofences.

Circular geofences are evaluated using geographic distance calculations. Polygon geofences are evaluated using point-in-polygon logic.

Boundary tolerance is applied to account for normal GPS accuracy variation around a geofence boundary.

Geographic evaluation is kept separate from transition detection. The engine first determines the geographic state and then compares it with the previous stored state.

Event Detection

The application maintains the previous state of each device relative to each geofence.

This persistent state allows the system to distinguish a new transition from repeated GPS readings while a device remains in the same area.

Supported event states include:

- ENTER

- EXIT

- INSIDE

- OUTSIDE

Duplicate location submissions and out-of-order timestamps are handled so that event processing remains consistent.

The processing flow is:

GPS Location

     ↓

Request Validation

     ↓

Location Persistence

     ↓

Active Geofence Evaluation

     ↓

Geographic State Detection

     ↓

Previous State Lookup

     ↓


Transition Detection

     ↓

State Update

     ↓

Geofence Event Creation

     ↓

Audit / History

Database Design

The main database entities are:

Users

Stores users, authentication information, and application roles.

Devices

Stores registered devices, identifiers, names, types, ownership information, and active status.

Geofences

Stores geofence configuration, type, center or boundary information, tolerance, event rules, and active status.

Geofence Points

Stores polygon boundary coordinates associated with polygon geofences.

Location Events

Stores incoming device GPS readings and timestamps.

Geofence Events

Stores generated transitions between devices and geofences.

Device Geofence States

Stores the latest known state of each device relative to each geofence and prevents repeated transition generation.

Audit Logs

Stores important application actions for traceability and operational auditing.

Foreign keys, indexes, constraints, and relationships are used to maintain data integrity.

Authentication and Authorization

Authentication is implemented using JWT access tokens.

Protected frontend requests include the access token through a centralized Axios interceptor.

The backend validates the token and applies role-based authorization to protected operations.

Administrative operations are restricted according to the authenticated user's role.

Passwords are stored using secure password hashing rather than plain text.

Frontend

The frontend is built with React and TypeScript and organized into reusable components, pages, hooks, API modules, layouts, routes, and shared types.

Main application areas include:

- Authentication

- Dashboard

- Devices

- Geofences

- Location processing

- Events and history

- User management

- Audit logs


Application configuration is centralized through Pydantic Settings.

Environment-specific values include:

- Database connection

- JWT secret


- CORS origins

- Application environment

- Bootstrap administrator configuration

- Authentication settings

Sensitive configuration values should be replaced with secure deployment-specific values.

Database Migrations

Alembic manages database schema changes.

Migrations keep the database schema synchronized with the SQLAlchemy models and provide a controlled process for future schema updates.

Testing

The backend test suite covers important application behavior, including:

- Authentication

- Device operations

- Geofence operations

- Circular geofence calculations

- Polygon calculations

- Boundary tolerance

- Location processing

- Enter and exit transitions

- Persistent device/geofence state

- Duplicate location handling

- Out-of-order location handling

- Validation behavior

- Geographic boundary conditions

Running the Application

The backend can be started through Docker Compose and exposes the FastAPI service on port 8000.

The frontend uses Vite during local development and runs on port 5173.

The frontend communicates with the versioned FastAPI backend through a centralized Axios client.

Swagger/OpenAPI documentation is available through the FastAPI documentation interface.

Development Flow

Start MySQL

     ↓

Apply Alembic migrations

     ↓


Start FastAPI backend

     ↓

Start React frontend

     ↓

Authenticate

     ↓

Manage devices

     ↓

Manage geofences

     ↓

Process GPS locations

     ↓

Detect transitions

     ↓

Review events and history

     ↓

Review audit information

Security

The application includes:

- JWT authentication

- Password hashing

- Role-based authorization

- Protected API resources

- Input validation

- Database constraints

- Transaction rollback

- Configurable CORS

- Centralized error handling

- Audit logging

Production deployments should use strong secrets, HTTPS, restricted CORS origins, and secure database credentials.

Project Outcome

The completed system provides an end-to-end geofencing workflow from device and boundary management through GPS processing, geographic evaluation, state tracking, event generation, persistence, and frontend visualization.

The separation between geographic calculations, transition rules, database operations, API handling, and presentation makes the system easier to maintain, test, and extend.
