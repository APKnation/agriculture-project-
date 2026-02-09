# Dockerfile for Django Backend
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (including curl for health check)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project
COPY . /app/

# Copy startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Create media directories
RUN mkdir -p /app/media/profile_images /app/media/crop_images

# Expose port
EXPOSE $PORT

# Health check (using Django endpoint)
HEALTHCHECK --interval=60s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:$PORT/health/ || exit 1

# Run the startup script
CMD ["/start.sh"]
