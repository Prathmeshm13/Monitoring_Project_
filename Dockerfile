# Use an official Python image as base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the GitHub repo into the container
COPY . .

# Install dependencies if requirements.txt exists
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port (Change based on your app)
EXPOSE 5000

# Define the command to run your application (Modify accordingly)
CMD ["python", "app.py"]
