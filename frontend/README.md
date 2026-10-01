# Geofencing & Location Event Detection — Pastel Frontend

A production-style React + TypeScript frontend connected to the existing FastAPI geofencing backend.

## What is included

- Pastel responsive dashboard
- JWT login and live `/auth/me` session
- Role-aware navigation for admin, operator and viewer
- Live device management
- Geofence creation, editing, activation and deletion
- Circle and polygon geofences
- Event-rule configuration
- Live Leaflet/OpenStreetMap map using backend geofences and current locations
- Location event history with filters
- Administrator user role/status management
- Live backend error handling and refresh actions
- TypeScript API types matching the backend schemas

## Backend connection

The frontend does **not** use fake or hardcoded operational data. It calls the running FastAPI backend for users, devices, geofences, locations, events and administration.

Default API:

`http://localhost:8000/api/v1`

Set another API URL in `.env`:

`VITE_API_BASE_URL=http://localhost:8000/api/v1`

## Run

```bash
npm install
npm run dev
```

Open `http://localhost:5173`.

The backend CORS configuration already allows `http://localhost:5173`.

## Production build

```bash
npm run build
npm run preview
```

## Backend workflow supported by this UI

Login → create devices → create circle/polygon geofences → submit locations through the backend location processing endpoint → observe ENTER / INSIDE / EXIT / OUTSIDE events → inspect live locations and event history.

## Main screens

Dashboard, Devices, Geofences, Process Location, Live Map, Events & History, Users (admin) and Audit Logs (admin).
