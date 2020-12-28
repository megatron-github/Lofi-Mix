import gif
import quote
import sound
import webbrowser

def makeweb():
    """Create web page with a gif and a dubbed song"""

    # Retrieve a gif URL from Giphy
    gif_url = gif.getGif_random()

    # Retrieve a string from Wikiquote
    # to create a quote
    author, quote_str = quote.getQuote_random()

    # Retrieve a song URL from Napster to add flavor
    sound_url = sound.getSound_random()

    # Read the a formatted html
    with open('format.html', 'r') as info:
        webmaker = info.read().format(gif_url, author, quote_str, sound_url)

    # Create an html file with the Gif and Song URL
    # using a formatted html file
    with open('gif.html','wb') as publisher:
        publisher.write(webmaker.encode())
        publisher.close()
        
    print("Enjoy!")

    # Open the newly created html file
    # to watch the gif and listen to the track
    webbrowser.open('gif.html')

def main():
    """Main function"""
    
    makeweb()

main()
