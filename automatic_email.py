# Your Python code (with corrected indentation)
import os
import datetime as dt
import ssl
import smtplib
import pandas as pd
from data_analysis import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

file = open(r'C:\Users\glowi\OneDrive\Documents\Projects\Midnight Sun\Jira Automation\email_log.txt', 'a')

file.write(f'{dt.date.today()} - the script ran \n')

email_sender = os.environ.get('Email_Address')
email_password = os.environ.get('Google_App_Password')
email_receiver = 'elizabeth.taranen@gmail.com'

subject = 'Email Sender Test'

em = MIMEMultipart("alternative")
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject

inactive_tickets_html = stale_tickets.to_html(index=False, classes="nice-table")
inactive_tickets_html = inactive_tickets_html.replace('class="dataframe"', 'class="nice-table"')

html = """\
<html>
  <head>
    <style>
      .nice-table {{
        font-family: Arial, sans-serif;
        font-size: 14px;
        color: #333;
        border-collapse: collapse;
        border: 1px solid #ccc;
        margin: 20px;
      }}

      .nice-table th {{
        background-color: #f2f2f2;
        font-weight: bold;
        text-align: left;
        padding: 8px;
      }}

      .nice-table td {{
        padding: 8px;
      }}

      .nice-table tr:hover {{
        background-color: #f9f9f9;
      }}

      .nice-table tr:nth-child(even) {{
        background-color: #f2f2f2;
      }}
    </style>
  </head>
  <body>
    <p> Good morning team leads! <br>
       Here is this week's ticket information: <br>
    </p>
    {inactive_tickets_html}
  </body>
</html>
""".format(inactive_tickets_html=inactive_tickets_html)

print(html)

part = MIMEText(html, "html")
em.attach(part)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
