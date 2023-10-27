# Use the official Python base image
FROM python:3.9-slim

# Install system packages required by Flask, the dev environment, and Git
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /workspace
WORKDIR /workspace

# Create a non-root user to run our application
RUN useradd -m vscode

# Switching to the new user
USER vscode

# Expose the Flask default port
EXPOSE 5000

# Set up the entry point
CMD [ "bash" ]
