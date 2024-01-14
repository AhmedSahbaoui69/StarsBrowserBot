import base64
import json
import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests

# Necessary tokens to interact with the Whatsapp Business API
PAGE_ACCESS_TOKEN = os.environ['PAGE_ACESS_TOKEN']
WHATSAPP_URL = os.environ['WHATSAPP_URL']

# Verify if a string represents a valid url (structure wise)
def is_valid_url(string):
    try:
        result = urlparse(string)
        return bool(result.netloc)
    except ValueError:
        return False

# Extract the base domain URL from a long URL.
def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

# Save a URL's entire HTML content (including images, external JS & CSS) into a file.
def save_html(url, filepath):
    headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # Fetch the url
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # Parse the html content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Fetch and replace external CSS
    css_links = soup.find_all('link', rel='stylesheet')
    for css_link in css_links:
        css_url = urljoin(url, css_link['href'])
        css_response = requests.get(css_url)
        css_content = css_response.text
        style_tag = soup.new_tag('style')
        style_tag.string = css_content
        css_link.replace_with(style_tag)

    # Fetch and replace external JavaScript
    script_tags = soup.find_all('script', src=True)
    for script_tag in script_tags:
        script_url = urljoin(url, script_tag['src'])
        script_response = requests.get(script_url)
        script_content = script_response.text
        new_script_tag = soup.new_tag('script')
        new_script_tag.string = script_content
        script_tag.replace_with(new_script_tag)

    # Fetch and encode images in base64
    base_url = get_base_url(url)
    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        try:
            img_url = img_tag['src']
            # Adjust relative URLs to absolute URLs
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            elif img_url.startswith('/'):
                img_url = urljoin(base_url, img_url)

            # Fetch and encode the image in base64
            img_response = requests.get(img_url)
            img_data = base64.b64encode(img_response.content).decode('utf-8')
            # Replace the src attribute
            img_tag['src'] = f'data:image/png;base64,{img_data}'
        except:
            pass

    # Save the modified HTML to the given file
    with open(filepath, 'w', encoding='utf-8') as html_file:
        html_file.write(str(soup))

def generate_text_message_payload(contact_id, body):
    data = {
        'messaging_product': 'whatsapp',
        'recipient_type': 'individual',
        'to': contact_id,
        'type': 'text',
        'text': {
            'body': body
        }
    }
    return json.dumps(data)


def generate_template_message_payload(contact_id, template_name):
    data = {
        "messaging_product": "whatsapp",
        'recipient_type': 'individual',
        "to": contact_id,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
            "code": "en"
            }
        }
    }
    return json.dumps(data)


def generate_document_message_payload(contact_id, url, caption, filename):
    data = {
        'messaging_product': 'whatsapp',
        'recipient_type': 'individual',
        'to': contact_id,
        'type': 'document',
        'document': {
            'link': url,
            'caption': caption,
            'filename': filename
        }
        }
    return json.dumps(data)


def send_reply(data):
    url = f'https://graph.facebook.com/v18.0/{WHATSAPP_URL}/messages'
    headers = {
    'Authorization': f'Bearer {PAGE_ACCESS_TOKEN}',
    'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
