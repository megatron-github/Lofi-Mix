import random

def seed_generator(essay, seed_length=1):
    """generate random seed from the give text file to start
       random writer"""

    # generate a random index
    random_i = int((random.random() * len(essay)) % (len(essay) - 280))

    # Goal: while the random seed started anywhere rather than
    # the beginning of a sentence, change the seed. In other
    # words, the seed must start at the beginning of a sentence
    while(essay[random_i] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        random_i = int((random.random() * len(essay)) % (len(essay) - 280))

    # get the character at the random index
    seed = essay[random_i]

    # add new characters (that followed the index of the random character)
    # until the seed have the desired length
    for i in range(1, seed_length):
        seed = seed + essay[random_i + i]
    return seed

def get_new_char(essay, seed):
    """Add a followed character into a given seed,
       then delete the first character of the seed
       to keep the length of the seed constant"""

    # generate a random index
    random_i = int(random.random() * len(essay)) % len(essay)

    # get the character at the random index
    seed = seed + essay[random_i]
    return seed

def seed_in_text_at(index, seed_length, seed, essay):
    """Return True if the seed is found in the text file at the give index.
       Otherwise, False"""

    # For each characters in the given seed
    for i in range(0, seed_length):

        # At given index, check if the i-th character of the seed is
        # the same character of the text file at index + ith position
        if(essay[index + i] != seed[len(seed) + i - seed_length]): return False
    return True

def pick_a_quote(essay, seed, seed_length):
    """In the text file, look for a sequence of characters that resemble the
       given seed, and save all the characters that that often follow the
       sequence, then randomly pick a characters and add it to the seed"""

    characters = []      # list of characters

    # go to through the text file and
    # look for a sequence that resemble the seed
    for i in range(0, len(essay) - seed_length):

        # when the first character of the seed is found in the text file
        if(essay[i] == seed[0]):

            # If the seed length is one or less, than we have found
            # the following character of the seed
            if(seed_length <= 1):
                characters.append(essay[i + 1])

            # If the seed length is greater than one, then we have to
            # check whether the following characters in the text file
            # match with the characters from the seed
            elif(seed_in_text_at(i + 1, seed_length - 1, seed, essay)):

                # if, at the given index i, the a sequence of characters
                # similar to the seed is found, save the following
                # character of the seed
                characters.append(essay[i + seed_length])

    # special case: if there is no possible character to follow the seed,
    # the program will create a new seed from the input text
    if(len(characters) < 1):
        seed = " " + seed_generator(essay, seed_length - 1)
        return seed

    # randomly add a characters from all characters
    # that often follow the seed into the seed
    seed = get_new_char(characters, seed)

    # keeping length of the seed constant
    return seed[1:]

def write(essay, seed_length, string_length):
    """Create a string of given string_length using a seed_length seed
       and source text from given text file"""

    # Error: Seed length and output length cannot be smaller than 0
    if((string_length < 0) or (seed_length < 0)):
        raise NameError('"String Length" or "Seed Length" must be positive')

    # Error: Seed length cannot be greater than Output length
    if(string_length < seed_length):
        raise NameError('"Seed Length" cannot be greater than "Seed Length"')

    # Error: Seed length cannot be greater than the size of the source text
    if(len(essay) <= seed_length):
        raise NameError('The source text file should contains more than {} characters'.format(seed_length))

    # If given string length is 0, return empty string
    if(string_length == 0): return ""

    # Seed length must be 1 in order to start writing
    if(seed_length == 0): seed_length = 1

    # get a seed_length seed
    seed = seed_generator(essay, seed_length)
    quote = seed

    # create a string of given string_length
    for i in range(0, string_length - seed_length):
        seed = pick_a_quote(essay, seed, seed_length)

        # add the last character of the seed to the quote
        # since it is the only new character
        quote = quote + seed[-1]

        # if a period is found, then it is the end of a quote
        if seed[-1] == '.': return quote
    return quote
