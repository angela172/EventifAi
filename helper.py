import os
import json
import logging
import datetime
import time
import yaml
from base64 import b64encode
import spotipy
from langchain.requests import Requests
from langchain import OpenAI

from utils import reduce_openapi_spec, ColorPrint
from model import ApiLLM

from model.api_selector import icl_examples as api_selector_icl
from model.planner import icl_examples as planner_icl
from requests.auth import HTTPBasicAuth

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def format_event_response(response):
    try:
        # Parse the JSON string response
        event_details = json.loads(response)
        return event_details
    except json.JSONDecodeError as e:
        print("response=",response)
        print("Error parsing JSON response:", e)
        return None


def create_google_calendar_event(service, event_details, use_google_meet):
    from uuid import uuid4
    event = {
        'summary': event_details["summary"],
        'location': event_details["location"],
        'description': event_details["description"],
        'start': {
            'dateTime': event_details["start_time"],
            'timeZone': event_details["time_zone"],
        },
        'end': {
            'dateTime': event_details["end_time"],
            'timeZone': event_details["time_zone"],
        },
        'attendees': [{'email': email} for email in event_details["attendees"]]
    }

    if use_google_meet:
        event["conferenceData"] = {
            'createRequest': {
                'requestId': str(uuid4()),  # Generate a unique requestId
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        }

    try:
        event = service.events().insert(calendarId='primary', body=event, sendUpdates='all', conferenceDataVersion=1 if use_google_meet else 0).execute()
        print(event)
        return event
        # return event 
        # print(f"Event created: {event.get('htmlLink')}")
        # if use_google_meet:
            # return event.get('hangoutLink')
            # print(f"Google Meet link: {event.get('hangoutLink')}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_google_calendar_service(creds_path='configs.json', token_path='token.json'):
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "configs.json", SCOPES)
            creds = flow.run_local_server(port=8080)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def populate_api_selector_icl_examples():
    with open(f"./icl_examples/api_selector/gcalendar.txt", 'r') as f:
        examples = f.read()
    api_selector_icl['gcalendar'] = f"""{examples}
    """

def populate_planner_icl_examples():
    with open(f"./icl_examples/planner/gcalendar.txt", 'r') as f:
        examples = f.read()
    planner_icl['gcalendar'] = f"""{examples}
    """

def replace_api_credentials(model, actual_key, actual_token):
    # Open the file and read the contents
    with open(f"./icl_examples/{model}/gcalendar_base.txt", 'r') as file:
        content = file.readlines()

    # Replace placeholders with actual key and token
    updated_content = [line.replace(r"{key}", actual_key).replace(r"{token}", actual_token) for line in content]

    # Write the updated content back to the file
    with open(f"./icl_examples/{model}/gcalendar.txt", 'w') as file:
        file.writelines(updated_content)

def replace_api_credentials_in_json( actual_key, actual_token):
    # Open the JSON file and load the content
    with open(f"./specs/gcalendar_base.json", 'r') as json_file:
        content = json.load(json_file)

    def replace_values(d, actual_key, actual_token):
        for key, value in d.items():
            if isinstance(value, dict):
                replace_values(value, actual_key, actual_token)
            elif isinstance(value, str):
                d[key] = value.replace(r"{key}", actual_key).replace(r"{token}", actual_token)

    def process_list_of_dicts(lst, actual_key, actual_token):
        for item in lst:
            if isinstance(item, dict):
                replace_values(item, actual_key, actual_token)

    # Function to recursively update placeholders in a nested dictionary
    def update_placeholders(obj):
        if isinstance(obj, list):
            process_list_of_dicts(lst=obj, actual_key=actual_key, actual_token=actual_token)
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    update_placeholders(value)

    # Replace placeholders with actual key and token
    update_placeholders(content)

    # Write the updated content back to the file
    with open(f"./specs/gcalendar_oas.json", 'w') as json_file:
        json.dump(content, json_file, indent=2)
        print("Contents updated!")

