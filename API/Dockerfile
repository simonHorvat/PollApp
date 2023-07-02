# Official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the entire API directory into the container
COPY . .

# Expose the API port
EXPOSE 5000

# Set the command to run when the container starts
CMD ["python", "run.py"]
