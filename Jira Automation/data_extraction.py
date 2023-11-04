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

#save yesterday's data
old_tickets = pd.read_csv('new_tickets.csv')
old_tickets.to_csv('old_tickets.csv', index=False)

#pull new data
data = json.loads(response)
data = data['issues']
data = pd.json_normalize(data)
all_data = pd.DataFrame.from_dict(data, orient='columns')

automation_data = data[['fields.assignee.displayName', 'fields.created', 'fields.updated', 'id', 'self', 'key', 'fields.parent.id', 'fields.status.name', 'fields.issuetype.name', 'fields.summary', 'fields.description']]

for i in range(len(automation_data)):
    self = automation_data.loc[i, 'self']
    key = automation_data.loc[i, 'key']
    link = f'https://uwmidsun.atlassian.net/browse/{key}'
    automation_data.replace(self, link, inplace = True)

automation_data.to_csv('new_tickets.csv', index=False)
