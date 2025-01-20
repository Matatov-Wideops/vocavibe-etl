# Define variables
$PEM_FILE = "C:\\Users\\Nikita\\Desktop\\build.pem"
$EC2_USER = "nikita_m2"
$EC2_HOST = "35.221.31.111"
$CONTAINER_NAME = "klt-vocapp-frhp"
$REMOTE_FILE_PATH1 = "/data/.usershc.csv"
$EC2_LOCAL_PATH1 = "/home/nikita_m2/.usershc.csv"
$LOCAL_FILE_PATH1 = "../resources/usershc.csv"
$REMOTE_FILE_PATH2 = "/data/.userspd.csv"
$EC2_LOCAL_PATH2 = "/home/nikita_m2/.userspd.csv"
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
