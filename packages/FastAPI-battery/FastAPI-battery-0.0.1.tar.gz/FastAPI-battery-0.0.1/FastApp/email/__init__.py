import smtplib
import os

"""
This is a utility function to send email.
To use it, envs must be set:
GMAIL_ACCOUNT
GMAIL_APP_PASSWORD
These can be obtained from google.

It send email from GMAIL_ACCOUNT to itself.
"""


def send_admin_email(subject, content):
    msg = "Subject: " + subject + "\n\n" + content

    gmail_acc = os.getenv('GMAIL_ACCOUNT')
    gmail_pw = os.getenv('GMAIL_APP_PASSWORD')

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(gmail_acc, gmail_pw)
    smtp.sendmail(gmail_acc, gmail_acc, msg)
    smtp.quit()
