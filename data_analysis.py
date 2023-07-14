import pandas as pd
import json
import csv
import sqlalchemy


import datetime
current = datetime.date.today()
previous = current - datetime.timedelta(days=7)


current_data = pd.read_csv('2023-07-08_tickets.csv', encoding='utf-8')
previous_data = pd.read_csv('2023-07-05_tickets.csv', encoding='utf-8')
# current_data = pd.read_csv(f'{current}_tickets.csv')
# previous_data = pd.read_csv(f'{previous}_tickets.csv')


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


#consecutive weekly progress and overall- who has a streak, whos fastest overall
#append/edit columns to the end of the csv with this info so we can add streaks from previous csv data


# append last 2 (or 3 if velocity) columns for previous_data (progress_count and progress_streak) to current_data
# make sure to match up the rows correctly using a join (sql but also exists in pandas)
# go through each row check the following:
# if the jira has been updated, add 1 to the total count of progress and 1 to the streak
# if the jira has not been updated and streak != 0, set streak to 0
# velocity could be either from the day the ticket was created (this can be inaccurate as there are many stale tickts with no one assigned)
# long-term we can track if previous_data['assignee']= None and current_data['assignee']!= None, start count from that week to check velocity
# for burn down charts we need leads to put an estimated time of completion
# maybe even start with creating a data frame with active tickets (like the one at the bottom of the page)
# then you can join each week (data will only be connected if the previous week has data)
# easy way to track if someone has started a ticket (for velocity - a start date)


# for i in range(len(current_data)):
#     row = current_data.loc[i]
#     data = row['fields.updated']
#       OR
#     data = current_data.loc[i, 'fields.updated'])


# dataframe of stale tickets
todo_tickets = current_data.loc[current_data['fields.status.name'] == 'To Do']
todo_tickets.to_csv(f'todo_tickets.csv', index=False)

# dataframe of active tickets
inprogress_tickets = current_data.loc[current_data['fields.status.name'] == 'In Progress']
inprogress_tickets = inprogress_tickets.loc[inprogress_tickets['fields.issuetype.name'] == 'Subtask']
