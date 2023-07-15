import os
import pandas as pd
from requests.auth import HTTPBasicAuth
import requests
import json
import csv

import datetime

#if there is an error when running - no data or doesnt exist - check your key is correct
user = 'elizabeth.taranen@gmail.com'
apikey = os.environ.get('Atlassian_API_Token')
server = 'https://uwmidsun.atlassian.net'


url = "https://uwmidsun.atlassian.net/rest/api/2/search"
auth = HTTPBasicAuth(user, apikey)

headers = {"Accept": "application/json"}

query = {'jql': 'project = STRAT15', "maxResults":200}
response = requests.get(url, params=query, headers=headers, auth=auth).text


data = json.loads(response)
data = data['issues']
data = pd.json_normalize(data)
all_data = pd.DataFrame.from_dict(data, orient='columns')

automation_data = data[['fields.assignee.displayName', 'fields.created', 'fields.updated', 'id', 'self', 'key', 'fields.parent.id', 'fields.status.name', 'fields.issuetype.name', 'fields.status.statusCategory.id', 'fields.summary', 'fields.description']]

automation_data.to_csv(f'{datetime.date.today()}_tickets.csv', index=False)
