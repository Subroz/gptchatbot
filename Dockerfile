FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY telegram_ai_bot.py .
COPY .env .

# Create volume for persistent data
VOLUME ["/app/data"]

# Set environment variable to use volume for data
ENV DATA_DIR=/app/data

# Run the bot
CMD ["python", "-u", "telegram_ai_bot.py"]
