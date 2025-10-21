# Use official slim Python image
FROM python:3.13-slim

# Set environment variables to avoid buffering and bytecode files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies needed for building wheels and SSL
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy only requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the app and model
COPY app ./app
COPY static ./static
COPY spam_classifier.pkl .

# Expose port
EXPOSE 8000

# Run FastAPI app using uvicorn with reload disabled for production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
