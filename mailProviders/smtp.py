import smtplib
import certifi
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def mailSSL(server, msg):
    context = ssl.create_default_context(cafile=certifi.where())
    try:
        recipients = msg['To'].split(',')
        mailserver = smtplib.SMTP_SSL(server['host'], server['port'], context=context)
        mailserver.login(server['username'], server['password'])
        mailserver.sendmail(msg['From'], recipients, msg.as_string())
        mailserver.close()
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

    return

def main(server, envelope, content):
    
    msg =  MIMEMultipart("alternative")
    msg['To'] = envelope['To']
    msg['From'] = envelope['From']
    msg['Subject'] = envelope['Subject']
    msg.attach(MIMEText(content, 'html'))
    
    if server['Authentication'] == 'SSL':
        mailSSL(server, msg)
    else:
        print('Unavailable Authentication Method')
        raise Exception