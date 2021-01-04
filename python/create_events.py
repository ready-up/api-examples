import csv
import json
import os
import requests


# The URL we'll use as a base for all API calls to ReadyUp
API_URL = os.environ.get('READYUP_API_URL', 'https://api.readyup.com/v1/')

# The token (API Token) is what we'll use to authenticate so that we can retrieve a list of events.
# API Tokens can be acquired from the ReadyUp Admin UI
TOKEN = os.environ.get('READYUP_TOKEN')
assert TOKEN is not None, 'The "READYUP_TOKEN" environment variable must be set with your ReadyUp API Token'

# The standard header we'll use for ALL API calls to ReadyUp
HEADERS = { 'Authorization': f"readyup {TOKEN}" }


def create_image(file_name: str) -> str:
    """Creates an image in ReadyUp and returns the ID which can be used when creating events

    Parameters:
        file_name - the name of the image file (in our file system) that we want to add to ReadyUp

    Returns: The ID of the image added to ReadyUp
             or None if the image was not added
    """
    headers = { 'content-type': 'image/png', **HEADERS}
    with open(file_name, 'rb') as f:
        data = f.read()

    response = requests.post(f'{API_URL}images', data=data, headers=headers)
    if (response.status_code == 201):
        return response.json()['id']
    else:
        print(f"Failed to upload image '{file_name}'")

    return None

def find_game(game_name: str) -> str:
    """Attempts to find a game based on it's name

    Parameters:
        game_name - the name of the game we want to search for

    Returns: The ID of the game in ReadyUp
             or None if the game is not in the system
    """
    response = requests.get(f'{API_URL}games', params = { 'name': game_name },  headers=HEADERS)
    if (response.status_code == 200):
        return response.json()['id']

    return None

def import_csv(filename: str) -> None:
    """Imports a CSV file of event information, creating one event per row.

    The CSV file must be of the format
    'title','
    """
    assert os.path.exists(filename) and os.path.isfile(filename), f'{filename} does not exist.'

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # First - make sure we have an image we can refer to
            image_file = row['cover'].strip()
            if image_file:
                image_id = create_image(row['cover'])

            # Then - find the ID of the game the tournament is for
            game_id = find_game(row['game'])
            if not game_id:
                print(f"Game '{row['game']}' does not exist - skipping event")
                # continue

            # Then - create an event based on the data in the CSV file
            # title,game,starts_on,ends_on,stream_label,stream_link,cover            
            print(row['title'], row['game'])
            event = {
                'title': row['title'],
                'type': 'tournament',
                'games': [ game_id ],
                'locationType': 'ONLINE',
                'streamLinks': [{ 'label': row['stream_label'], 'url': row['stream_link'] }],
                'cover': image_id,
                'startsOn': row['starts_on'],
                'endsOn': row['ends_on']
            }

            response = requests.post(f'{API_URL}events', json=event, headers=HEADERS)
            if response.status_code == 201:
                print(f"Event '{row['title']}' successfully created.")
            elif response.status_code == 401:
                print(f"Failed to create event '{row['title']}' - check that the authentication token is valid.")
            else:
                print(f"Failed to create event '{row['title']}'.", response.json())


def create() -> None:
    """Creates events by importing them from an example CSV file"""
    import_csv("./data/events.csv")

if __name__ == '__main__':
    import_csv()