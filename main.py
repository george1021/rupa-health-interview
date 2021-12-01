import os
from dotenv import load_dotenv
from flask import Flask, request
import requests
import yaml
import html2text
import json
import http.client

load_dotenv()
app = Flask(__name__)


@app.route("/", methods=['POST'])
def hello_world():
    email = request.get_json(force=True)
    valid = validate_input(email)
    if not valid:
        return 'Invalid format'
    replace_html_with_text(email)
    service = get_email_service()
    if service == 'mailgun':
        response = send_email_mailgun(email)
    else:
        response = send_email_sendgrid(email)
    if response.status_code == 200:
        return f"Email sent!"
    else:
        return f"Error sending email through {service}: Code {response.status_code} - {response.text}"


def validate_input(email):
    if not email.get('to') or \
            not email.get('to_name') or \
            not email.get('from') or \
            not email.get('from_name') or \
            not email.get('subject') or \
            not email.get('body'):
        return False
    return True


def replace_html_with_text(email):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_tables = True
    email['body'] = h.handle(email['body'])


def send_email_mailgun(email):
    url = os.getenv('MAILGUN_URL')
    api_key = os.getenv('MAILGUN_API_KEY')
    return requests.post(
        url,
        auth=("api", api_key),
        data={"from": f"{email['from_name']} <{email['from']}>",
              "to": [f"{email['to_name']} <{email['to']}>"],
              "subject": email['subject'],
              "text": email['body']})


def send_email_sendgrid(email):
    url = os.getenv('SENDGRID_BASE_URL')
    api_key = os.getenv('SENDGRID_API_KEY')
    headers = {
        'authorization': 'Bearer ' + api_key,
        'content-type': 'application/json'
    }
    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": email['to'],
                        "name": email['to_name']
                    }
                ]
            }
        ],
        "subject": email['subject'],
        "content": [
            {
                "type": "text/plain",
                "value": email['body']
            }
        ],
        "from": {
            "email": email['from'],
            "name": email['from_name']
        },
    }
    payload =json.dumps(data)
    conn = http.client.HTTPSConnection(url)
    conn.request('POST', '/v3/mail/send', payload, headers)
    res = conn.getresponse()

    return res


def get_email_service():
    config = get_config()
    if config['default_email_service'] and config['default_email_service'].lower() in ['sendgrid', 'mailgun']:
        current_service = config['default_email_service'].lower()
    else:
        last_used_service = str(config.get('last_used_email_service', 'sendgrid')).lower()
        current_service = 'mailgun' if last_used_service == 'sendgrid' else 'sendgrid'

    config['last_used_email_service'] = current_service
    write_config(config)
    return current_service


def get_config():
    filename = os.environ.get('EMAIL_SERVICE_CONFIG', 'config.yaml')
    with open(filename, 'r+') as f:
        return yaml.load(f, yaml.FullLoader)


def write_config(config):
    filename = os.environ.get('EMAIL_SERVICE_CONFIG', 'config.yaml')
    with open(filename, 'w') as f:
        yaml.dump(config, f)


if __name__ == '__main__':
    app.run()
