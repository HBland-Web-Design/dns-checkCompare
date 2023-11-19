import mailProviders

class NoProvider(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)

class Mailer:
    def __init__(self, env):
        self.env = env
        self.MAILCREDENTIALS = {}
        self.MAILER = ""

    def DefineMailer(self):
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

    def chosenProvider(self):
        provider = self.MAILER
        try:
            if provider == "MSGRAPH":
                continue
            elif provider == "SMTP""
                continue
            else:
                raise NoProvider("No Provider Selected")
            return
        except NoProvider as err:
            print(f"Error: {err}")
            return

    def sendMail(self):

        return