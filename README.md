# wx-web: Modern Weather Dashboard

A modern, containerized weather dashboard for real-time data, graphs, and exploration.

## Features
- Modular, multi-container architecture (backend, frontend, graph generator, explorer)
- Real-time weather data ingestion and storage
- Interactive web dashboard with graphs and data explorer
- Easy deployment with Docker Compose

## Directory Structure
- `wx-web-backend/` — MQTT ingestion and database service
- `wx-web-frontend/` — Flask web dashboard
- `wx-web-graph-generator/` — Automated graph/image generation
- `wx-web-explorer/` — Data explorer web app
- `wx-web-utils/` — Utility scripts (import, setup)
- `data/` — Persistent data (SQLite DB, static assets, generated graphs)

## Quick Start
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd wx-web
   ```
2. Build and start all services:
   ```bash
   docker compose up --build
   ```
3. Access the dashboard at [http://localhost:8080](http://localhost:8080)

## Data Directory Path
- By default, all containers mount `./data` as the persistent data directory.
- **You can update the path in `docker-compose.yml` to a full path (e.g., `/docker_data/wx-web/data`) to help manage application data outside the project directory.**
- Example:
  ```yaml
  volumes:
    - /your/absolute/path/data:/data:rw
  ```

## Git & Workflow Tips
- The SQLite database (`/data/weather.db`) is excluded from git tracking via `.gitignore`.
- For safe collaboration, use feature branches and avoid force-pushes unless rewriting history is required.

## License
MIT
