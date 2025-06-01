# wx-web: Modern Weather Dashboard

A modern, containerized weather dashboard for real-time data, graphs, alerts, and exploration.

## Features
- Modular, multi-container architecture (backend, frontend, graph generator, explorer, alerter)
- Real-time weather data ingestion and storage
- Interactive web dashboard with graphs and data explorer
- Customizable alerts with Pushover integration
- Secure configuration using Docker secrets or manual volume mounts
- Easy deployment with Docker Compose
- All containers run as the invoking user for safe file permissions
- Single unified Dockerfile for all services

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

## Configuration with Docker Secrets (Important Note)
- **Docker Compose secrets (the `/run/secrets/...` mount) only work natively with Docker Swarm.**
- For regular Docker Compose (non-Swarm), you must mount secrets files manually as volumes:
  ```yaml
  volumes:
    - ./wx-web-frontend.secrets:/run/secrets/wx-web-frontend.secrets:ro
  ```
- The `secrets:` section in `docker-compose.yml` is ignored unless you are using Swarm mode.
- This project is set up to use manual volume mounts for secrets by default for maximum compatibility.

Example secrets files:
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

> **Note:** By default, secrets files must be present in the directory where you run `docker compose`. You can use absolute or relative paths in the `volumes:` section if you want to store them elsewhere.

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
- Only one Dockerfile (in the project root) is used for all services. All other Dockerfiles have been removed.

## Integrated Web Stats with GoAccess

### Overview
- GoAccess is now integrated as a service (`wx-web-goaccess`) in the main `docker-compose.yml`.
- It processes nginx access logs and generates real-time HTML reports.
- Reports are available at `/webstats/` via the main nginx reverse proxy.

### How it Works
- The GoAccess container reads logs from `./logs/nginx` and writes reports to `./webstats`.
- The nginx container serves the reports at `http://localhost:8099/webstats/`.
- Both containers share the log and report directories via bind mounts.

### GoAccess Service Details
- **Dockerfile:** `goaccess.Dockerfile`
- **Service name:** `wx-web-goaccess`
- **Volumes:**
  - `./logs/nginx:/logs` (read nginx logs)
  - `./webstats:/webstats` (write HTML reports)
- **Depends on:** nginx (starts after nginx is up)

### Usage
- No manual steps are needed; GoAccess starts automatically with the rest of the stack.
- To view web stats, visit: [http://localhost:8099/webstats/](http://localhost:8099/webstats/)
- If you want to reset stats, you can clear the `./logs/nginx/access.log` and `./webstats/` directory.

### Troubleshooting
- If you do not see stats, ensure:
  - Nginx is writing logs to `./logs/nginx/access.log`.
  - The GoAccess container is running (`docker compose ps`).
  - Permissions on `logs/nginx` and `webstats` allow UID/GID 1002 to read/write.
- To manually rebuild GoAccess reports:
  ```bash
  docker compose restart wx-web-goaccess
  ```

### Example GoAccess Command (in container)
```
goaccess /logs/access.log -o /webstats/report.html --log-format=COMBINED --real-time-html --ws-url=ws://localhost:7890 --daemonize
```

## Git & Workflow Tips
- The SQLite database (`/data/weather.db`) is excluded from git tracking via `.gitignore`.
- For safe collaboration, use feature branches and avoid force-pushes unless rewriting history is required.

## License
MIT
