# Stage 1: Build frontend with Node.js
# Use a lightweight base image for the build process
FROM node:20-slim AS frontend

# Set working directory inside the container
WORKDIR /app

# Install frontend dependencies
# Copy package files first to leverage Docker layer caching
COPY package*.json ./
# Use --silent and --no-progress for cleaner output during install
RUN npm install --legacy-peer-deps --silent --no-progress

# Copy source code and build the frontend
COPY . .
RUN npm run build

# -----------------------------------------------------------------

# Stage 2: Backend with Python (Production Server)
# Use a specific, slim Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# 1. Install backend dependencies
# Copy requirements file first
COPY requirements.txt ./
# Install dependencies. The double command handles restrictive environments (like Canvas)
# by trying to install normally first, then without system path modification if needed.
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages || \
    pip install --no-cache-dir -r requirements.txt

# 2. Copy all backend source code.
# CRITICAL: This ensures internal modules like 'discipleai_legal' are copied and found by Python.
COPY . .

# 3. Copy the compiled frontend static files from the build stage
COPY --from=frontend /app/dist ./dist

# 4. Expose the port the Python server will listen on
EXPOSE 8000

# 5. Command to start the Python server
# Use 'python' for better compatibility in slim images
CMD ["python", "api_server_full.py"]