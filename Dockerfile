# Use an official Python image as base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app/Backend
# Copy the contents of the GitHub repo into the container
COPY Backend/requirements.txt .

# Install dependencies if requirements.txt exists
RUN pip install --no-cache-dir -r requirements.txt

COPY Backend .
# Expose the application port (Change based on your app)
EXPOSE 5000

# Define the command to run your application (Modify accordingly)
CMD ["python", "app.py"]
