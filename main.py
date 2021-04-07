import urllib.request
import json

import requests

params = {'lat':32.8000,'lon':34.9833,'n':50}
response = requests.get("http://api.open-notify.org/iss-pass.json",params=params)
rows = response.json()['response']

all = response.text # No need to parse this, unless you want to check it's valid
cur.execute('insert into t select * from json_populate_recordset(null::t, %s)', [all])

