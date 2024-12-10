FROM alpine:3.21

# Install necessary packages
RUN apk add --no-cache \
    git=2.47.1-r0 \
    bash=5.2.37-r0

# Set the working directory inside the container
WORKDIR /usr/src

# Copy any source file(s) required for the action
COPY entrypoint.sh .

# Configure the container to be run as an executable
ENTRYPOINT ["/usr/src/entrypoint.sh"]

# FROM python:3.9-alpine

# # Set the working directory inside the container
# WORKDIR /usr/src

# # Copy the Python script
# COPY entrypoint.py .

# # Configure the container to be run as an executable
# ENTRYPOINT ["python", "/usr/src/entrypoint.py"]