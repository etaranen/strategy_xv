import pandas as pd
import json
import csv
import sqlalchemy

import datetime as dt
from datetime import datetime, timedelta

file = open(r'C:\Users\glowi\OneDrive\Documents\Projects\Midnight Sun\Jira Automation\data_log.txt', 'a')

file.write(f'{dt.date.today()} - the script ran \n')


current = dt.date.today()
previous = current - dt.timedelta(days=1)
stale_date = current - dt.timedelta(days=12)

current_data = pd.read_csv('new_tickets.csv')
previous_data = pd.read_csv('old_tickets.csv')


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
current_data.to_csv('new_tickets.csv', index= False)

for i in range(len(current_data)):

    #progress count and streak
    if current_data.loc[i, 'fields.status.name'] == 'In Progress':
        updated = current_data.loc[i, 'fields.updated']
        updated = datetime.strptime(updated[:10], '%Y-%m-%d').date()
        if current_data.loc[i, 'Count'] == None:
            current_data.loc[i, 'Count'] = 0
            current_data.loc[i, 'Streak'] = 0            
        if updated > previous:
            current_data.loc[i, 'Count'] += 1
            current_data.loc[i, 'Streak'] += 1
        else:
            current_data.loc[i, 'Streak'] = 0
 
current_data.to_csv('new_tickets.csv', index=False)


#date formating
current_data['fields.created'] = pd.to_datetime(current_data['fields.created'], format='%Y-%m-%dT%H:%M:%S.%f%z', utc=True)
current_data['fields.created'] = pd.to_datetime(current_data['fields.created']).dt.strftime('%Y-%m-%d')

current_data['fields.updated'] = pd.to_datetime(current_data['fields.updated'], format='%Y-%m-%dT%H:%M:%S.%f%z', utc=True)
current_data['fields.updated'] = pd.to_datetime(current_data['fields.updated']).dt.strftime('%Y-%m-%d')

inactive_members = current_data

# dataframe of to-do tickets
todo_tickets = current_data.loc[current_data['fields.status.name'] == 'To Do']


# dataframe of stale tickets
stale_tickets=current_data.loc[current_data['fields.status.name'].isin(['To Do', 'In Progress'])]

stale_tickets = stale_tickets.sort_values(by='Count', ascending=True)
stale_tickets = stale_tickets.head(5)

# stale based on a date
# for i in range(1, len(current_data)):
#     updated = current_data.loc[i, 'fields.updated']
#     updated = datetime.strptime(updated[:10], '%Y-%m-%d').date()
#     if updated > stale_date:
#         stale_tickets = stale_tickets.drop(labels=i, axis=0)

stale_tickets = stale_tickets.rename(columns={'fields.assignee.displayName':'Name', 'fields.created': 'Created', 'fields.updated': 'Updated', 'id': 'ID', 'self': 'Link', 'key': 'Key', 'fields.parent.id' : 'Parent ID', 'fields.status.name' : 'Status', 'fields.issuetype.name' : 'Issue Type', 'fields.summary' : 'Summary', 'fields.description' : 'Description'})
stale_tickets.to_csv('stale_tickets.csv', index=False)



#inactive members
# unique_names = inactive_members['fields.assignee.displayName'].unique().tolist()
# three_weeks_ago = current - dt.timedelta(days=21)
# inactive_members = inactive_members[inactive_members['fields.updated'] < three_weeks_ago]
# inactive_names = inactive_members['fields.assignee.displayName'].unique().tolist()
# inactive_members.to_csv('inactive_members.csv', index=False)


#leaderboard
current_data_count = current_data.sort_values(by='Count', ascending=False)
leaderboard = current_data_count.head(5)
leaderboard = leaderboard[['fields.assignee.displayName', 'self', 'fields.summary', 'Count', 'Streak']]
leaderboard = leaderboard.rename(columns={'fields.assignee.displayName':'Name', 'self': 'Link', 'fields.summary' : 'Summary'})

leaderboard.to_csv('leaderboard.csv', index=False)

