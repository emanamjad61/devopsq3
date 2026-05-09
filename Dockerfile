ARG SELENIUM_PLATFORM=linux/amd64
FROM --platform=$SELENIUM_PLATFORM selenium/standalone-chrome:latest

USER root

# Install Python and clean up
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install in venv
COPY requirements.txt .
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the app directory
COPY app ./app

# Set environment variables
ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1

EXPOSE 7000

# Switch back to selenium user for security
USER seluser
ENTRYPOINT []
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7000"]

