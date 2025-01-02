import os
import pandas as pd

from src.settings import Settings
# from settings import Settings


def save_processed_filekey(filekey, log_file):
        with open(log_file, 'a') as f:
            f.write(f"{filekey}\n")



def load_processed_files(log_file):
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            return list(f.read().splitlines())
    return []


def load_blacklist():
    try:
        df = pd.read_csv(Settings.DO_NOT_DOWNLOAD)
    except:
        return []
    return df['filekey'].tolist()