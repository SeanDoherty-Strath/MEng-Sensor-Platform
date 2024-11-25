# Use a base Python image
FROM python:3.12.7-slim

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Define the default command
CMD ["python", "main.py"]
