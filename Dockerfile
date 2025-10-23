# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system deps required by some Python packages and for Playwright to work (optional)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libnss3 \
       libatk1.0-0 \
       libatk-bridge2.0-0 \
       libcups2 \
       libxkbcommon0 \
       libx11-xcb1 \
       libxcomposite1 \
       libxdamage1 \
       libxrandr2 \
       libgbm1 \
       libpango-1.0-0 \
       libpangocairo-1.0-0 \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Default environment variables
ENV PORT=8000

# Use a simple entrypoint to run the Flask app. In production, you might prefer gunicorn.
CMD ["python", "app.py"]