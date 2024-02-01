import requests, uuid, json, os
from dotenv import load_dotenv

load_dotenv()

# Add your key and endpoint
key = os.environ.get("TRANSLATOR_KEY")
endpoint = os.environ.get("TRANSLATOR_URL")

print(endpoint)
# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location = os.environ.get("REGION")

path = '/translate'
constructed_url = endpoint + path

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
    'text': '你以爲你是誰',
    # 'text': 'Hello, friend! What did you do today?'
},
{
     'text': '你是誰啊',
}
]

request = requests.post(constructed_url, params=params, headers=headers, json=body)
print(request)
response = request.json()

print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))