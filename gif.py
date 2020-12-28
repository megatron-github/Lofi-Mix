from urllib.request import urlopen
import random
import json

# Giphy API and API key
API = "http://api.giphy.com/v1/gifs/search?"
APIKEY = "&api_key=YOUR_KEY_HERE"

def getGif__with(topic):
    """Get a gif from Giphy with a given topic"""

    # Function called check
    print("Finding a gif for you...")

    #query for desired gif topic
    query = "&q={}".format(topic)

    # URL of the API
    url = API + APIKEY + query

    # Open the API URL
    # Load Gihpy's info to Json format
    gif = json.loads(urlopen(url).read())

    # Raise system error if the given topic has no Gif file
    if(len(gif['data']) == 0):
        raise NameError('The specified query of "{}" for Gif does not exist'.format(topic))

    # Get a random gif from the random topics
    i = int((random.random() * len(gif['data']) + 1) % (len(gif['data']) - 1))

    # Return the publicly-accessible direct URL for the GIF.
    return gif['data'][i]['images']['original']['url']

def getGif_random():
    """Get a random gif from Giphy"""

    # Function called check
    print("Finding a gif for you...")

    # Some cool gif topics
    vocabs = ['lofi', 'chillwave', 'anime', 'ghibli', 'cowboy-bebop', 'naruto',
              'studio-ghibli', 'synthwave', 'shakira', 'emma-watson',
              'my-neighbor-totoro', 'kikis-delivery-service', 'anime-aesthetic',
              'howls-moving-castle']

    # Query for the random topics
    query = "&q=" + random.choice(vocabs)

    # URL of the API
    url = API + APIKEY + query

    # Open the API URL
    # Load Gihpy's info to Json format
    gif = json.loads(urlopen(url).read())

    # Get a random gif from the random topics
    i = int((random.random() * len(gif['data']) + 1) % (len(gif['data']) - 1))

    # Return the publicly-accessible direct URL for the GIF
    return gif['data'][i]['images']['original']['url']
