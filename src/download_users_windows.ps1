# Define variables
$PEM_FILE = "../build-key.pem"
$EC2_USER = "ec2-user"
$EC2_HOST = "ec2-3-83-206-91.compute-1.amazonaws.com"
$CONTAINER_NAME = "vocabe"
$REMOTE_FILE_PATH1 = "/data/.usershc.csv"
$EC2_LOCAL_PATH1 = "/home/ec2-user/.usershc.csv"
$LOCAL_FILE_PATH1 = "resources/usershc.csv"
$REMOTE_FILE_PATH2 = "/data/.userspd.csv"
$EC2_LOCAL_PATH2 = "/home/ec2-user/.userspd.csv"
$LOCAL_FILE_PATH2 = "resources/userspd.csv"

# Log into AWS EC2 and copy the file from the Docker container to the EC2 instance's home directory
ssh -i $PEM_FILE $EC2_USER@$EC2_HOST "sudo docker cp ${CONTAINER_NAME}:${REMOTE_FILE_PATH1} ${EC2_LOCAL_PATH1}; sudo docker cp ${CONTAINER_NAME}:${REMOTE_FILE_PATH2} ${EC2_LOCAL_PATH2}"

# Check if the SSH command was successful
if ($LASTEXITCODE -eq 0) {
  Write-Output "File copied from container to EC2 instance successfully."
} else {
  Write-Output "Failed to copy file from container to EC2 instance."
  exit 1
}

# Download the file from the EC2 instance to the local machine
scp -i $PEM_FILE ${EC2_USER}@${EC2_HOST}:${EC2_LOCAL_PATH1} $LOCAL_FILE_PATH1
scp -i $PEM_FILE ${EC2_USER}@${EC2_HOST}:${EC2_LOCAL_PATH2} $LOCAL_FILE_PATH2

# Check if the SCP command was successful
if ($LASTEXITCODE -eq 0) {
  Write-Output "File downloaded to local machine successfully."
} else {
  Write-Output "Failed to download file to local machine."
  exit 1
}
