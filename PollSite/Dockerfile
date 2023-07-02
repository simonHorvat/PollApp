# Official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 8000

# Set the command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]