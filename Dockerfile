# ============================
# Stage 1: Build dependencies
# ============================
FROM python:3.12-slim AS builder

# Environment variables for clean Python environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ============================
# Stage 2: Production image
# ============================
FROM python:3.12-slim AS production

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Work directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY . .

# Create static and media directories
RUN mkdir -p /app/vol/static /app/vol/media
RUN chmod +x ./start.sh

# Expose Gunicorn port
EXPOSE 8112

# Keep root user (default)
USER root

# Start the Django app
CMD ["./start.sh"]
