import pandas as pd
import json
import csv
import sqlalchemy
from sqlalchemy import create_engine
engine = create_engine(*args)

import datetime
current = datetime.date.today()
previous = current - datetime.timedelta(days=7)


current_data = pd.read_csv('2023-07-08_tickets.csv')
previous_data = pd.read_csv('2023-07-05_tickets.csv')
# current_data = pd.read_csv(f'{current}_tickets.csv')
# previous_data = pd.read_csv(f'{previous}_tickets.csv')

columns = (current_data.columns)


sql = "SELECT * FROM current_data "
stale_tickets = pd.read_sql_query(sql, engine)
stale_tickets

# for i in range(24,len(current_data)):
#   row = current_data.loc[i]
#   print(row)
  # print(current_data.loc[i, 'fields.updated'])


#print(current_data.loc[23])

# print(current_data.head())

