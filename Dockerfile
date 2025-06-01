# Common Dockerfile for all wx-web-* services
FROM python:3.11-slim
WORKDIR /app
COPY wx-web-backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt matplotlib flask jinja2 paho-mqtt
COPY wx-web-backend/app/ wx-web-backend/app/
COPY wx-web-graph-generator/ wx-web-graph-generator/
COPY wx-web-frontend/ wx-web-frontend/
COPY wx-web-explorer/ wx-web-explorer/
COPY wx-web-utils/ wx-web-utils/
VOLUME ["/data"]
# The command will be overridden per service in docker-compose.yml
CMD ["python", "--version"]
