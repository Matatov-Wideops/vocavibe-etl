#!/bin/bash

# Define variables

CONTAINER_NAME="klt-vocapp-frhp"
REMOTE_FILE_PATH1="/data/.usershc.csv"
EC2_LOCAL_PATH1="/home/ec2-user/.usershc.csv"
LOCAL_FILE_PATH1="resources/usershc.csv"
REMOTE_FILE_PATH2="/data/.userspd.csv"
EC2_LOCAL_PATH2="/home/ec2-user/.userspd.csv"
LOCAL_FILE_PATH2="resources/userspd.csv"

# Log into AWS EC2 and copy the file from the Docker container to the EC2 instance's home directory

sudo docker cp $CONTAINER_NAME:$REMOTE_FILE_PATH1 $EC2_LOCAL_PATH1
sudo docker cp $CONTAINER_NAME:$REMOTE_FILE_PATH2 $EC2_LOCAL_PATH2


# Check if the SSH command was successful
if [ $? -eq 0 ]; then
  echo "File copied from container to EC2 instance successfully."
else
  echo "Failed to copy file from container to EC2 instance."
  exit 1
fi


