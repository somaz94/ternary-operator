FROM python:3.14-slim

# Set the working directory inside the container
WORKDIR /usr/src

# Copy the Python script
COPY entrypoint.py .

# Configure the container to be run as an executable
ENTRYPOINT ["python", "/usr/src/entrypoint.py"]