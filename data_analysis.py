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


columns = (current_data.columns)


for i in range(len(current_data)):
    print(current_data.loc[i, 'fields.updated'])





