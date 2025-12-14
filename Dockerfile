FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install system deps needed by mysqlclient
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config \
        curl \
        git \
        libssl-dev \
        libffi-dev \
        netcat-openbsd \
        && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Fix line endings and make wait-for-db executable
RUN sed -i 's/\r$//' /app/wait-for-db.sh && chmod +x /app/wait-for-db.sh

# Expose Django port
EXPOSE 8000

# Default command (overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
