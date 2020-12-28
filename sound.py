from urllib.request import urlopen
import random
import json

# Napster API and API key
API = "https://api.napster.com/v2.2"
APIKEY = "apikey=MmY3Nzg2NjYtYmE1MC00ZGQwLWEyNGItMzYzMGQ2OGMzY2Ey"

def save_trackID(id):
    """Saving Napster's Track ID"""

    # save Napster's track id to a text file
    savior = open('trackIDs.txt', 'a')
    savior.write("{}\n".format(id))
    savior.close()

def getSound_top_tracks():
    """Get Top Napster's Top Track"""

    # Function called check
    print("Adding some more flavors...")

    # Query for Napster top tracks
    query = "/tracks/top?"

    # Url for the API
    url = API + query + APIKEY

    # Open the API URL
    # load Napster's info to Json format
    sound = json.loads(urlopen(url).read())

    # randomly pick a song from Napster's top track
    i = random.randint(0, len(sound['tracks']))

    # If the selected track is not streamable,
    # find another track
    while(sound['tracks'][i]['isStreamable'] != True):
        i = random.randint(0, len(sound['tracks']))

    # Return the publicly-accessible direct URL for the track
    return sound['tracks'][i]['previewURL']

def getSound_random():
    """Get a random track from Napster API"""

    # Function called check
    print("Adding some more flavors...")

    # To get Napster's individual track, we need the
    # id of the track, which usually a 4 to 9 digits number
    id = int((random.random() * 1000000000) % 1000000007)

    # query for Napster's track
    query = "/tracks/tra.{}?".format(id)

    # API url to access Napster's info
    url = API + query + APIKEY

    # load Napster's info to a readable json file
    sound = json.loads(urlopen(url).read())

    # Since Napster's track id are randomly assigned,
    # we need to try all possible ids to find a
    # streamable track on Napster
    while((sound['meta']['returnedCount'] == 0) or
          (sound['tracks'][0]['isStreamable'] != True)):
        id = int((random.random() * 1000000000) % 1000000007)
        query = "/tracks/tra.{}?".format(id)
        url = API + query + APIKEY
        sound = json.loads(urlopen(url).read())

    save_trackID(id)

    # Return the publicly-accessible direct URL for the track
    return sound['tracks'][0]['previewURL']
