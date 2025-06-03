from flask import jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GA4_MEASUREMENT_ID = os.getenv('GA4_MEASUREMENT_ID')
API_SECRET = os.getenv('API_SECRET_GA4')

# Send the event to Google Analytics 4
def send_event_to_ga4(data):
    payload = create_payload(data)

    url = get_url()

    response = requests.post(url, json=payload)
    if response.status_code == 204:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': response.text}), 500

# Create the payload for the Google Analytics 4
def create_payload(data):
    return {
        'client_id': data.get('client_id'),
        "events": [
            {
                'name': data.get('event_name'),
                'params': data.get('params', {})
            }
        ]
    }

# Get the URL for the Google Analytics 4
def get_url():
    return f'https://www.google-analytics.com/mp/collect?measurement_id={GA4_MEASUREMENT_ID}&api_secret={API_SECRET}'