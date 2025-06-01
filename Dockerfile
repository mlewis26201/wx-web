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
COPY data/static/ ./data/static/

# Add a non-root user matching the host UID/GID
ARG HOST_UID=1002
ARG HOST_GID=1002
RUN groupadd -g $HOST_GID appuser && \
    useradd -m -u $HOST_UID -g $HOST_GID appuser

USER appuser
CMD ["python", "-u", "app.py"]
