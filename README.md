# wx-web: Modern Weather Dashboard

A modern, containerized weather dashboard for real-time data, graphs, alerts, and exploration.

## Features
- Modular, multi-container architecture (backend, frontend, graph generator, explorer, alerter)
- Real-time weather data ingestion and storage
- Interactive web dashboard with graphs and data explorer
- Customizable alerts with Pushover integration
- Secure configuration using Docker secrets
- Easy deployment with Docker Compose
- Containers run as the invoking user for safe file permissions

## Directory Structure
- `wx-web-backend/` — MQTT ingestion and database service
- `wx-web-frontend/` — Flask web dashboard
- `wx-web-graph-generator/` — Automated graph/image generation
- `wx-web-explorer/` — Data explorer web app
- `wx-web-alerter/` — Alerting service with Pushover integration
- `wx-web-utils/` — Utility scripts (import, setup)
- `data/` — Persistent data (SQLite DB, static assets, generated graphs)

## Quick Start
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd wx-web
   ```
2. Create and edit the secrets files as needed (see below).
3. Build and start all services (ensure you pass your UID/GID for correct file permissions):
   ```bash
   docker compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g)
   docker compose up
   ```
4. Access the dashboard at [http://localhost:8099](http://localhost:8099) (or your configured port)

## Configuration with Docker Secrets
All sensitive and user-editable settings are managed via Docker secrets files. Example secrets files:

- `wx-web-backend.secrets` (for MQTT settings):
  ```
  MQTT_BROKER_HOST=mqtt.local
  MQTT_BROKER_PORT=1883
  MQTT_BROKER_USER=mqtt
  MQTT_BROKER_PASSWORD=YOUR_PASSWORD
  MQTT_TOPIC=weather/loop
  ```
- `wx-web-frontend.secrets` (for frontend settings):
  ```
  NOAA_Radar=KMVX
  FRONTEND_PORT=8099
  ```
- `wx-web-alerter.secrets` (for Pushover API):
  ```
  PUSHOVER_USER_KEY=your_user_key
  PUSHOVER_API_TOKEN=your_api_token
  ```

> **Note:** By default, secrets files must be present in the directory where you run `docker compose`. You can use absolute or relative paths in `docker-compose.yml` if you want to store them elsewhere.

## Data Directory Path
- By default, all containers mount `./data` as the persistent data directory.
- **You can update the path in `docker-compose.yml` to a full path (e.g., `/docker_data/wx-web/data`) to help manage application data outside the project directory.**
- Example:
  ```yaml
  volumes:
    - /your/absolute/path/data:/data:rw
  ```

## Security Notes
- All secrets files are excluded from git tracking via `.gitignore`.
- Docker secrets are only available to containers at runtime and are not exposed in images or environment variables.
- Never commit secrets or sensitive data to version control.

## Git & Workflow Tips
- The SQLite database (`/data/weather.db`) is excluded from git tracking via `.gitignore`.
- For safe collaboration, use feature branches and avoid force-pushes unless rewriting history is required.

## License
MIT
