import pandas as pd
import os

from google.cloud import storage
from rich.console import Console
from rich.tree import Tree
import boto3
from tqdm import tqdm
from typing import List

from src.settings import Settings
from src.keys import Keys

# from src.process_bucket import list_bucket



def list_bucket_for_user(username: str) -> List[str]:
    print(f"\nListing files for user: {username} from AWS bucket...")
    # AWS_ACCESS_KEY_ID = Keys.AWS_ACCESS_KEY_ID
    # AWS_SECRET_ACCESS_KEY = Keys.AWS_SECRET_ACCESS_KEY
    
    # Set AWS credentials in environment
    # os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    # os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY

    # Create S3 client
    # s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3 = storage.Client()
    files = []
    # response = s3.list_objects_v2(Bucket=Settings.BUCKET_NAME, Prefix=f"{username}/")
    response = s3.list_blobs(bucket_or_name=Settings.BUCKET_NAME, prefix=f"{username}/")
    while True:
        for content in tqdm(response.get('Contents', [])):
            files.append(content['Key'])
        
        # Check if there are more files to list
        if response.get('IsTruncated'):  # True if there are more files
            continuation_token = response.get('NextContinuationToken')
            # response = s3.list_objects_v2(Bucket=Settings.BUCKET_NAME, Prefix=f"{username}/", ContinuationToken=continuation_token)
            response = s3.list_blobs(bucket_or_name=Settings.BUCKET_NAME, Prefix=f"{username}/", ContinuationToken=continuation_token)
        else:
            break
    return files



def build_tree(filekeys):
    hierarchy = {}
    for filekey in filekeys:
        parts = filekey.split('/')
        current_level = hierarchy
        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
    return hierarchy


def add_branches(tree, hierarchy):
    for key, value in hierarchy.items():
        branch = tree.add(key)
        add_branches(branch, value)



def visualize_folder_structure(username, session=None):
    # Load the CSV file
    file_path = Settings.ALL_FILES
    df = pd.read_csv(file_path, dtype=str)


    # Filter the DataFrame based on username and session
    if session:
        filtered_df = df[(df['username'] == username) & (df['session'] == session)]
    else:
        filtered_df = df[df['username'] == username]

    # Extract file keys
    filekeys = filtered_df['filekey'].tolist()

    # Build the hierarchy
    hierarchy = build_tree(filekeys)

    # Create the root of the tree
    tree = Tree(f"Files and Folders for {username}" + (f" (Session: {session})" if session else ""))

    # Add branches to the tree
    add_branches(tree, hierarchy)

    # Print the tree using rich
    console = Console()
    console.print(tree)



def visualize_folder_structure_from_bucket(username):
    # List files for the specific user from the S3 bucket
    filekeys = list_bucket_for_user(username)

    # Build the hierarchy
    hierarchy = build_tree(filekeys)

    # Create the root of the tree
    tree = Tree(f"Files and Folders for {username}")

    # Add branches to the tree
    add_branches(tree, hierarchy)

    # Print the tree using rich
    console = Console()
    console.print(tree)




