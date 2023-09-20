FROM python:3.9-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Upgrade pip and install necessary packages
RUN python -m pip install --upgrade pip \
    && apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
