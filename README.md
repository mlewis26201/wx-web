# Weather Dashboard System

A modern, minimal weather dashboard system that ingests MQTT weather data into SQLite, generates scheduled graphs, and provides a sleek web frontend. The system is fully containerized and headless except for the web UI.

## Features
- **MQTT Ingestion:** Subscribes to a configurable MQTT topic and broker, writing all weather data to SQLite (`weather_history` table).
- **Dynamic Schema:** Automatically adds new columns as new fields appear in MQTT messages.
- **Graph Generation:** Scheduled generation of temperature, humidity, wind (spider/vector), solar, rain, pressure, and "feels-like" graphs for multiple time intervals. Graphs are saved to `/data/static`.
- **Modern Web Frontend:**
  - Dashboard UI with cards for outside/inside temperature, solar, pressure, and humidity.
  - Each card shows the latest value and average values for the last 1 and 24 hours (smaller, lighter font).
  - Dark/light theme toggle.
  - Direct SQLite access for fast, up-to-date data.
  - `/api/latest` and `/api/averages` endpoints for frontend data.
- **Dockerized:** All components (MQTT-to-DB, graph generator, frontend, explorer) run as containers, orchestrated via `docker-compose`.
- **NOAA Radar Card:** Displays a live radar loop from the configured NOAA station (default: KMVX). Change the station by setting the `NOAA_Radar` environment variable in your compose file.
- **Branching Workflow:** Use `git checkout -b <branch>` to safely develop and test features without affecting the main branch. The `data/` directory is excluded from git.

## Usage

### 1. Build and Run with Docker Compose

```bash
docker-compose up --build
```

- The MQTT-to-DB service will subscribe to the MQTT topic and write all weather data to `data/weather.db`.
- The graph generator will periodically update graphs in `data/static/`.
- The web frontend will be available at [http://localhost:8080](http://localhost:8080).
- The explorer will be available at [http://localhost:8081](http://localhost:8081).

### 2. Start Fresh (Optional)
To reset the database, simply delete the file and restart the containers:
```bash
rm -f data/weather.db
docker-compose restart wx-web-backend wx-web-graph-generator wx-web-frontend wx-web-explorer
```

## Configuration
All configuration is via environment variables (see `docker-compose.yml`):
- `MQTT_BROKER_HOST` (default: mqtt.local)
- `MQTT_BROKER_PORT` (default: 1883)
- `MQTT_BROKER_USER` (optional)
- `MQTT_BROKER_PASSWORD` (optional)
- `MQTT_TOPIC` (default: weather/loop)
- `SQLITE_PATH` (default: /data/weather.db)
- `NOAA_Radar`: Set this environment variable in the `wx-web-frontend` service in `docker-compose.yml` to configure which NOAA radar station is displayed in the radar card. Example:

```
services:
  wx-web-frontend:
    ...
    environment:
      - NOAA_Radar=KMVX  # Change KMVX to your desired station code
```

## Directory Structure
- `wx-web-backend/`: MQTT-to-SQLite ingestion service
- `wx-web-graph-generator/`: Scheduled graph generation
- `wx-web-frontend/`: Flask web frontend (dashboard UI, API, static, templates)
- `wx-web-explorer/`: Data explorer web app
- `wx-web-utils/`: Utility scripts
- `Dockerfile`: Common Docker build for all components
- `docker-compose.yml`: Multi-service deployment
- `data/`: Persistent SQLite database and generated graphs (excluded from git)

## API Endpoints
- `/api/latest`: Latest weather data (rounded, for dashboard)
- `/api/averages`: 1h and 24h averages for all dashboard metrics

## Branching Workflow
To create a new branch for development/testing:
```bash
git checkout main
git pull
git checkout -b my-feature-branch
```
Replace `my-feature-branch` with your branch name. Work and commit on this branch. When ready, merge it back into main. The `data/` directory is excluded from git by `.gitignore`.

## Example Usage
To change the radar station, edit your `docker-compose.yml`:

```
services:
  wx-web-frontend:
    ...
    environment:
      - NOAA_Radar=KXYZ  # Replace KXYZ with your preferred NOAA radar station code
```

Then rebuild and restart the frontend:

```
docker compose build --no-cache wx-web-frontend
docker compose up -d wx-web-frontend
```

The dashboard will now show the radar loop for your selected station.

## License
MIT
