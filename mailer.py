import mail-providers

def DefineMailer(env):
    MAILCREDENTIALS = {}
    MAILER = ""
    if env.MS_MAIL == "True": #TODO: Add to ENV Variables
        MAILER = MSGRAPH
        MAILCREDENTIALS['TENNANTID'] = env.MS_TENNANT_ID
        MAILCREDENTIALS['CLIENTID'] = env.MS_CLIENT_ID
        MAILCREDENTIALS['CLIENTSECRET'] = env.MS_CLIENT_SECRET
    elif env.SMTP == 'True': #TODO: Add to ENV Variables
        MAILER = SMTP
        MAILCREDENTIALS['SERVER'] = "" #TODO: Update ENV Variables and fill
        MAILCREDENTIALS['PORT'] = "" #TODO: Update ENV Variables and fill
        MAILCREDENTIALS['USERNAME'] = "" #TODO: Update ENV Variables and fill
        MAILCREDENTIALS['PASSWORD'] = "" #TODO: Update ENV Variables and fill
    else:
        MAILER = ""

def chosenProvider():

    return

def sendMail():

    return