import pandas as pd
import json
import csv
import sqlalchemy

import datetime as dt
from datetime import datetime

current = dt.date.today()
previous = current - dt.timedelta(days=7)
stale_date = current - dt.timedelta(days=14)

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
current_data = current_data.merge(previous_data[['id','progress.count', 'progress.streak']], on='id',  how='left')
current_data.to_csv(f'{current}_tickets.csv', index= False)

for i in range(len(current_data)):

    #progress count and streak
    if current_data.loc[i, 'fields.status.name'] == 'In Progress':
        updated = current_data.loc[i, 'fields.updated']
        updated = datetime.strptime(updated[:10], '%Y-%m-%d').date()
        if updated > previous or updated <= current:
            current_data.loc[i, 'progress.count'] += 1
            current_data.loc[i, 'progress.streak'] += 1
        else:
            current_data.loc[i, 'progress.streak'] = 0
        
    
current_data.to_csv(f'{dt.date.today()}_tickets.csv', index=False)


# dataframe of unassigned tickets
todo_tickets = current_data.loc[current_data['fields.status.name'] == 'To Do']

# dataframe of stale tickets
stale_tickets = current_data

for i in range(1, len(current_data)):
    updated = current_data.loc[i, 'fields.updated']
    updated = datetime.strptime(updated[:10], '%Y-%m-%d').date()
    if updated > stale_date:
        stale_tickets = stale_tickets.drop(labels=i, axis=0)

stale_tickets.to_csv('stale_tickets.csv', index=False)


# dataframe of active tickets
# inprogress_tickets = current_data.loc[current_data['fields.status.name'] == 'In Progress']
# inprogress_tickets = inprogress_tickets.loc[inprogress_tickets['fields.issuetype.name'] == 'Subtask']


# velocity could be either from the day the ticket was created (this can be inaccurate as there are many stale tickts with no one assigned)
# long-term we can track if previous_data['assignee']= None and current_data['assignee']!= None, start count from that week to check velocity
# for burn down charts we need leads to put an estimated time of completion
# maybe even start with creating a data frame with active tickets (like the one at the bottom of the page)
# then you can join each week (data will only be connected if the previous week has data)
# easy way to track if someone has started a ticket (for velocity - a start date)
