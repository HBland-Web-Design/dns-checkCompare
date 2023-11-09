import pydig
import tldextract

class NoResponse(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)

def get_root_domain(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

# Example usage
url = "https://subdomain.example.com/path/to/page"
root_domain = get_root_domain(url)
print(f"Root domain: {root_domain}")

def resolveQuery(record, recordType):

    try:
        queryAnswer = pydig.query(record, recordType)
        if queryAnswer == []:
            raise NoResponse("No Value")
        else:
            response = {}
            response["domain"] = 
            response["record"] = record
            response["recordType"] = recordType
            response["recordValue"] = queryAnswer

            return response

    except NoResponse as err:
        print(f"Fail: {err}")
