from fbchat import Client
from fbchat.models import *
import getpass
import time
import re
import random
import json

class IsoSendHelper(Client):

    def __init__(self, user, pw):
        super(IsoSendHelper, self).__init__(user, pw)
        self.latest_message = None
        self.latest_thread_id = None
        self.latest_thread_type = None
        self.latest_author_id = None
        
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
        self.latest_message = message_object
        self.latest_thread_id = thread_id
        self.latest_thread_type = thread_type
        self.latest_author_id = author_id

cookies = None
client = None
try:
    with open('cookies', 'r') as f:
        cookies = json.loads(f.read())
    client = Client('', '', session_cookies=cookies)
except Exception as e:
    user = input('Insert user e-mail: ')
    pw = getpass.getpass('Insert password: ')
    try:
        client = Client(user, pw)
    except Exception as e:
        raise(e)

answers = ["jah", "ei", "võibolla"]

cookies = client.getSession()
with open('cookies', 'w+') as f:
    f.write(json.dumps(cookies))

#client = IsoSendHelper(user, pw)
#client.startListening()
grp = client.searchForGroups('Iso Send Help')[0]
gid = grp.uid
print(gid)
messages = ''
oldmessages = ''
r = re.compile('.*(?:(?:kes|keegi)\s*(?:seltsis|majas)\s*(?:on|ka)|on\s*keegi\s*(?:seltsis|majas)|kes\s*preppab)\s*\?*')
while True:
    messages = client.fetchThreadMessages(thread_id=gid, limit=1)
    newmessages = ''
    for message in messages:
        newmessages += message.text
    if newmessages != oldmessages:
        print(newmessages)
        print()
        if r.match(newmessages.lower()):
            client.send(Message(text='preppar'), thread_id = gid, thread_type=ThreadType.GROUP)
        oldmessages = newmessages
    time.sleep(0.1)
