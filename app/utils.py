from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from random import randint, choice
from datetime import datetime

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

MINE_ID = '1aiz9gRKu0BlPa9CjMmCwSepc4idziYT894HflLo6d-0'
# SAMPLE_RANGE_NAME = 'Jan!A:D'

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
    result = sheet.values().get(spreadsheetId=MINE_ID, range=cell_range).execute()
    categories = result.get('values', [])
    unique_categories = []
    for category in categories:
        if category[0] not in unique_categories:
            unique_categories.append(category[0])
    return unique_categories

def send_data_to_sheet(data_to_be_sent):
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
    result = service.spreadsheets().values().append(spreadsheetId=MINE_ID, range=cell_range, valueInputOption='USER_ENTERED', body=body).execute()
