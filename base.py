'''
Setup and Base Functions for all HID analytics
'''
import json
import urllib.request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pytz import timezone
import os

# Set up Google Sheets connection
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
if os.path.isfile('client_secret.json'):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    with open('client_secret.json') as f:
        data = json.load(f)
        API_KEY = data["api_key"]
else:
    creds = {}
    creds["type"] = "service_account"
    creds["project_id"] = os.getenv('PROJECT_ID')
    print(os.getenv('PROJECT_ID'))
    creds["private_key_id"] = os.getenv('PRIVATE_KEY_ID')
    creds["private_key"] = os.getenv('PRIVATE_KEY').replace("\\n", "\n")
    creds["client_email"] = os.getenv('CLIENT_EMAIL')
    creds["client_id"] = os.getenv('CLIENT_ID')
    creds["auth_uri"] = "https://accounts.google.com/o/oauth2/auth"
    creds["token_uri"] = "https://accounts.google.com/o/oauth2/token"
    creds["auth_provider_x509_cert_url"] = "https://www.googleapis.com/oauth2/v1/certs"
    creds["client_x509_cert_url"] = os.getenv('CLIENT_X509_CERT_URL')
    API_KEY = os.getenv('API_KEY')
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
gc = gspread.authorize(credentials)
wks = gc.open("HID Metrics")

def open_url(url):
    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req).read()
    content = json.loads(r.decode('utf-8'))
    return content

def update_timestamp(worksheet): # Pull time of program execution and update
    geneva = timezone('Etc/GMT-2')
    current_time = datetime.now(geneva)
    formatted_time = current_time.strftime("%d %m %Y %H:%M:%S")
    updated = "As of: " + formatted_time + ' (GMT+2)'
    return updated