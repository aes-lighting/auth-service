FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Expose port (Railway will override via PORT env var)
EXPOSE 5000

# Run gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]
