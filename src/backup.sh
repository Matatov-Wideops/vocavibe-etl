#!/bin/bash

# Define S3 bucket and destination directory
bucket="s3://vocabucket"
destination_base="/mnt/seagate/bucket"

# Create destination directory if it doesn't exist
mkdir -p "$destination_base"

# Function to check if the external storage is mounted
check_mount() {
    if ! mount | grep -q "/mnt/seagate"; then
        echo "External storage is not mounted. Exiting..."
        exit 1
    fi
}

# List files in the S3 bucket
echo "Listing files in S3 bucket $bucket..."
files=$(aws s3 ls "$bucket" --recursive | awk '{print $4}')

# Loop through each file and download it
for file in $files; do
    # Check if the external storage is still mounted
    check_mount

    destination_path="$destination_base/$file"
    destination_dir=$(dirname "$destination_path")

    # Skip the file if it already exists
    if [ -f "$destination_path" ]; then
        echo "Skipping $file as it already exists at $destination_path."
        continue
    fi

    echo "Downloading $file to $destination_path..."

    # Create destination directory if it doesn't exist
    mkdir -p "$destination_dir"

    # Download the file directly to the external storage
    aws s3 cp "$bucket/$file" "$destination_path"

    # Check if the download was successful
    if [ $? -eq 0 ]; then
        echo "Successfully downloaded $file to $destination_path."
    else
        echo "Failed to download $file to $destination_path."
    fi
done
