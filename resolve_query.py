import pydig

class NoResponse(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)

def resolveQuery(record, recordType):

    try:
        queryAnswer = pydig.query(record, recordType)
        if queryAnswer == []:
            raise NoResponse("No Value")
        else:
            return queryAnswer
    except NoResponse as err:
        print(f"Fail: {err}")
    
