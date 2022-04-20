from __future__ import print_function

import json
import os.path
from typing import List

from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks', ]

APP_TOKEN_FILE = "token.json"
USER_TOKEN_FILE = "user_token.json"


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
    flow = InstalledAppFlow.from_client_secrets_file(APP_TOKEN_FILE,
                                                     SCOPES)
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
            flow = InstalledAppFlow.from_client_secrets_file(
                APP_TOKEN_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(USER_TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds


# Использовал при первой регистрации нужно проверить работоспособность без него
# def get_service_auth():
#     '''Get Auth API service with O'Auth 2.0'''
#     # creds = get_creds_cons()
#     creds = get_creds_saved()
#     service = build('oauth2', 'v2', credentials=creds)
#     return service


def get_service_task():
    '''Get Tasks API service with O'Auth 2.0'''
    # creds = get_creds_cons()
    creds = get_creds_saved()
    service = build('tasks', 'v1', credentials=creds)
    return service


def pop_tasklist_by_title(list_items: List) -> str:
    for item in list_items:
        try:
            if item.get('title') == 'Task List from Python':
                service.tasklists().delete(tasklist=item.get('id')).execute()
        except:
            pass


def insert_task_list():
    '''Create item of TaskLists'''
    service = get_service_task()
    service.tasklists().insert(
        body={'title': 'Task List from Python'}
        ).execute()


def get_service_method_dict():
    for i in dir(get_service_task().tasklists()):
        if not i.startswith('_'):
            for j in dir(i):
                if not j.startswith('_'):
                    print(f'<<< service method : {i} - {j} >>>')


class TasksCRUD(object):
    def __init__(self):
        self.service = get_service_task()

    def get_list_tasklists(self) -> List:
        '''Get User List of TaskLists'''
        response = self.service.tasklists().list().execute()

        items = response.get('items', [])
        return items

    def insert_task_list(self) -> None:
        '''Create item of TaskLists'''
        self.service.tasklists().insert(
            body={'title': 'Task List from Python'}).execute()

    def update_task_list(self) -> None:
        '''Update item of TaskLists'''
        for item in self.get_list_tasklists():
            if str(item.get('title')) == 'Task List from Python':
                item['title'] = 'Changed Task List'
                self.service.tasklists().update(
                    tasklist=item['id'],
                    body=item).execute()

    def delete_task_list(self) -> None:
        '''Delete item of TaskLists'''
        for item in self.get_list_tasklists():
            if str(item.get('title')) == 'Changed Task List':
                self.service.tasklists().delete(
                    tasklist=item['id']).execute()


if __name__ == '__main__':
    # Смотрим какие сервисы нам доступны
    get_service_method_dict()

    # Создаем объект TasksCRUD API c соответствующими параметрами
    api = TasksCRUD()

    # Получаем список СпискЗадач: List[< tasklist >]
    items = api.get_list_tasklists()

    print('Task lists:')
    for item in items:
        print(u'{0} ({1})'.format(item['title'], item['id']))
