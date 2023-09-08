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


inactive_tickets_html = stale_tickets.to_html()
table = inactive_tickets_html.find('table')
inactive_tickets_html = inactive_tickets_html[:(table)] + 'table class="nice-table"' + inactive_tickets_html[(table+34):]


html = """\
<html>
  <head>
  <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    </n>

    <p> Good morning team leads! <br>
       Here is this week's ticket information: <br>
    </p>
    
    
    {inactive_tickets_html}
    
  </body>
</html>
""".format(inactive_tickets_html=inactive_tickets_html)


# part = MIMEText(html, "html")
# em.attach(part)


# context = ssl.create_default_context()

# with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#     smtp.login(email_sender, email_password)
#     smtp.sendmail(email_sender, email_receiver, em.as_string())
