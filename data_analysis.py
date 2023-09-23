import pandas as pd
import json
import csv
import sqlalchemy

import datetime as dt
from datetime import datetime

current = dt.date.today()
previous = current - dt.timedelta(days=7)
stale_date = current - dt.timedelta(days=12)

current_data = pd.read_csv(f'{current}_tickets.csv')
previous_data = pd.read_csv(f'{previous}_tickets.csv')


#temporary unicode error fix - prints to the console but won't be seen if sending an email
for row in current_data.iterrows():
    try:
        print(row)
    except Exception as e:
        e= str(e)
        start = e.find('\\')
        end = e.find('in')
        char = e[start:(end-2)]
        current_data['fields.summary'] = current_data['fields.summary'].str.replace(char, ' ', regex=True)
        current_data['fields.description'] = current_data['fields.description'].str.replace(char, ' ', regex=True)


# consecutive weekly progress and overall count- who has a streak, whos fastest overall
current_data = current_data.merge(previous_data[['id','Count', 'Streak']], on='id',  how='left')
current_data.to_csv(f'{current}_tickets.csv', index= False)

for i in range(len(current_data)):

    #progress count and streak
    if current_data.loc[i, 'fields.status.name'] == 'In Progress':
        updated = current_data.loc[i, 'fields.updated']
        updated = datetime.strptime(updated[:10], '%Y-%m-%d').date()
        if updated > previous or updated <= current:
            current_data.loc[i, 'Count'] += 1
            current_data.loc[i, 'Streak'] += 1
        else:
            current_data.loc[i, 'Streak'] = 0

# velocity
# velocity = []
# for i in range(len(current_data)):
#     velocity += ((current_data.loc[i, 'Count'])/days)

        
current_data.to_csv(f'{dt.date.today()}_tickets.csv', index=False)


# dataframe of unassigned tickets
todo_tickets = current_data.loc[current_data['fields.status.name'] == 'To Do']

current_data['fields.created'] = pd.to_datetime(current_data['fields.created'], format='%Y-%m-%dT%H:%M:%S.%f%z', utc=True)
current_data['fields.created'] = pd.to_datetime(current_data['fields.created']).dt.strftime('%Y-%m-%d')

current_data['fields.updated'] = pd.to_datetime(current_data['fields.updated'], format='%Y-%m-%dT%H:%M:%S.%f%z', utc=True)
current_data['fields.updated'] = pd.to_datetime(current_data['fields.updated']).dt.strftime('%Y-%m-%d')

# dataframe of stale tickets
stale_tickets = current_data

for i in range(1, len(current_data)):
    updated = current_data.loc[i, 'fields.updated']
    updated = datetime.strptime(updated[:10], '%Y-%m-%d').date()
    if updated > stale_date:
        stale_tickets = stale_tickets.drop(labels=i, axis=0)

stale_tickets = stale_tickets.rename(columns={'fields.assignee.displayName':'Name', 'fields.created': 'Created', 'fields.updated': 'Updated', 'id': 'ID', 'self': 'Link', 'key': 'Key', 'fields.parent.id' : 'Parent ID', 'fields.status.name' : 'Status', 'fields.issuetype.name' : 'Issue Type', 'fields.summary' : 'Summary', 'fields.description' : 'Description'})
stale_tickets.to_csv('stale_tickets.csv', index=False)


import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('2023-07-15_tickets.csv')  
unique_names = df['fields.assignee.displayName'].unique().tolist()
df['fields.updated'] = pd.to_datetime(df['fields.updated'])
current = dt.datetime.now()
three_weeks_ago = current - timedelta(weeks=3)
# inactive_members = df[df['fields.updated'] < three_weeks_ago]
# inactive_names = inactive_members['fields.assignee.displayName'].unique().tolist()

current_data_count = current_data.sort_values(by='Count', ascending=False)
leaderboard = current_data_count.head(5)
leaderboard = leaderboard[['fields.assignee.displayName', 'self', 'fields.summary', 'Count', 'Streak']]
leaderboard = leaderboard.rename(columns={'fields.assignee.displayName':'Name', 'self': 'Link', 'fields.summary' : 'Summary'})

leaderboard.to_csv('leaderboard.csv', index=False)

