# Wordle Bot

import random as rd
import logging as log
import os

# CONSTANTS
WORD_BANK = []
CORRECT_WORD = 'XXXXX'
INCORRECT_POSITION = [] 
INCORRECT_LETTERS = []
GAME_URL = "https://www.nytimes.com/games/wordle/index.html"


# initalize the wordbank.
def initWordbank():
    try:
        with open("wordbank.txt", 'r') as file:
            for line in file:
                line = line.rstrip()        # strips word of newline.
                line = line.upper()
                WORD_BANK.append(line)
        log.info("initWordbank() -> just added {} words.".format(len(WORD_BANK)))
    except FileNotFoundError:
        log.error("initwordbank() -> {} not found.".format('wordbank.txt'))

# returns a random string from the current word bank.
def getRandomString() -> str:
    return rd.choice(WORD_BANK)

# gets user input if letters are in the correct places
def validateResults(guess_string):
    user_input = input("Enter (Y if letter matches) (N if no match) (M if exists in word)")
    log.info("validateResults() -> user just entered: {}".format(user_input))

    for i in range(0, len(user_input)):
        if user_input[i] == 'y' or user_input[i] == 'Y':
            log.debug("validateResults() -> i: {}, CORRECT_WORD[i]: {}, guess_string[i]: {}".format(i, CORRECT_WORD[i], guess_string[i]))
            CORRECT_WORD = CORRECT_WORD[:i] + guess_string[i] + CORRECT_WORD[i+1:]
            log.debug("validateResults() -> Added {} to the CORRECT_WORD at position {}".format(guess_string[i], i))
        elif user_input[i] == 'n' or user_input[i] == 'N':
            log.debug("validateResults() -> removing {} because user input was N".format(guess_string[i]))
            # need to remove the letter from any word where it has this letter in this spot.
            removeFromWordBank(guess_string[i], i)
        elif user_input[i] == 'm' or user_input[i] == 'M':
            log.debug("validateResults() -> letter {} in incorrect position.".format(user_input[i]))
        else:
            log.error("validateResults() -> Error: incorrect character entered.")


# removes words from word bank who have letter in this index.
def removeFromWordBank(letter: str, index: int):
    current_size = 0
    try:
        current_size = len(WORD_BANK)
        log.debug("removeFromWordBank() -> {} words before removal.".format(len(WORD_BANK)))
    except:
        log.error("removeFromWordBank() -> error getting length from WORD_BANK")
    

    override_word_bank = []
    # iterate through the word bank and check if words have the letter at the index.
    for word in WORD_BANK:
        if word.find(letter) == index:
            log.debug("removeFromWordBank() -> removing {}... has {} at index {}".format(word, letter, index))
        else:
            override_word_bank.append(word)
    
    WORD_BANK.clear()
    WORD_BANK = override_word_bank

    log.debug("removeFromWordBank() -> {} words after removal.".format(len(WORD_BANK)))
    
def clear_logs():
    if os.path.exists("./wordlebot.log"):
        os.remove("./wordlebot.log")
        log.info("CLEANED UP LOG FILE")
    else:
        log.error("COULDN'T FIND LOG FILE")

def play():
    
    initWordbank()
    GUESSES = 6
    while GUESSES > 0:
        print("{} guesses remaining, {} words in the word_bank.".format(GUESSES, len(WORD_BANK)))
        guess_string = getRandomString().upper()
        log.info("play() -> generated random string: {}".format(guess_string))
        print("ENTER: {}" .format(guess_string))
        validateResults(guess_string)       # verifying how the first guess went.
        GUESSES = GUESSES - 1
        if GUESSES == 0:
            print("Out of guesses!")
            return

# Tracks the average number of solves to effectively solve the daily Wordle.
# open a file in append mode and write the most recent data to the file. 
def trackMetrics():
    pass

# driver code
def main():

    play()
    #removeFromWordBank()
    WORD_BANK.clear() # remove all from word_bank before exiting.

# Logging Messages
# .debug, .info, .warning, .error, .critical
clear_logs()
log.basicConfig(filename = 'wordlebot.log', level=log.DEBUG, format = '%(levelname)s - %(message)s')
main()