from oauth2client.client import flow_from_clientsecrets, HttpAccessTokenRefreshError
from oauth2client.file import Storage
from apiclient.discovery import build
import os
import httplib2

from mailbot.constants import *

oauth_root = os.path.join(credential_root, 'oauth')

def saveCredentials(username, credentials):
    storage = Storage(os.path.join(oauth_root, '%s_creds' % username))
    storage.put(credentials)

def getCredentialsFromOnline():
    flow = flow_from_clientsecrets(os.path.join(oauth_root, 'client_id.json'),
                               scope='https://www.googleapis.com/auth/gmail.send',
                               redirect_uri='urn:ietf:wg:oauth:2.0:oob')
    auth_uri = flow.step1_get_authorize_url()

    print("Please go to the following link, click accept, and copy the code from your browser")
    print()
    print(auth_uri)
    print()

    code = input("Oauth code: ")

    credentials = flow.step2_exchange(code)

    return credentials

def getCredentialsFromStorage(username):
    storage = Storage(os.path.join(oauth_root, '%s_creds' % username))
    credentials = storage.get()

    return credentials

def getCredentials(username):
    credentials = getCredentialsFromStorage(username)

    if credentials is None:
        print("Credentials were not found locally, getting new credentials from Google")
        credentials = getCredentialsFromOnline()
        saveCredentials(username, credentials)
    else:
        if credentials.access_token_expired:
            print("Credentials have expired, refreshing...")
            try:
                credentials.refresh(httplib2.Http())
            except HttpAccessTokenRefreshError:
                print("Unable to refresh credentials, getting new credentials from google")
                credentials = getCredentialsFromOnline()
                saveCredentials(username, credentials)

    if credentials is None:
        raise Exception("Unable to obtain credentials from a file or the server")

    return credentials

def getServiceInstance(credentials):
    http = httplib2.Http()
    http = credentials.authorize(http)
    return build('gmail', 'v1', http=http)
