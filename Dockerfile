# Use official slim Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and static folders, and the model
COPY app ./app
COPY static ./static
COPY spam_model.pkl .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
