import os
import numpy as np
import re
import csv
import subprocess
import hashlib
import platform
import pandas as pd
from cryptography.fernet import Fernet
import boto3
import requests
from datetime import date
import string
import secrets
import json
from datetime import datetime

from src.settings import Settings
from src.keys import Keys
# from src.query import list_bucket_for_user

# from settings import Settings
# from keys import Keys

def list_to_csv(var, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename'])
        for file in var:
            writer.writerow([file])


def get_s3():
    AWS_ACCESS_KEY_ID = Keys.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = Keys.AWS_SECRET_ACCESS_KEY
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    return s3


def get_os():
    return platform.system()


def run_shell_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command output:", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr.decode())
        raise


def run_windows_shell_command(command):
    try:
        result = subprocess.run(["powershell.exe", "-Command", command], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command output:", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr.decode())
        raise


def hash_phone_number(phone_number: str):
    # Convert the phone number to bytes
    bytes_data = phone_number.encode('utf-8')

    # Perform SHA-1 hashing
    sha1_hash = hashlib.sha1()
    sha1_hash.update(bytes_data)

    # Convert the digest to a hexadecimal string
    hashed_phone_number = sha1_hash.hexdigest()

    return hashed_phone_number


def standardize_phone_number(phone_number: str) -> str:

    try:
        cleaned_number = re.sub(r'\D', '', phone_number)
        if not cleaned_number.startswith('0'):
            cleaned_number = '0' + cleaned_number
        standardized_number = '+972' + cleaned_number
        return standardized_number
    except:
        return None



samplers = pd.read_csv(Settings.SAMPLERS_CSV, dtype=str, usecols=['sampler_phone', 'sampler_username', 'Hebrew'])
the_dict = samplers.set_index('sampler_phone')['sampler_username'].to_dict()
def sampler_phone_to_name(x):
        y = str(x).replace("+", "")
        if y in the_dict.keys():
            return the_dict[y]
        else:
            return x



def get_file(filekey: str, destination_folder, print_exist=False): 
    ENCRYPTION_KEY = Keys.ENCRYPTION_KEY
    s3 = get_s3()

    os_type = get_os()
    if os_type == "Windows":
        save_filekey = filekey.replace(":", "-")
    else:
        save_filekey = filekey

    destination_path = os.path.join(destination_folder, save_filekey)

    # Check if the file already exists in the destination folder
    if os.path.exists(destination_path):
        if print_exist:
            print(f"File {destination_path} already exists, skipping download.")
        return

    local_path, _ = os.path.split(destination_path)
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    s3.download_file('vocabucket', filekey, destination_path)
    fernet = Fernet(ENCRYPTION_KEY)
    with open(destination_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(destination_path, 'wb') as file:
        file.write(decrypted_data)



def generate_password(length):
    alphabet = string.ascii_letters + string.digits # + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


def generate_digits_password(length=9):
    alphabet = string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return f'0{password}'



def open_sampler(username, password, phone):
    AWS_ACCESS_KEY_ID = Keys.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = Keys.AWS_SECRET_ACCESS_KEY
    ADMIN_USER_NAME = Keys.ADMIN_USER_NAME
    ADMIN_PASSWORD = Keys.ADMIN_PASSWORD
    BASE_URL = Keys.BASE_URL

    # Set AWS credentials in environment
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY

    # Authenticate admin
    auth_url = f"{BASE_URL}/v1/auth/token"
    response = requests.post(auth_url, data={
        "username": ADMIN_USER_NAME,
        "password": ADMIN_PASSWORD,
        "scope": "sampler user admin",
        "grant_type": "password",
    })
    print(response)
    token = response.json()['access_token'] 
    headers = {
    'Authorization': f'Bearer {token}'
    }


    url = "https://voca-be.com/v1/users/signup"

    # User data
    user_data = {
        'is_healthy': False,
        'healthy_name': 'x',
        'consent': False,
        'sampler_phone': phone,
        'send_to': phone,
        'birth_date': date.today().isoformat(),
        'language': 'he',
        'gender': 'female',
        'mother_tongue': 'hebrew',
        'diagnosed_condition': 'parkinson',
        'year_of_diagnosis': 1900,
        'respiratory_disorders': [],
        'smoking_routine': "non_smoker",
        'dbs': "2024-04-24",
        'is_sampler': True,
        'username': "s_" + username,
        'password': password,
        "medical_center": "Ichilov",
        "nickname": "string",
        "send_password": True,
        "sleep_talk": True,
        "constipation": True,
        "falling": True,
        "smell": True
    }


    # Make a POST request to the API
    response = requests.post(url, json=user_data, headers=headers)

    # Check response
    if response.status_code == 200:
        print("User created successfully")
    else:
        print(response.status_code, response.json())




def get_user(username: str, hc=False):
    AWS_ACCESS_KEY_ID = Keys.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = Keys.AWS_SECRET_ACCESS_KEY
    ADMIN_USER_NAME = Keys.ADMIN_USER_NAME
    ADMIN_PASSWORD = Keys.ADMIN_PASSWORD
    BASE_URL = Keys.BASE_URL

    # Set AWS credentials in environment
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY

    # Authenticate admin
    auth_url = f"{BASE_URL}/v1/auth/token"
    response = requests.post(auth_url, data={
        "username": ADMIN_USER_NAME,
        "password": ADMIN_PASSWORD,
        "scope": "sampler user admin",
        "grant_type": "password",
    })
    token = response.json()['access_token'] 
    headers = {
    'Authorization': f'Bearer {token}'
    }

    HC = "hc_" if hc else ''
    userhash = username if len(username)>=40 else f"{HC}{hash_phone_number(username)}"
    url = f"https://voca-be.com/v1/users/{userhash}"

    response = requests.get(url, headers=headers)

    # Check response
    # if response.status_code == 200:
    #     print("User exists")
    # else:
    print(response.status_code, response.json())




def open_demo_patient(phone, password,
                 sampler_phone = "+9720549776075",
                 ):
    AWS_ACCESS_KEY_ID = Keys.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = Keys.AWS_SECRET_ACCESS_KEY

    # Admin credentials for other service
    ADMIN_USER_NAME = Keys.ADMIN_USER_NAME
    ADMIN_PASSWORD = Keys.ADMIN_PASSWORD
    BASE_URL = Keys.BASE_URL

    # Set AWS credentials in environment
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY

    # Authenticate admin
    auth_url = f"{BASE_URL}/v1/auth/token"
    response = requests.post(auth_url, data={
        "username": ADMIN_USER_NAME,
        "password": ADMIN_PASSWORD,
        "scope": "sampler user admin",
        "grant_type": "password",
    })
    print(response)
    token = response.json()['access_token'] 
    headers = {
    'Authorization': f'Bearer {token}'
    }


    url = "https://voca-be.com/v1/users/signup"

    # User data
    user_data = {
        'is_healthy': False,
        'healthy_name': 'x',
        'consent': False,
        'sampler_phone': sampler_phone,
        'send_to': phone,
        'birth_date': date.today().isoformat(),
        'language': 'he',
        'gender': 'female',
        'mother_tongue': 'hebrew',
        'diagnosed_condition': 'parkinson',
        'year_of_diagnosis': 1900,
        'respiratory_disorders': [],
        'smoking_routine': "non_smoker",
        'dbs': None,
        'is_sampler': False,
        'username': hash_phone_number(phone),
        'password': password,
        "medical_center": "Ichilov",
        "nickname": "string",
        "send_password": True,
        "sleep_talk": True,
        "constipation": True,
        "falling": True,
        "smell": True
    }


    # Make a POST request to the API
    response = requests.post(url, json=user_data, headers=headers)

    # Check response
    if response.status_code == 200:
        print("User created successfully")
    else:
        print(response.status_code, response.json())



def open_patient(phone: str, 
                password: str,
                birth_date: str,
                gender: str,
                mother_tongue: str,
                year_of_diagnosis: int,
                smoking_routine: str,
                genetic: str,
                sampler_phone="+9720549776075",
                language='he',
                respiratory_disorders=[],
                dbs=None,
                demo=False):
    
    AWS_ACCESS_KEY_ID = Keys.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = Keys.AWS_SECRET_ACCESS_KEY

    # Admin credentials for other service
    ADMIN_USER_NAME = Keys.ADMIN_USER_NAME
    ADMIN_PASSWORD = Keys.ADMIN_PASSWORD
    BASE_URL = Keys.BASE_URL

    # Set AWS credentials in environment
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY

    # Authenticate admin
    auth_url = f"{BASE_URL}/v1/auth/token"
    response = requests.post(auth_url, data={
        "username": ADMIN_USER_NAME,
        "password": ADMIN_PASSWORD,
        "scope": "sampler user admin",
        "grant_type": "password",
    })
    token = response.json()['access_token'] 
    headers = {
    'Authorization': f'Bearer {token}'
    }


    url = "https://voca-be.com/v1/users/signup"

    # User data
    user_data = {
        'is_healthy': False,
        'healthy_name': 'x',
        'consent': False,
        'sampler_phone': sampler_phone,
        'send_to': phone,
        'birth_date': birth_date,
        'language': language,
        'gender': gender,
        'mother_tongue': mother_tongue,
        'diagnosed_condition': 'parkinson',
        'year_of_diagnosis': year_of_diagnosis,
        'respiratory_disorders': respiratory_disorders,
        'smoking_routine': smoking_routine,
        'dbs': dbs,
        'is_sampler': False,
        'username': hash_phone_number(phone),
        'password': password,
        "medical_center": "Sheba",
        "nickname": "string",
        "send_password": True,
        "sleep_talk": False,
        "constipation": False,
        "falling": False,
        "smell": False,
        "genetic": genetic
    }


    # Make a POST request to the API
    response = requests.post(url, json=user_data, headers=headers)

    # Check response
    if response.status_code == 200:
        print("User created successfully")
    else:
        print(response.status_code, response.json())

    if demo:
        with open(Settings.DEMO_USERS, 'a', newline='') as csvfile:
            fieldnames = ['user_phone', 'username', 'date', 'sampler_phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write the header if the file is new
            if not os.path.isfile(Settings.DEMO_USERS):
                writer.writeheader()
            
            # Append the new row
            writer.writerow({
                'user_phone': phone,
                'username': hash_phone_number(phone),
                'date': date.today().isoformat(),
                'sampler_phone': sampler_phone
            })




def user_dict_from_row(row):
    user_dict = {}
    user_dict['healthy_name'] = 'from csv'
    user_dict['send_to'] = f"+972{row['מספר טלפון']}"
    
    dob = f"{row['שנת לידה']}-01-01"
    date_object = date.fromisoformat(dob)
    user_dict['birth_date'] = date_object.isoformat()

    user_dict['gender'] = 'male' if row['מגדר']=='גבר' else 'female'
    user_dict['smoking_routine'] = 'smoker' if row['שאלות כלליות [מעשן/ת?]']=='כן' else 'non_smoker'
    user_dict['mother_tongue'] = row['שפת אם'][:-3]
    user_dict['sleep_talk'] = True if row['שאלות כלליות [האם את/ה זז/ה הרבה מתוך שינה?]']=='כן' else False
    user_dict['constipation'] = True if row['שאלות כלליות [האם את/ה סובל/ת מעצירות?]']=='כן' else False
    user_dict['falling'] = True if row['שאלות כלליות [האם נפלת יותר מ 3 פעמים במהלך השנה האחרונה?]']=='כן' else False
    user_dict['smell'] = True if row['שאלות כלליות [האם יש ירידה בחוש הריח?]']=='כן' else False
    genetic = row['האם יש לך נטייה גנטית לפרקינסון?']
    if (genetic=='GBA') or (genetic=='LRRK2'):
        user_dict['genetic']=genetic
    elif genetic=='לא ידוע לי':
        user_dict['genetic']='NO'
    else:
        user_dict['genetic']='YES'
    return user_dict



def open_healthy(user_dict, sampler='+9720532752715'):
    AWS_ACCESS_KEY_ID = Keys.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = Keys.AWS_SECRET_ACCESS_KEY

    # Admin credentials for other service
    ADMIN_USER_NAME = Keys.ADMIN_USER_NAME
    ADMIN_PASSWORD = Keys.ADMIN_PASSWORD
    BASE_URL = Keys.BASE_URL

    # Set AWS credentials in environment
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY

    # Authenticate admin
    auth_url = f"{BASE_URL}/v1/auth/token"
    response = requests.post(auth_url, data={
        "username": ADMIN_USER_NAME,
        "password": ADMIN_PASSWORD,
        "scope": "sampler user admin",
        "grant_type": "password",
    })
    token = response.json()['access_token'] 
    headers = {
    'Authorization': f'Bearer {token}'
    }


    url = "https://voca-be.com/v1/users/signup"

    # User data
    user_data = {
        'is_healthy': True,
        'healthy_name': user_dict['healthy_name'],
        'consent': True,
        'sampler_phone': sampler,
        'send_to': user_dict['send_to'],
        'birth_date': user_dict['birth_date'],
        'language': 'he',
        'gender': user_dict['gender'],
        'mother_tongue': user_dict['mother_tongue'],
        'diagnosed_condition': 'parkinson',
        'year_of_diagnosis': 1900,
        'respiratory_disorders': [],
        'smoking_routine': user_dict['smoking_routine'],
        'dbs': None,
        'is_sampler': False,
        'username': f"hc_{hash_phone_number(user_dict['send_to'])}",
        'password': generate_digits_password(),
        "medical_center": "Sheba",
        "nickname": "string",
        "send_password": True,
        "sleep_talk": user_dict['sleep_talk'],
        "constipation": user_dict['constipation'],
        "falling": user_dict['falling'],
        "smell": user_dict['smell'],
        'genetic': user_dict['genetic'],
    }


    # Make a POST request to the API
    response = requests.post(url, json=user_data, headers=headers)

    # # Check response
    # if response.status_code == 200:
    #     print("User created successfully")
    # else:
    #     print(response.status_code, response.json())
    return response



def delete_user(username):
    AWS_ACCESS_KEY_ID = Keys.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = Keys.AWS_SECRET_ACCESS_KEY

    # Admin credentials for other service
    ADMIN_USER_NAME = Keys.ADMIN_USER_NAME
    ADMIN_PASSWORD = Keys.ADMIN_PASSWORD
    BASE_URL = Keys.BASE_URL

    # Set AWS credentials in environment
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY

    # Authenticate admin
    auth_url = f"{BASE_URL}/v1/auth/token"
    response = requests.post(auth_url, data={
        "username": ADMIN_USER_NAME,
        "password": ADMIN_PASSWORD,
        "scope": "sampler user admin",
        "grant_type": "password",
    })
    # print(response)
    token = response.json()['access_token'] 
    headers = {
    'Authorization': f'Bearer {token}'
    }


    url = f"https://voca-be.com/v1/users/{username}"

    # Make a DELETE request to the API
    response = requests.delete(url, headers=headers)

    # Check response
    if response.status_code == 200:
        print(f"User {username} deleted successfully")
    else:
        print(response.status_code, response.json())


def usernames_from_response(response_content):
    data = json.loads(response_content)
    usernames = [item["username"] for item in data]
    return usernames


def check_date_format(date_str):
    try:
        datetime.strptime(date_str, Settings.DATE_FORMAT)
    except ValueError:
        raise ValueError(f"Date {date_str} is not in the format {Settings.DATE_FORMAT}")
    

def get_all_users():
    AWS_ACCESS_KEY_ID = Keys.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = Keys.AWS_SECRET_ACCESS_KEY

    # Admin credentials for other service
    ADMIN_USER_NAME = Keys.ADMIN_USER_NAME
    ADMIN_PASSWORD = Keys.ADMIN_PASSWORD
    BASE_URL = Keys.BASE_URL

    # Set AWS credentials in environment
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY

    # Authenticate admin
    auth_url = f"{BASE_URL}/v1/auth/token"
    response = requests.post(auth_url, data={
        "username": ADMIN_USER_NAME,
        "password": ADMIN_PASSWORD,
        "scope": "sampler user admin",
        "grant_type": "password",
    })
    # print(response)
    token = response.json()['access_token'] 
    headers = {
    'Authorization': f'Bearer {token}'
    }


    url = f"https://voca-be.com/v1/users"

    # Make a DELETE request to the API
    response = requests.get(url, headers=headers)

    # Check response
    if response.status_code == 200:
        print(f"Users fetched successfully")
    else:
        print(response.status_code, response.json())
    return usernames_from_response(response._content)


def add_to_dropout(phone, date) -> None:
    check_date_format(date)
    try:
        df = pd.read_csv(Settings.DROPOUT, dtype=str)
    except:
        df = pd.DataFrame()
    sphone = standardize_phone_number(phone)
    hphone = hash_phone_number(sphone)
    user_df = pd.DataFrame(columns=['username','user_phone','drop_out'], data=[[hphone,sphone,date]])
    df = pd.concat([df, user_df], ignore_index=True)
    df = df.drop_duplicates(ignore_index=True)
    df.to_csv(Settings.DROPOUT, index=False)



def get_password(identifier, users_file = Settings.ALL_USERS):
    users_df = pd.read_csv(users_file, dtype=str)
    
    def normalize_phone(phone):
        if pd.isna(phone) or not isinstance(phone, str):
            return np.nan
        phone = ''.join(filter(str.isdigit, phone))
        return phone[3:] if phone.startswith(('972', '+972')) else phone

    if identifier in users_df['username'].values:
        result = users_df[users_df['username'] == identifier]
    else:
        identifier_normalized = normalize_phone(identifier)
        if identifier in users_df['user_phone'].values:
            result = users_df[users_df['user_phone'] == identifier]
        else:
            result = users_df[users_df['user_phone'].apply(normalize_phone) == identifier_normalized]

    if result.empty:
        return "No user found with that identifier."
    
    return result[['username', 'user_phone', 'password']].to_dict(orient='records')



# def check_when_hc_recorded(phone:str) -> datetime:
#     filekeys = list_bucket_for_user("hc_" + hash_phone_number(f'+972{phone}'))