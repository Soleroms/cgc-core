# Multi-stage build: Node.js for frontend, Python for backend
FROM node:20-slim AS frontend

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy source
COPY . .

# Build frontend
RUN npm run build

# Python stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python requirements
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages || \
    pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Copy built frontend from previous stage
COPY --from=frontend /app/dist ./dist

# Expose port
EXPOSE 8000

# Start Python server
CMD ["python3", "api_server_full.py"]