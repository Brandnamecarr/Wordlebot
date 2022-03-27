# Wordle Bot
import requests
from bs4 import BeautifulSoup
import random as rd

# CONSTANTS
WORD_BANK = []
CORRECT_WORD = []   # store correct letters in correct index.
INCORRECT_POSITION = [] 
INCORRECT_LETTERS = []
GAME_URL = "https://www.nytimes.com/games/wordle/index.html"

# initalize the wordbank.
def initLoad():
    with open("wordbank.txt", 'r') as file:
        for line in file:
            line = line.rstrip()        # strips word of newline.
            line = line.upper()
            WORD_BANK.append(line)

# tester function to print the current correct word...
def getCorrectWord():
    if len(CORRECT_WORD) == 0:
        return
    
    retVal = ""
    for i in range(0, len(CORRECT_WORD)):
        index = CORRECT_WORD[i][0]
        letter = CORRECT_WORD[i][1]
        if i == index:
            retVal[i] = letter
        else:
            retVal[i] = 'x'
    print(retVal)


# can check random words for membership.
def checkForMembership(word) -> bool:
    word = word.upper()
    if word in WORD_BANK:
        return True
    else:
        return False

# returns a random string from the current word bank.
def getRandomString() -> str:
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

# checks if the letter is in the tuple, which contains the correct (index, letter).
def existsInTuple(letter) -> bool:
    letter = letter.upper()
    for i in range(0, len(CORRECT_WORD)):
        if letter == CORRECT_WORD[i][-1]:
            return True    
    return False

# checking if a word contains letters that have been found to be in the correct word.
'''
    @returns TRUE: the letter exists in the correct word. do NOT remove from the wordbank.
    @returns FALSE: the letter DNE in the correct word. safe to remove from the wordbank.
'''
def checkLetters(word) -> bool:
    word = word.upper()
    for i in range(0,len(word)):
        if existsInTuple(word[i]) is False:
            return False
        elif existsInTuple(word[i]) is True:
            return True
    
# checking if words exist in the correct place in the word.
'''
    @param: takes in a word to be disassembled and checked.
            if the word does not have letters in the same place as letters in the tuple, returns FALSE.
'''
def checkEach(word) -> bool:
    word = word.upper()
    if len(CORRECT_WORD) == 0:
        return

    for i in range(0, len(CORRECT_WORD)):
        letter = CORRECT_WORD[i][1]
        index = CORRECT_WORD[i][0]
        # print("letter: {}, index: {} word[index]: {}".format(letter, index, word[index]))
        if word[index] != letter:
            # print("Removing {} from the dictionary because {} doesn't equal {}.".format(word, word[index], letter))
            return False

# this function is going to look at the correct letters in their correct index and then remove words from the wordBank if they don't match.
def removeFromWordBank():
    print("Before removal: {}".format(len(WORD_BANK)))
    initLen = len(WORD_BANK)
    if len(CORRECT_WORD) == 0:      # if there is no correct letters, exit
        return
    
    # removes current word doesn't have the right letters.
    for word in WORD_BANK:
        if checkLetters(word) is False:
            WORD_BANK.remove(word)

    print("1st removal call: {}".format(len(WORD_BANK)))

    # removes word if the letters are not in the correct space.
    for word in WORD_BANK:
        if checkEach(word) is False:
            WORD_BANK.remove(word)

    print("AFTER removal: {}".format(len(WORD_BANK)))
    print("Removed a total of {} words!".format(initLen-len(WORD_BANK)))
    print("Current workbank: ")
    print(WORD_BANK)

def cleanUpWordBank():
    removeFromWordBank()

# Function responsible for the runtime of the wordle algorithm.

def play():
    initLoad()
    GUESSES = 6
    while GUESSES > 0:
        print("{} guesses remaining, {} words in the word_bank, correctWord looks like: {}".format(GUESSES, len(WORD_BANK), getCorrectWord()))
        guess_string = getRandomString()
        print("ENTER: {}" .format(guess_string))
        validateResults(guess_string)       # verifying how the first guess went.
        GUESSES = GUESSES - 1
        if GUESSES == 0:
            print("Out of guesses!")
            return
        cleanUpWordBank()

# Tracks the average number of solves to effectively solve the daily Wordle.
def trackMetrics():
    pass

# driver code
def main():
    play()
    #removeFromWordBank()
    WORD_BANK.clear() # remove all from word_bank before exiting.

main()