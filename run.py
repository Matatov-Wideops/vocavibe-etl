from src.process_bucket import list_bucket
from src.utils import get_file
from tqdm import tqdm

bucket = list_bucket()
for filekey in tqdm(bucket):
    get_file(filekey,  destination_folder = '/home/alon/bucket')