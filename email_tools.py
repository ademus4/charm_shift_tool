import smtplib
from email.mime.text import MIMEText
from email.message import Message


def alert(subject, message, sender, recipients):
    msg = MIMEText(message)

    msg['Subject']  = subject
    msg['From']     = sender
    msg['To']       = ", ".join(recipients)

    s = smtplib.SMTP('cernmx.cern.ch')
    s.sendmail(msg['From'], recipients, msg.as_string())
    s.quit()
