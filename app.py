from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import datetime
import window
import mailer
import analytics
import wp_articles

# Load the environment variables
load_dotenv()

# Create the Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://orbweber.com/", "https://www.orbweber.com/", "https://www.orbweber.com", "https://orbweber.com"]}})

# Set the API key
app.config['API_KEY'] = os.getenv("B_API_KEY")

# Print a message to the console when app starts
print("App is running")

# Define the global variables
window_home = None
services = None
service_services = None
websites_testimonials = None
about = None
contact = None
blog_meta = None

# Load the data from the Airtable
def load_data():
    global window_home
    global service_services
    global websites_testimonials
    global services
    global about
    global contact
    global blog_meta

    meta_home = window.get_meta_for_page("home")
    intro = window.get_intro()
    services_home = window.get_services_home()
    story_home = window.get_story_home()
    websites_testimonials = window.get_websites_testimonials()
    window_home = {
        "meta" : meta_home,
        "intro" : intro,
        "services_home" : services_home,
        "story_home" : story_home,
        "websites_home" : websites_testimonials
    }

    meta_services = window.get_meta_for_page("services")
    offer_services = window.get_offer_services()
    services_services = window.get_services_services()
    services = {
        "meta" : meta_services,
        "offer_services" : offer_services,
        "services_services" : services_services
    }

    meta_contact = window.get_meta_for_page("contact")
    contact_data = window.get_contact()
    contact = {
        "meta" : meta_contact,
        "contact" : contact_data
    }

    meta_about = window.get_meta_for_page("about")
    abouts_personal = window.get_about()
    about = {
        "meta" : meta_about,
        "abouts_personal" : abouts_personal,
        "websites_about" : websites_testimonials
    }
    blog_meta = window.get_meta_for_page("blog")

load_data()

def authenticate(api_key):
    return api_key == app.config['API_KEY']

# Endpoints
# The route for reloading data every 4 hrs since airtable image links expire every 4 hrs
@app.route("/data_reload", methods=['GET'])
def data_reload():
    load_data()
    print("Data reloaded")
    return "Data reloaded", 200

# The route for sending an email from the contact form
@app.route('/send_email', methods=['POST'])
def send_email_route():
    api_key = request.headers.get('Authorization')

    if not api_key or not authenticate(api_key):
        print("Unauthorized called")
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    print(data)
    mail = mailer.send_contact_email(data)
    if mail == 'Mail sent succesfully':
        return mail, 200
    else:
        return mail, 500

# The route for keeping the server alive
@app.route('/keep_alive', methods=['GET'])
def keep_alive():
    print("Kept alive")
    return 'OK', 200

# the route for getting the home page data
@app.route('/get_window_home', methods=['GET'])
def get_window_home():
    if window_home != None:
        print(datetime.datetime.now())
        return window_home, 200
    else:
        return "Error retieving intros", 500

# the route for getting the services page data
@app.route('/get_services', methods=['GET'])
def get_services():
    if services != None:
        return services, 200
    else:
        return "Error retieving services", 500

# the route for getting the service page data according to the service name
@app.route('/get_service', methods=['POST'])
def get_service():
    data = request.get_json()
    service = window.get_service_service_page(data['service_name'])
    if service != None:
        return service, 200
    else:
        return "Error retieving service", 500

# the route for getting the contact page data
@app.route('/get_contact', methods=['GET'])
def get_contact():
    if contact != None:
        return contact, 200
    else:
        return "Error retieving contact", 500

# the route for getting the about page data
@app.route('/get_about', methods=['GET'])
def get_about():
    if about != None:
        return about, 200
    else:
        return "Error retieving about", 500

# the route for tracking events
@app.route('/track_event', methods=['POST'])
def track_event():
    data = request.get_json()
    response = analytics.send_event_to_ga4(data)
    return response

# the route for getting the blog meta data
@app.route('/get_blog_meta', methods=['GET'])
def get_blog_meta():
    if blog_meta != None:
        return blog_meta, 200
    else:
        return "Error retieving blog meta", 500

# the route for getting the articles
@app.route('/get_articles', methods=['GET'])
def get_articles():
    articles = wp_articles.get_articles()
    return articles

# the route for getting a single article by id
@app.route('/get_article', methods=['POST'])
def get_article():
    data = request.get_json()
    article = wp_articles.get_article(data['article_id'])
    return article

# start the server
if __name__ == "__main__":
    app.run()
