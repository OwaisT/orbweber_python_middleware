import os
import requests
from dotenv import load_dotenv

load_dotenv()

WP_URL = os.getenv("WP_LINK")

# Get all the articles from WP
def get_articles():
    url = WP_URL + "posts"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return None

# Get a specific article from WP by id
def get_article(article_id):
    url = WP_URL + f"posts/{article_id}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return None