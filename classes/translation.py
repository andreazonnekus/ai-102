import requests, uuid, json, os, sys
from dotenv import load_dotenv

class Translation:
    def __init__(self) -> None:
        load_dotenv()

        # Add your key and url
        self.key = os.environ.get("TRANSLATOR_KEY")
        self.url = os.environ.get("TRANSLATOR_URL")
        self.location = os.environ.get("REGION")
        
    def main(self):
        try:
            # Get image
            if len(sys.argv) > 1:
                if len(sys.argv) > 2:
                    txt = sys.argv[2]
            
                # Analyze image
                if sys.argv[1] == 'translate':
                    self.analyse_image(txt)
        except Exception as ex:
            print(ex)

    def translate(self, text = None):
        while text == None:
            text = input("What text do you want to translate?\n")
        path = '/translate'
        constructed_url = self.url + path

        params = {
            'api-version': '3.0',
            'from': 'zh',
            'to': ['en', 'fr', 'it']
        }

        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            # location required if you're using a multi-service or regional (not global) resource.
            'Ocp-Apim-Subscription-Region': self.location,
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