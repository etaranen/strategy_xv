import datetime
from email.message import EmailMessage
import ssl
import smtplib
import gingers

file = open(r'C:\Users\glowi\OneDrive\Documents\Projects\Midnight Sun\Jira Automation\email_log.txt', 'a')

file.write(f'{datetime.datetime.now()} - the script ran \n')

email_sender = 'glowing.prl@gmail.com'
email_password = 'isvmggguzupdyalo'
email_receiver = 'elizabeth.taranen@gmail.com'

subject = 'Email Sender Test'
body = f"Testing to see if the email sends {datetime.datetime.now()} \n"

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())

# https://www.youtube.com/watch?v=g_j6ILT-X0k