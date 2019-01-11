"""Utility functions to help with writitng to the Google Sheet"""
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

load_dotenv(dotenv_path='./.env')

SCOPES = getenv('WRITE-SCOPE')
SHEET_ID = getenv('SHEET-ID')
SUBMISSION_KEY = getenv('SECRET-SUBMISSION-KEY')


def get_categories():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    sheet = service.spreadsheets()
    month = datetime.now().strftime('%b')
    cell_range = '%s!C2:C' % month
    result = sheet.values().get(spreadsheetId=SHEET_ID,
                                range=cell_range).execute()
    categories = result.get('values', [])
    sorted_set = set([x[0] for x in categories])
    return sorted_set


def send_data_to_sheet(data_to_be_sent, sent_key=None, send_data=True):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    month = datetime.now().strftime('%b')
    cell_range = '%s!A:D' % month
    body = {
        'values': [data_to_be_sent]
    }
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    if send_data and sent_key == SUBMISSION_KEY:
        service.spreadsheets().values().append(spreadsheetId=SHEET_ID, range=cell_range, valueInputOption='USER_ENTERED', body=body).execute()
        return True
    else:
        return False
