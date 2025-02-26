import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

data = {
    "query": "Can I club my CL and SL together?",
}

body = str.encode(json.dumps(data))

url = 'https://wcazaistudioproject-ezpsv.southindia.inference.ml.azure.com/score'

api_key = 'GjUW9eV4OJqiaYFSipxq0IjFV6ayraUM'
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")


headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    # print(result)
    decoded_result = json.loads(result.decode("utf8"))["reply"]
    reference = json.loads(result.decode("utf8"))["documents"]
    print(decoded_result)
    print(reference)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))