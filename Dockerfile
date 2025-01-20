# Use the official Python 3.12 image as a base
FROM python:3.10-slim

# Set environment variables to avoid Python buffering output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# Copy requirements.txt to the working directory
COPY requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory to the working directory

COPY resources ./resources
COPY src ./src
COPY . .
#COPY /src/process_bucket.py /process_bucket.py
# Specify the default command to run the process_bucket.py script
CMD ["python", "./run.py"]