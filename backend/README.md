# Geofencing & Location Event Detection System — Backend

Enterprise-style FastAPI backend for creating circular and polygon geofences, receiving device locations, calculating geofence state, and recording enter/exit/inside/outside events.

## Stack
Python 3.12, FastAPI, SQLAlchemy 2.x, MySQL 8, Alembic, Pydantic v2, JWT, Argon2 password hashing, pytest, Docker.

## Architecture
The backend uses a fixed layered architecture: API endpoints → services → repositories/database, with a dedicated geofencing engine for geographic calculations. Models and schemas are separated so persistence and API contracts do not leak into each other.

## Main modules
- `app/api`: versioned HTTP endpoints.
- `app/core`: configuration, database, security and exceptions.
- `app/models`: SQLAlchemy persistence models.
- `app/schemas`: validated API request/response contracts.
- `app/repositories`: database access for reusable persistence operations.
- `app/services`: business workflows and transactions.
- `app/geofencing`: Haversine circle detection, polygon point-in-polygon and boundary tolerance.
- `tests`: geographic and validation unit tests.
- `alembic`: database migrations.
- `postman`: API collection.

## Data model
The database contains users, devices, geofences, ordered geofence points, location events, geofence events, device/geofence state, and audit logs. `device_geofence_states` stores the latest state for every device/geofence pair so transitions can be detected without replaying the entire event history.

## Security
JWT bearer authentication is used for protected endpoints. Passwords are stored as Argon2 hashes. Roles are `admin`, `operator`, and `viewer`. Administrators can manage users and create/update/delete geofences. Operators can create and modify geofences. Device access is restricted to the owning user unless the caller is an administrator.

A development administrator can be bootstrapped from environment variables. Change the default password before using the system outside local development.

## Geofencing behavior
Circle detection uses the Haversine distance between the reported location and the configured center. Polygon detection uses a point-in-polygon test and an optional boundary tolerance measured in meters. Latitude and longitude are validated by Pydantic before business processing.

For each active geofence, the engine compares the new state with the persisted previous state. `outside → inside` creates ENTER, `inside → outside` creates EXIT, and unchanged states produce INSIDE or OUTSIDE when the corresponding event rule is enabled. Exact duplicate location submissions are rejected and older timestamps are rejected to prevent state rollback.

## Run with Docker
1. Copy `.env.example` to `.env` and change the secrets/passwords.
2. Run `docker compose up --build`.
3. The backend starts on port 8000 and applies the Alembic migration automatically.
4. Swagger UI is available at `/docs`; ReDoc is available at `/redoc`.

## Local run
Create a Python 3.12 virtual environment, install `requirements.txt`, configure a reachable MySQL database in `.env`, then run `alembic upgrade head` followed by `uvicorn app.main:app --reload`.

## Testing
Run `pytest`. The included unit tests cover circle center/boundary/tolerance behavior, polygon inside/outside/edge/tolerance behavior, event transitions, and coordinate/geofence validation.

## Operational notes
The service rejects out-of-range coordinates, duplicate location payloads, and out-of-order timestamps. State rows are locked during event processing to reduce concurrent transition races. Database indexes support device/time and device/geofence event lookups. Geofences are evaluated independently, so overlapping geofences can generate separate events for the same location.

The current implementation deliberately keeps geographic calculations in the application layer so the database remains MySQL-compatible and does not require vendor-specific spatial extensions.
