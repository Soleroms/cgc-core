# Frontend build
FROM node:18-alpine AS frontend
WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . .
RUN npm run build

# Backend
FROM python:3.11-slim

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Python backend
FROM python:3.11-slim

WORKDIR /app

# Instalar utilidades necesarias
RUN apt-get update && apt-get install -y curl procps \
    && rm -rf /var/lib/apt/lists/*

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Python backend
COPY api_server_full.py .
COPY auth_system.py .
COPY database.py .
COPY config.py .
COPY logging_config.py .




COPY api_server_full.py .
COPY auth_system.py .
COPY database.py .
COPY config.py .
COPY logging_config.py .

# CGC CORE™
COPY cgc_core/ ./cgc_core/

# DiscipleAI Legal™
COPY discipleai_legal/ ./discipleai_legal/

# Frontend
COPY --from=frontend /app/dist ./dist

# Directories
RUN mkdir -p data logs

EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8080/api/health || exit 1

ENTRYPOINT ["python", "api_server_full.py"]