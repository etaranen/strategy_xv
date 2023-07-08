import pandas as pd
from requests.auth import HTTPBasicAuth
import requests
import json
import csv

import datetime

user = 'elizabeth.taranen@gmail.com'
apikey = 'ATATT3xFfGF0Fbztw2pDGyDasFTPcYc5oKS6Tux8JLk_W5TMmV_auQBkLI2dW5xsx_Lw2XeHdSPP-dCOfROb52h8gYTK1a8YjKU1ucThurp8cejYIqf6NN_Jqe7clR01Fjtr9H3919XRGEDdlH3fSdGRuoj17uPwEyxj2gWSR7lR6n81x2jMydc=52997052'
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

#automation_data.to_csv(f'{datetime.date.today()}_tickets.csv', index=False)
all_data.to_csv('issues.csv', index=False)

