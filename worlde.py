# World Bot
import re

# CONSTANTS
WORDLE_CHARS = []  # can store correct matches in a tuple:
MISPLACED_CHARS = []
GUESSES = 6

# compares test string with game string and see where misaligned. 
def initialStringCompare(test, actual):

    # checks for CORRECT words.
    for i in range(0, len(test)):  # loop through the size (really, just 5)
        if test[i] == actual[i]:
            temp_tuple = (i, test[i])
            WORDLE_CHARS.append(temp_tuple)
    
    # need to check if the character is in the word, just in the wrong spot.
    for i in range(0, len(test)):
        # calls helper function to return if the character is in the actual word, stores only character not index.
        if checkForMembership(test[i], actual):
            MISPLACED_CHARS.append(test[i])

# helper function to check if a character is IN the actual word.
def checkForMembership(character, actual):
    if character in actual:
        return True
    else:
        return False

# main loop for the execution
def play():
    while GUESSES > 0:
        pass

# driver code
def main():
    play()
    pass