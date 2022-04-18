from __future__ import print_function

import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

APP_TOKEN_FILE = "token.json"
USER_TOKEN_FILE = "user_token.json"

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks', ]


def main():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('tasks', 'v1', credentials=creds)

        # Call the Tasks API
        results = service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])

        if not items:
            print('No task lists found.')
            return

        print('Task lists:')
        for item in items:
            print(u'{0} ({1})'.format(item['title'], item['id']))
    except HttpError as err:
        print(err)


def get_creds_cons():
    '''Ask from console'''
    flow = InstalledAppFlow.from_client_secrets_file(APP_TOKEN_FILE, SCOPES)
    return flow.run_console()


def get_creds_saved():
    '''Reusebale user OAuth2 token'''
    # https://developers.google.com/docs/api/quickstart/python
    creds = None

    if os.path.exists(USER_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(USER_TOKEN_FILE, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(APP_TOKEN_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(USER_TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds


def get_service():
    '''Get YouTube API service w API Key only'''
    # creds = get_creds_cons()
    creds = get_creds_saved()
    service = build('oauth2', 'v2', credentials=creds)
    return service


def get_service_task():
    '''Get YouTube API service w API Key only'''
    # creds = get_creds_cons()
    creds = get_creds_saved()
    service = build('tasks', 'v1', credentials=creds)
    return service


def get_user_info():
    '''Get User Info'''
    service = get_service_task()
    results = service.tasks().list().execute()
    items = results.get('items', [])
    if not items:
        print('No task lists found.')
        return
    print('Task lists:')
    for item in items:
        print(u'{0} ({1})'.format(item['title'], item['id']))


def get_service_dict():
    for i in dir(get_service_task().tasks()):
        if not i.startswith('_'):
            print(i)


if __name__ == '__main__':
    get_user_info()
    # get_service_dict()
