
import requests
import os
from dotenv import load_dotenv
load_dotenv()
PAGE_ID = os.getenv("PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")

def get_facebook_page_posts():
    url = f'https://graph.facebook.com/v17.0/{PAGE_ID}/posts'
    params = {
        'access_token': FB_ACCESS_TOKEN
    }
    
    response = requests.get(url, params=params)

    
    if response.status_code == 200:
        posts = response.json()
        return posts
    else:
        print(f'Error: {response.status_code}')
        return None