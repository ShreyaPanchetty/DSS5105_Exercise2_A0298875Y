# Use lightweight Python image
FROM python:3.10

# Set working directory in container
WORKDIR /app

# Copy all files in your project directory to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (optional)
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
CMD [curl "http://localhost:5000/predict?W=1&X=20"]
CMD [curl "http://localhost:5000/ate"]
