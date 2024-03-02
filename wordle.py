# Wordle Bot

import random as rd
import logging as log
import os


class Wordle:

    # constants
    WORD_BANK = []
    CORRECT_WORD = 'XXXXX'


    # vars
    filename = ''
    logFilename = ''
    GUESSES = 6

    # constructor 
    def __init__(self):
        self.filename = 'wordbank.txt'
        self.logFilename = 'wordlebot.log'
        self.clear_logs()
        # Logging Messages
        # .debug, .info, .warning, .error, .critical
        log.basicConfig(filename = self.logFilename, level=log.DEBUG, format = '%(levelname)s - %(message)s')

    # initalize the wordbank.
    def initWordbank(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    line = line.rstrip()        # strips word of newline.
                    line = line.upper()
                    self.WORD_BANK.append(line)
            log.info("initWordbank() -> just added {} words.".format(len(self.WORD_BANK)))
            log.info("initWordbank() -> random word to see if its capitalized: {}".format(rd.choice(self.WORD_BANK)))
        except FileNotFoundError:
            log.error("initwordbank() -> {} not found.".format(self.filename))

    # returns a random string from the current word bank.
    def getRandomString(self) -> str:
        return rd.choice(self.WORD_BANK)

    # gets user input if letters are in the correct places
    def validateResults(self, guess_string):
        user_input = input("Enter (Y if letter matches) (N if no match) (M if exists in word)")
        log.info("validateResults() -> user just entered: {}".format(user_input))

        for i in range(0, len(user_input)):
            if user_input[i] == 'y' or user_input[i] == 'Y':
                log.debug("validateResults() -> i: {}, CORRECT_WORD[i]: {}, guess_string[i]: {}".format(i, self.CORRECT_WORD[i], guess_string[i]))
                self.CORRECT_WORD = self.CORRECT_WORD[:i] + guess_string[i] + self.CORRECT_WORD[i+1:]
                log.debug("validateResults() -> Added {} to the CORRECT_WORD at position {}".format(guess_string[i], i))
                log.debug("validateResults() -> CORRECT_WORD is now: {}".format(self.CORRECT_WORD))
            elif user_input[i] == 'n' or user_input[i] == 'N':
                log.debug("validateResults() -> removing {} because user input was N".format(guess_string[i]))
                # need to remove the letter from any word where it has this letter in this spot.
                self.removeFromWordBank(guess_string[i], i)
            elif user_input[i] == 'm' or user_input[i] == 'M':
                log.debug("validateResults() -> letter {} in incorrect position, but exists in the word.".format(guess_string[i]))
                # since letter exists in the word, need to remove words from word_bank that don't contain that letter
                log.debug("validateResults() -> CORRECT_WORD is now: {}".format(self.CORRECT_WORD))
            else:
                log.error("validateResults() -> Error: incorrect character entered.")


    # removes words from word bank who have letter in this index.
    def removeFromWordBank(self, letter: str, index: int):
        current_size = 0
        try:
            current_size = len(self.WORD_BANK)
            log.debug("removeFromWordBank() -> {} words before removal.".format(len(self.WORD_BANK)))
        except:
            log.error("removeFromWordBank() -> error getting length from WORD_BANK")
        

        override_word_bank = []
        # iterate through the word bank and check if words have the letter at the index.
        for word in self.WORD_BANK:
            if word.find(letter) == index:
                log.debug("removeFromWordBank() -> removing {}... has {} at index {}".format(word, letter, index))
            else:
                override_word_bank.append(word)
        
        self.WORD_BANK.clear()
        self.WORD_BANK = override_word_bank

        log.debug("removeFromWordBank() -> {} words after removal.".format(len(self.WORD_BANK)))
    
    # removes word from wordbank if it doesn't contain a letter
    def removeWordIfDoesntHaveLetter(self, letter: str):
        current_size = 0
        try:
            current_size = len(self.WORD_BANK)
            log.debug("removeWordIfDoesntHaveLetter() -> {} words before removal.".format(len(self.WORD_BANK)))
        except:
            log.error("removeWordIfDoesntHaveLetter() -> error getting length from WORD_BANK")

        override_word_bank = []
        # iterate through the word bank and check if words have the letter at the index.
        for word in self.WORD_BANK:
            # if finding the letter does NOT return -1, that means it exists in the word somewhere
            if word.find(letter) == -1:
                log.debug("removeWordIfDoesntHaveLetter() -> removing {}... does NOT contain letter {}".format(word, letter))
            else:
                override_word_bank.append(word)
        
        self.WORD_BANK.clear()
        self.WORD_BANK = override_word_bank

        log.debug("removeWordIfDoesntHaveLetter() -> {} words after removal.".format(len(self.WORD_BANK)))
    
    # deletes log file between runs for easy debug effort.
    def clear_logs(self):
        if os.path.exists(self.logFilename):
            os.remove(self.logFilename)

    def play(self):
        
        self.initWordbank()
        GUESSES = 6
        while GUESSES > 0:
            print("{} guesses remaining, {} words in the word_bank.".format(GUESSES, len(self.WORD_BANK)))
            guess_string = self.getRandomString().upper()
            log.info("play() -> generated random string: {}".format(guess_string))
            print("ENTER: {}" .format(guess_string))
            self.validateResults(guess_string)       # verifying how the first guess went.
            GUESSES = GUESSES - 1
            if GUESSES == 0:
                print("Out of guesses!")
                return

    # Tracks the average number of solves to effectively solve the daily Wordle.
    # open a file in append mode and write the most recent data to the file. 
    def trackMetrics(self):
        pass

# --------------------------------- END OF CLASS DEFINITION -----------------------------------------------------------------------



wordle = Wordle()
wordle.play()