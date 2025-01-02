import pandas as pd
from datetime import datetime
from twilio.rest import Client
import json

from src.settings import Settings
from src.keys import Keys
from src.utils import hash_phone_number as hashp




# def send_recording_update_to(source_file, X=28):
#     sessions_df = pd.read_csv(Settings.SESSIONS, dtype=str)
#     dropout = pd.read_csv(Settings.DROPOUT, dtype=str)
#     dropout['username'] = dropout['user_phone'].apply(hashp)
#     dropout = dropout['username'].tolist()
#     sessions_df = sessions_df[~sessions_df['username'].isin(dropout)].reset_index(drop=True)

#     # Create the desired dataframe with "username" and "last session" (the latest date for each user)
#     sessions_df = sessions_df.groupby('username')['date'].max().reset_index()
#     sessions_df.columns = ['username', 'last session']
#     sessions_df['last session'] = pd.to_datetime(sessions_df['last session'])

#     phones = pd.read_csv(Settings.USERS_CSV, dtype=str, usecols=['user_phone','username','password'])
#     sessions_df = pd.merge(sessions_df, phones, how='left', on=['username'])
#     sessions_df['days since last session'] = sessions_df['last session'].apply(lambda x: (datetime.now() - x).days)
#     sessions_df = sessions_df.sort_values(by='days since last session', ascending=False, ignore_index=True)
#     sessions_df['send?'] = sessions_df['days since last session'].apply(lambda x: 1 if x >= X else 0)
#     sessions_df = sessions_df[sessions_df['days since last session'] >= X-3]
#     return sessions_df[['username', 'user_phone', 'password', 'last session', 'days since last session', 'send?']]



def send_recording_notification(destination_phone_number: str, username, password) -> None:
    client = Client(Keys.TWILIO_ACCOUNT_SID, Keys.TWILIO_AUTH_TOKEN)
    try:
        # Send the whatsapp message
        message = client.messages.create(
            content_sid='HXc2bf7eb0b5ca2f4782630bab074144dd',
            from_=Keys.TWILIO_SENDER_SID,
            content_variables=json.dumps({
                '1': username,
                '2': password
            }),
            to=f'whatsapp:{destination_phone_number}'
        )

        print(f"Recording Notification Message sent to {destination_phone_number} with SID: {message.sid}")

    except Exception as e:
        print(f"Error sending SMS: {e!s}")


def send_recording_notification_without_link(destination_phone_number: str) -> None:
    client = Client(Keys.TWILIO_ACCOUNT_SID, Keys.TWILIO_AUTH_TOKEN)
    try:
        # Send the whatsapp message
        message = client.messages.create(
            content_sid='HX43f1d5b9209d22c2aa43106bbbfaeba7',
            from_=Keys.TWILIO_SENDER_SID,
            # content_variables=json.dumps({
            #     '1': username,
            #     '2': password
            # }),
            to=f'whatsapp:{destination_phone_number}'
        )

        print(f"Recording Notification Message sent to {destination_phone_number} with SID: {message.sid}")

    except Exception as e:
        print(f"Error sending SMS: {e!s}")



def send_recording_notification_ynet(destination_phone_number: str) -> None:
    client = Client(Keys.TWILIO_ACCOUNT_SID, Keys.TWILIO_AUTH_TOKEN)
    try:
        # Send the whatsapp message
        message = client.messages.create(
            content_sid='HX6e546b27daf521ad5c495b697058006a',
            from_=Keys.TWILIO_SENDER_SID,
            # content_variables=json.dumps({
            #     '1': username,
            #     '2': password
            # }),
            to=f'whatsapp:{destination_phone_number}'
        )

        print(f"Recording Notification Message sent to {destination_phone_number} with SID: {message.sid}")

    except Exception as e:
        print(f"Error sending SMS: {e!s}")



def send_healthy_notification(destination_phone_number: str, username, password) -> None:
    client = Client(Keys.TWILIO_ACCOUNT_SID, Keys.TWILIO_AUTH_TOKEN)
    try:
        # Send the whatsapp message
        message = client.messages.create(
            content_sid='HXf7d84b997e797d77d139c70cf089dcce',
            from_=Keys.TWILIO_SENDER_SID,
            content_variables=json.dumps({
                '1': username,
                '2': password
            }),
            to=f'whatsapp:{destination_phone_number}'
        )

        print(f"Recording Notification Message sent to {destination_phone_number} with SID: {message.sid}")

    except Exception as e:
        print(f"Error sending SMS: {e!s}")




def send_request_for_details_to_healthy(destination_phone_number: str, url: str = 'https://forms.gle/BPp8o398Mjk7Ka6L7') -> None:
    client = Client(Keys.TWILIO_ACCOUNT_SID, Keys.TWILIO_AUTH_TOKEN)
    try:
        # Send the whatsapp message
        message = client.messages.create(
            content_sid='HX7245044a97757a37d4b7381af4c41e1f',
            from_=Keys.TWILIO_SENDER_SID,
            content_variables=json.dumps({
                '1': url,
            }),
            to=f'whatsapp:{destination_phone_number}'
        )

        print(f"Recording Notification Message sent to {destination_phone_number} with SID: {message.sid}")

    except Exception as e:
        print(f"Error sending SMS: {e!s}")


def yom_kipur(destination_phone_number: str) -> None:
    client = Client(Keys.TWILIO_ACCOUNT_SID, Keys.TWILIO_AUTH_TOKEN)
    try:
        # Send the whatsapp message
        message = client.messages.create(
            content_sid='HXa7f28835e3336301e6bdf1fcdeb7f934',
            from_=Keys.TWILIO_SENDER_SID,
            to=f'whatsapp:{destination_phone_number}'
        )

        print(f"Recording Notification Message sent to {destination_phone_number} with SID: {message.sid}")

    except Exception as e:
        print(f"Error sending SMS: {e!s}")



def send_hc_weekly_reminder(destination_phone_number: str) -> None:
    client = Client(Keys.TWILIO_ACCOUNT_SID, Keys.TWILIO_AUTH_TOKEN)
    try:
        # Send the whatsapp message
        message = client.messages.create(
            content_sid='HX0f509fe65205ae382046f7295f3519c4',
            from_=Keys.TWILIO_SENDER_SID,
            to=f'whatsapp:+972{destination_phone_number}'
        )

        print(f"Recording Notification Message sent to {destination_phone_number} with SID: {message.sid}")

    except Exception as e:
        print(f"Error sending SMS: {e!s}")