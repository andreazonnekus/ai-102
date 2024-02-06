import requests, uuid, json, os
from dotenv import load_dotenv

class Translation:
    def __init__(self):
        load_dotenv()

        # Add your key and url
        key = os.environ.get("TRANSLATOR_KEY")
        url = os.environ.get("TRANSLATOR_URL")
        location = os.environ.get("REGION")

    def translate(key, url, text = None):
        while text == None:
            text = input("What text do you want to translate?\n")
        path = '/translate'
        constructed_url = url + path

        params = {
            'api-version': '3.0',
            'from': 'zh',
            'to': ['en', 'fr', 'it']
        }

        headers = {
            'Ocp-Apim-Subscription-Key': key,
            # location required if you're using a multi-service or regional (not global) resource.
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # You can pass more than one object in body.
        body = [{
            'text': text,
        }]

        response = requests.post(constructed_url, params=params, headers=headers, json=body).json
        
        if response:
            print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))