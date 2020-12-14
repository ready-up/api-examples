import json
import os
import requests

# The token (API Token) is what we'll use to authenticate so that we can retrieve a list of events.
# API Tokens can be acquired from the ReadyUp Admin UI
TOKEN = os.environ.get('READYUP_TOKEN')
assert TOKEN is not None, 'The "READYUP_TOKEN" environment variable must be set with your ReadyUp API Token'

def list() -> None:
   '''Print out a list of all events that our organization manages'''

   # Make the request to get the listing of events
   r = requests.get('https://api.readyup.com/v1/events', headers = { 'Authoriziation': f'readyup {TOKEN}'})
   assert r.status_code is requests.codes.ok, 'Failed to get events - ensure your TOKEN is valid'

   # At this point we should have an array of events.  Iterate through them and print out some details.
   for event in r.json():
      print(f'Event "{event["title"]}" - starts on {event["startsOn"]}, ends on {event["endsOn"]}')

if __name__ == '__main__':
   list()
