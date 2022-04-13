# Wordle Bot
#import requests
#from bs4 import BeautifulSoup
import random as rd
import logging as log

# CONSTANTS
WORD_BANK = []
CORRECT_WORD = []   # store correct letters in correct index.
INCORRECT_POSITION = [] 
INCORRECT_LETTERS = []
GAME_URL = "https://www.nytimes.com/games/wordle/index.html"

# Logging Messages
# .debug, .info, .warning, .error, .critical
log.basicConfig(filename = 'wordlebot.log', filemode = 'a', format = '%(name)s - %(levelname)s - %(message)s')
log.basicConfig(level = log.DEBUG)

# initalize the wordbank.
def initLoad():
    with open("wordbank.txt", 'r') as file:
        for line in file:
            line = line.rstrip()        # strips word of newline.
            line = line.upper()
            WORD_BANK.append(line)

# can check random words for membership.
def checkForMembership(word) -> bool:
    word = word.upper()
    if word in WORD_BANK:
        return True
    else:
        return False

# returns a random string from the current word bank.
def getRandomString() -> str:
    print(len(WORD_BANK))
    return rd.choice(WORD_BANK)

# could expand service to actually play the game for you.... 
def loadPage():
    page = requests.get(GAME_URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    link = soup.find('game-app')
    for i in link:
        test = link.find("#shadow-root")
        print(test)

# gets user input if letters are in the correct places (for a non-web-interactive program).
def validateResults(guess_string):
    guess_string = guess_string.upper()
    for i in range(0, 5):
        response = input("Is the {} letter in the correct place? (Enter Yes or No)".format((i+1)))
        
        if response.upper() == 'YES':
            CORRECT_WORD.append((i, guess_string[i])) 

        elif response.upper() == 'NO':
            response = input("Does this letter exist elsewhere in the word? (Enter Yes or No)")

            if response.upper() == 'YES':
                INCORRECT_POSITION.append(guess_string[i])

            elif response.upper() == 'NO':
                INCORRECT_LETTERS.append(guess_string[i])


# this function is going to look at the correct letters in their correct index and then remove words from the wordBank if they don't match.
def removeFromWordBank():
    print("Before removal: {}".format(len(WORD_BANK)))
    initLen = len(WORD_BANK)
    if len(CORRECT_WORD) == 0:      # Base Case: if the 'Correct Word' doesn't have any letters, return.
        return
    
    # Case 1: a word in the Word_Bank does not contain a letter at the same index as the Correct Word.
    for word in WORD_BANK:
        for i in range(0, len(CORRECT_WORD)):
            letter = CORRECT_WORD[i][1]
            index = CORRECT_WORD[i][0]
            if word[index] != letter:
                if word in WORD_BANK:
                    WORD_BANK.remove(word)
                else:
                    print("{} Already Removed!".format(word))

def cleanUpWordBank():
    numChecks = 3
    while numChecks > 0:
        removeFromWordBank()
        numChecks = numChecks - 1

# Function responsible for the runtime of the wordle algorithm.

def play():
    initLoad()
    GUESSES = 6
    while GUESSES > 0:
        print("{} guesses remaining, {} words in the word_bank.".format(GUESSES, len(WORD_BANK)))
        guess_string = getRandomString()
        print("ENTER: {}" .format(guess_string))
        validateResults(guess_string)       # verifying how the first guess went.
        GUESSES = GUESSES - 1
        if GUESSES == 0:
            print("Out of guesses!")
            return
        cleanUpWordBank()

# Tracks the average number of solves to effectively solve the daily Wordle.
# open a file in append mode and write the most recent data to the file. 
def trackMetrics():
    pass

# driver code
def main():
    play()
    #removeFromWordBank()
    WORD_BANK.clear() # remove all from word_bank before exiting.

main()