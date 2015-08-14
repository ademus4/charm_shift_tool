import smtplib
from email.mime.text import MIMEText
from email.message import Message


def alert(subject, message, sender, reciever):
    msg = MIMEText(message)

    msg['Subject']  = subject
    msg['From']     = sender
    msg['To']       = reciever

    print(msg['To'])
    print(reciever)
    s = smtplib.SMTP('cernmx.cern.ch')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
