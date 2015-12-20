from smtplib import SMTP_SSL

from flask import render_template
from email.mime.text import MIMEText

smtp_server = "smtp.gmail.com"
smtp_user = "something@mtu.edu"
smtp_pass = "shhhh"

def dispatchConfirmEmail(toaddr, code):
    # TODO: send an email here
    subject = "Please Confirm Your Broomball Referee Account"
    server = smtplib.SMTP_SSL(smtp_server)
    server.login(smtp_user, smtp_pass)

    server.close()

    return None