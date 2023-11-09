import pydig
import tldextract

class NoResponse(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)

def getRootDomain(record):
    extracted = tldextract.extract(record)
    return f"{extracted.domain}.{extracted.suffix}"
    
def resolveQuery(record, recordType):

    try:
        queryAnswer = pydig.query(record, recordType)
        if queryAnswer == []:
            raise NoResponse("No Value")
        else:
            response = {}
            response["domain"] = getRootDomain(record)
            response["record"] = record
            response["recordType"] = recordType
            response["recordValue"] = queryAnswer

            return response

    except NoResponse as err:
        print(f"Fail: {err}")
