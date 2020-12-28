from urllib.request import urlopen
from bs4 import BeautifulSoup
import randomwriter
import random
import string
import json
import re

# Wikiquote API
API = "https://en.wikiquote.org/w/api.php?"

def cleanTexts(texts):
    """Edit the given string to make it looks like a
       normal English string"""

    # Since Wikiquote API returns either plain texts
    # or limited HTML extracts of the given query, we may use
    # BeautifulSoup to delete the HTML codes
    texts = BeautifulSoup(texts, "html.parser")

    # Get only the texts that are being displayed on the HTML,
    # delete the HTML codes
    texts = texts.get_text(" ", strip=True)

    # List of Wiki sections that is not relevant to the purpose of
    # finding a quote
    nonContent = ['Cast', 'Discography', 'See Also', 'See also', 'Taglines',
                  'Reference', 'External links']

    # Find the first index where the section
    # of irrelevant begins
    non_i = texts.find('== External links ==')
    for non in nonContent:
        i = texts.find('== {} =='.format(non))
        if (non_i > i) and (i != -1):
            non_i = i

    # delete the irrelevant sections
    texts = texts[:non_i]

    # remove everything between (...), [...], and {...}
    texts = re.sub(r"((\[)+|(\()+|(\{)+|(=)+)(.*?)((\])+|(\))+|(\})+|(=)+)",
                   "", texts)

    # deleting all '...' and back lashes found in the string
    texts = texts.replace('...', '').replace('\\', '')

    # filter out non-Ascii characters
    texts = texts.encode("ascii", errors="ignore").decode()

    # delete all URL link attached
    texts = re.sub(r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))", "", texts)

    # delete all leading and trailing spaces
    texts = " ".join(texts.split())
    return texts

def copyQuote_random(quotes):
    """Randomly pick a starting point from the text file, return a
       string with random length with characters followed the
       starting point"""

    # filter out all of the new line characters and double spaces
    quotes = (quotes.replace('\n', '').replace('\r', '')).replace("  ", " ")

    # filter out non-Ascii characters
    quotes = quotes.encode("ascii", errors="ignore").decode()

    # create the length of the quote
    str_length = random.randint(140, 280)

    # create a random starting index from the source text:
    random_i = int((random.random() * len(quotes)) % (len(quotes) - 280))

    # Goal: while the random seed started anywhere rather than
    # the beginning of a sentence, change the seed. In other
    # words, the seed must start at the beginning of a sentence
    while(quotes[random_i] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        random_i = int((random.random() * len(quotes)) % (len(quotes) - 280))

    # first character at random inde
    seed = quotes[random_i]

    # write the quote with characters followed the seed
    for i in range(1, str_length):
        seed = seed + quotes[random_i + i]

        # if a period is founded, then
        # it is the end of a sentence (ignore "...")
        if quotes[random_i + i] == '.':
            return seed
    return seed

def getQuote_with(topic):
    """Find a quote from quote from API Url
       that include user's desire topic"""

    # Function called check
    print('Adding flavors with "{}"...'.format(topic))

    # Capitalize first letter of all words and replace spaces with underscores
    topic = (string.capwords(topic)).replace(" ", "_")

    # query for desired quote topic
    query = "action=query&prop=extracts&explaintext=true&titles={}&format=json".format(topic)

    # url for the API
    url = API + query

    # load the Wikiquote info to Json format
    response = json.loads(urlopen(url).read())

    # get the search query ID
    pageID = list(response['query']['pages'])[0]

    # Error: Wikiquote does not give quotes for some topics
    # Wrong spelling could also lead to this error
    if(pageId == -1):
        raise NameError('The specified query of "{}" does not exist'.format(topic))

    # edit the string to make it look like a normal English string
    texts = cleanTexts(response['query']['pages'][pageID]['extract'])

    # Some Wikiquote topic has little amount of words.
    # We need a file contain at least 140 words
    if(len(texts) < 140):
        raise NameError('The specified query of "{}" is not long enough'.format(topic))

    # Get a random string (quote) from the source file
    quote = copyQuote_random(texts)
    return (topic, quote)

def getQuote_random():
    """Get quotes from pre-selected topics"""

    # Some cool topics for quotes
    topics = ['Naruto', 'Sun_Tzu', 'Tupac_Shakur', 'Forrest_Gump', 'Lady_Gaga',
              'Moneyball_(film)', 'Barack_Obama', 'Steve_Jobs', 'Stephen_King',
              'Martin_Luther_King,_Jr.', 'Stephen_Hawking', 'Daniel_Kahneman']

    # Randomly choose a topic from the pre-selected list
    topic = random.choice(topics)

    # query for desired quote topic
    query = "action=query&prop=extracts&explaintext=true&titles={}&format=json".format(topic)

    # url for the API
    url = API + query

    # load the Wikiquote info to Json format
    response = json.loads(urlopen(url).read())

    # get the search query ID
    pageID = list(response['query']['pages'])[0]

    # get the Wikiquote's title of the search query
    title = response['query']['pages'][pageID]['title']

    # Function called check
    print('Adding flavors with "{}"...'.format(title))

    # edit the string to make it look like a normal English string
    texts = cleanTexts(response['query']['pages'][pageID]['extract'])

    # create a string of randomly attached strings with random writer file
    quote = copyQuote_random(texts)
    return (title, quote)
