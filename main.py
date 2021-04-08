import urllib.request
import json

import requests

params = {'lat':32.8000,'lon':34.9833,'n':50}
response = requests.get("http://api.open-notify.org/iss-pass.json",params=params)
rows = response.json()['response']


