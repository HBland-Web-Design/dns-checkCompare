from mailProviders import smtp
        
def sendSMTP(env, envelope, content):
    server={}
    server['host'] = env['SMTP_SERVER']
    server['port'] = env['SMTP_PORT']
    server['Authentication'] = env['SMTP_AUTHENTICATION']
    server['username'] = env['SMTP_USERNAME']
    server['password'] = env['SMTP_PASSWORD']
    
    smtp.main(server, envelope, content)
    
    return

def sendMSGRAPH():
    
    return

def main(env, subject, body):
    
    envelope={}
    envelope['To'] = env['RECIPIENT']
    envelope['From'] = env['SENDER']
    envelope['Subject'] = subject
    
    if env['MAILER'] == 'SMTP':
        sendSMTP(env, envelope, body)
    elif env['MAILER'] == 'MSGRAPH':
        pass
    return