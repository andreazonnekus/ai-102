import requests, json, os, ssl, sys
from dotenv import load_dotenv

load_dotenv()

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script

columns = dict.fromkeys([
      "day",
      "mnth",
      "year",
      "season",
      "holiday",
      "weekday",
      "workingday",
      "weathersit",
      "temp",
      "atemp",
      "hum",
      "windspeed"
])

for column in columns:
    columns[column] = input(f"What is {column}? ")

request_data =  {
  "input_data": {
    "data": [columns]
  }
}

url = os.environ.get("BIKE_RENTAL_URL") if os.environ.get("BIKE_RENTAL_URL") else sys.argv[1]
if not url:
    raise Exception("A key should be provided to invoke the endpoint as either the BIKE_RENTAL_URL or as an argument to the cmd ")

key = os.environ.get("BIKE_RENTAL_KEY") if os.environ.get("BIKE_RENTAL_KEY") else sys.argv[2]
if not key:
    raise Exception("A key should be provided to invoke the endpoint as either the BIKE_RENTAL_KEY or as an argument to the cmd ")

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ key), 'azureml-model-deployment': 'automl7888bd14162-1' }

try:
    response = requests.post(url, data=json.dumps(request_data), headers=headers)

    result = int(json.loads(response.content)[0])
    # result = json.loads(response.content)
    print(f"On {columns['day']}-{columns['mnth']}-{columns['year']} there should have been approximately {result} bike rentals")
    # print(result)
except requests.exceptions.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))