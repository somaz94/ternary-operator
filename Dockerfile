FROM alpine:3.21

RUN apk add --no-cache \
    git=2.45.2-r0 \
    bash=5.2.26-r0 

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