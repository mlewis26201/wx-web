# Common Dockerfile for all wx-web-* services
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY wx-web-backend/ ./wx-web-backend/
COPY wx-web-frontend/ ./wx-web-frontend/
COPY wx-web-graph-generator/ ./wx-web-graph-generator/
COPY wx-web-explorer/ ./wx-web-explorer/
COPY wx-web-alerter/ ./wx-web-alerter/
COPY wx-web-utils/ ./wx-web-utils/
# Copy shared static and template assets if needed
COPY data/static/ ./data/static/
CMD ["python", "-u", "app.py"]
