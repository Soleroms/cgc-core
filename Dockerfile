# Stage 1: Build frontend with Node.js
FROM node:20-slim AS frontend

WORKDIR /app

# Install frontend dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy source code and build
COPY . .
RUN npm run build

# Stage 2: Backend with Python
FROM python:3.11-slim

WORKDIR /app

# Install backend dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages || \
    pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY api_server_full.py ./

# Copy compiled frontend
COPY --from=frontend /app/dist ./dist

# CORRECCIÓN CRÍTICA: Alineamos el puerto a 8000 para que coincida con la configuración del servidor Python
EXPOSE 8000

# Usamos 'python' para mayor compatibilidad en imágenes slim
CMD ["python", "api_server_full.py"]