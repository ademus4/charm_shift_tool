# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.message import Message

sms_address = '004175411{}@mail2sms.cern.ch'

def main():
    msg = MIMEText('Sent at 14:21')

    msg['Subject']  = 'CHARM No Beam Test!'
    msg['From']     = 'yomama@cern.ch'
    #msg['To']       = 'adam.thornton@cern.ch'
    msg['To']       = sms_address.format(7164)
    #msg['To']       = '0041762167164@mail2sms.cern.ch'

    s = smtplib.SMTP('cernmx.cern.ch')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

if __name__ == '__main__':
    main()

