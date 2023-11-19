import msgraph-sdk
from azure.identity.aio import ClientSecretCredential

def graphClient():

    scopes = ['https://graph.microsoft.com/.default']

    credential = ClientSecretCredential(
        tenant_id=,
        client_id=,
        client_secret=)

    return GraphServiceClient(credential, scopes)