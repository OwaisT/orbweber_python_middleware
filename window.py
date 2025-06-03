import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Airtable API Key
API_KEY = os.getenv("API_KEY")
# Airtable Base URL
BASE_URL = os.getenv("API_URL")
# Airtable auth Headers
headers = {
    "Authorization": f"Token {API_KEY}"
}

# Get the intro data from the Airtable
def get_intro():
    url = f"{BASE_URL}457378/?user_field_names=true"
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        records = data['results']
        titles = []
        for record in records:
            title = record
            title["button_to_page"] = record['button_to_page'][0]['value']
            title['image'] = record['image'][0]['url']
            titles.append(title)
        print("Intro received")
        return titles
    else:
        return None

# Get the services data for home page from the Airtable
def get_services_home():
    url = f"{BASE_URL}457380/?user_field_names=true"
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        records = data['results']
        services = []
        for record in records:
            service = record
            service['headline'] = record['headline_service_home']
            service['subheadline'] = record['subheadline_service_home']
            service['button_to_page'] = record['button_to_page_service_home']
            service['button_text'] = record['button_text_service_home']
            service['image'] = record['image_service_home'][0]['url']
            services.append(service)
        print("Services received")
        return services
    else:
        return None

# Get the story data for home page from the Airtable
def get_story_home():
    url = f"{BASE_URL}457381/?user_field_names=true"
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        records = data['results']
        stories = []
        for record in records:
            story = record
            story['story'] = record['story_home']
            stories.append(story)
        print("Story received")
        return stories[0]['story']
    else:
        return None

# Get the websites testimonials data for home and about page from the Airtable
def get_websites_testimonials():
    url = f"{BASE_URL}457382/?user_field_names=true"
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        records = data['results']
        websites = []
        for record in records:
            website = record
            website['image'] = record['image'][0]['url']
            websites.append(website)
        print("Websites received")
        return websites
    else:
        return None

# Get the offer data for services page from the Airtable
def get_offer_services():
    url = f"{BASE_URL}457380/?user_field_names=true"
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        records = data['results']
        offers = []
        for record in records:
            if record['is_offer']['value'] == 'Yes':
                offer = {}
                offer['name'] = record['service_name']
                offer['headline'] = record['headline_services_page']
                offer['description'] = record['description_services_page']
                offer['button_text'] = record['button_text_services_page']
                offer['button_to_page'] = record['button_to_page_services_page']
                offer['image'] = record['image_services_page'][0]['url']
                offer['schema_name'] = record['schema_name']
                offer['schema_price'] = record['schema_price']
                offers.append(offer)
        print("Offers received")
        return offers
    else:
        return None

# Get the services data for services page from the Airtable
def get_services_services():
    url = f"{BASE_URL}457380/?user_field_names=true"
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        records = data['results']
        services = []
        for record in records:
            if record['is_offer']['value'] == 'No':
                service = {}
                service['name'] = record['service_name']
                service['headline'] = record['headline_services_page']
                service['description'] = record['description_services_page']
                service['button_text'] = record['button_text_services_page']
                service['button_to_page'] = record['button_to_page_services_page']
                service['image'] = record['image_services_page'][0]['url']
                service['schema_name'] = record['schema_name']
                service['schema_price'] = record['schema_price']
                services.append(service)
        print("Services received")
        return services
    else:
        return None

# Get all the features data for service individual page from the Airtable
def get_features():
    url = f"{BASE_URL}457385/?user_field_names=true"
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        print(data['results'])
        print("Features received")
        return data['results']
    else:
        return None

features = get_features()

# Get the services data for service individual page from the Airtable as a list
def get_services_service_page():
    url = f"{BASE_URL}457380/?user_field_names=true"
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        records = data['results']
        services = []
        for record in records:
            service = {}
            service['name'] = record['name']
            service['service_name'] = record['service_name']
            service['headline'] = record['headline_service_page']
            service['button_text'] = record['button_text_service_page']
            service['button_to_page'] = record['button_to_page_service_page']
            service['steps'] = record['steps']
            service['packaging'] = record['packaging']
            service["features"] = get_features_for_service(record['id'], features)
            service['price'] = record['price_service_page']
            service['background'] = record['background_service_page'][0]['url']
            service['image'] = record['image_service_page'][0]['url']
            service['meta_title'] = record['meta_title_service_page']
            service['meta_description'] = record['meta_description_service_page']
            service['schema_price'] = record['schema_price']
            service['schema_name'] = record['schema_name']
            services.append(service)
        return services
    else:
        return None

# get features for specific service from features list
def get_features_for_service(service_id, features):
    service_features = []
    for feature in features:
        for service in feature['services']:
            if service['id'] == service_id:
                service_features.append(feature)
                break # Exit the inner loop when a match is found
    return service_features

# Get the services data for service individual page from the Airtable as a list
def get_service_service_page(service_id):
    url = f"{BASE_URL}457380/{service_id}/?user_field_names=true"
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        record = data
        service = {}
        service['id'] = record['id']
        service['name'] = record['name']
        service['service_name'] = record['service_name']
        service['headline'] = record['headline_service_page']
        service['button_text'] = record['button_text_service_page']
        service['button_to_page'] = record['button_to_page_service_page']
        service['steps'] = record['steps']
        service['packaging'] = record['packaging']
        service["features"] = get_features_for_service(record['id'], features)
        service['price'] = record['price_service_page']
        service['background'] = record['background_service_page'][0]['url']
        service['image'] = record['image_service_page'][0]['url']
        service['meta_title'] = record['meta_title_service_page']
        service['meta_description'] = record['meta_description_service_page']
        service['schema_price'] = record['schema_price']
        service['schema_name'] = record['schema_name']
        print("Service received", service['id'])
        return service
    else:
        return None

# Get the contact data for contact page from the Airtable
def get_contact():
    url = f"{BASE_URL}457383/?user_field_names=true"
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        records = data['results']
        contacts = []
        for record in records:
            contact = record
            contact['copy'] = record['contact_copy']
            contacts.append(contact)
        return contacts[0]
    else:
        return None

# Get the about data for about page from the Airtable
def get_about():
    url = f"{BASE_URL}457381/?user_field_names=true"
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        records = data['results']
        stories = []
        for record in records:
            story = record
            story['image'] = record['image'][0]['url']
            stories.append(story)
        return stories
    else:
        return None

# Get the meta data for the page from the Airtable
def get_meta_for_page(page):
    url = f"{BASE_URL}457384/?user_field_names=true"
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        records = data['results']
        for record in records:
            if record['page'] == page:
                return record
        return None
    else:
        return None
