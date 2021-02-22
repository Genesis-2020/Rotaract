import base64
import httplib2

from email.mime.text import MIMEText

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
# from oauth2client.tools import run
from flask import Flask

app = Flask(__name__)

@app.route('/sendmail')

def sendmail():
  # Path to the client_secret.json file downloaded from the Developer Console
  CLIENT_SECRET_FILE = 'client_secret.json'

  # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
  OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

  # Location of the credentials storage file
  STORAGE = Storage('gmail.storage')

  # Start the OAuth flow to retrieve credentials
  flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
  http = httplib2.Http()

  # Try to retrieve credentials from storage or run the flow to generate them
  credentials = STORAGE.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(flow, STORAGE, http=http)

  # Authorize the httplib2.Http object with our credentials
  http = credentials.authorize(http)

  # Build the Gmail service from discovery
  gmail_service = build('gmail', 'v1', http=http)

  # create a message to send
  message = MIMEText("This is test mail from flask")
  message['to'] = "mukeshjavvaji123@gmail.com"
  message['from'] = "racgitameditorial@gmail.com"
  message['subject'] = "From the website"
  body = {'raw': base64.b64encode(message.as_string().encode('utf-8')).decode('utf-8')}

  # send it
  try:
    message = (gmail_service.users().messages().send(userId="me", body=body).execute())
    print('Message Id: %s' % message['id'])
    print(message)
  except Exception as error:
    print('An error occurred: %s' % error)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)