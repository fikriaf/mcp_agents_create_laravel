# GenLaravel Backend - Dockerfile for Railway
# Python FastAPI with WebSocket support

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agents/ ./agents/
COPY utils/ ./utils/
COPY backend/ ./backend/

# Create necessary directories
RUN mkdir -p output history my-laravel/resources/views/components \
    my-laravel/resources/views/layouts my-laravel/routes

# Create default Laravel routes file
RUN printf '<?php\n\nuse Illuminate\\Support\\Facades\\Route;\n\nRoute::get("/", function () {\n    return view("welcome");\n});\n' > my-laravel/routes/web.php

# Expose port (Railway uses $PORT)
EXPOSE 8080

# No HEALTHCHECK - let Railway handle it via /health endpoint

# Run the application with dynamic port from Railway
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8080}
