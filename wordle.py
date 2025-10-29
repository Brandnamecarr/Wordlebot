# Wordle Bot

import random as rd
import logging as log
import os
import json
from datetime import datetime

# --------------------------------- WordleMetrics CLASS DEFINITION -----------------------------------------------------------------------
class WorldeMetrics:
    total_games = 0
    total_wins = 0
    total_losses = 0
    total_guesses = 0
    average_guesses_per_win = 0.0
    correct_letter_guesses = 0

    def __init__(self):
        self.total_games = 0
        self.total_wins = 0
        self.total_losses = 0
        self.total_guesses = 0
        self.average_guesses_per_win = 0.0
        self.correct_letter_guesses = 0

    def keepRecords(self):
        self.initFromFile('Metrics.json')

    def updateRecords(self, data: dict):
        self.total_games += data.get('total_games', 0)
        self.total_wins += data.get('total_wins', 0)
        self.total_losses += data.get('total_losses', 0)
        self.total_guesses += data.get('total_guesses', 0)
        self.correct_letter_guesses += data.get('correct_letter_guesses', 0)
        if self.total_wins > 0:
            self.average_guesses_per_win = self.total_guesses / self.total_wins
        else:
            self.average_guesses_per_win = 0.0
        self.writeToFile('Metrics.json')
    
    def writeToFile(self, filename: str):
        data = {
            'timestamp': datetime.now().isoformat(),
            'total_games': self.total_games,
            'total_wins': self.total_wins,
            'total_losses': self.total_losses,
            'total_guesses': self.total_guesses,
            'average_guesses_per_win': self.average_guesses_per_win
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        file.close()
    
    def initFromFile(self, filename: str):
        with open(filename, 'r') as file:
            data = json.load(file)
            self.total_games = data.get('total_games', 0)
            self.total_wins = data.get('total_wins', 0)
            self.total_losses = data.get('total_losses', 0)
            self.total_guesses = data.get('total_guesses', 0)
            self.average_guesses_per_win = data.get('average_guesses_per_win', 0.0)
            self.correct_letter_guesses = data.get('correct_letter_guesses', 0)
        file.close()

# --------------------------------- END OF WordleMetrics CLASS DEFINITION -----------------------------------------------------------------------

# --------------------------------- Wordle CLASS DEFINITION -----------------------------------------------------------------------
class Wordle:

    # game mode
    testMode = False

    # constants
    WORD_BANK = []
    CORRECT_WORD = '00000'      # will be updated as letters are found in correct positions.
    CORRECT_WORD_IN_TUPLE = []
    RIGHT_LETTER_WRONG_POSITION = {}

    # vars
    filename = ''
    logFilename = ''
    GUESSES = 5

    # metrics tracker:
    recordKeeper = WorldeMetrics()

    # constructor 
    def __init__(self, testMode):
        self.filename = 'wordbank.txt'
        self.logFilename = 'wordlebot.log'
        self.testMode = testMode

        # remove log file if exists
        if os.path.exists(self.logFilename):
            os.remove(self.logFilename)
            print('Removed old log file.')
        
        # starts the recorder. 
        # TODO: make this configurable maybe?
        self.recordKeeper.keepRecords()
        
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
        except FileNotFoundError:
            log.error("initwordbank() -> {} not found.".format(self.filename))
            print("Error: wordbank.txt not found.")
            exit(1)

    # returns a random string from the current word bank.
    def getRandomString(self) -> str:
        return rd.choice(self.WORD_BANK)

    # gets user input if letters are in the correct places
    def validateResults(self, guess_string):
        if len(guess_string) != 5:
            log.error("validateResults() -> guess_string length is not 5.")
            exit(1)
        
        # loop through each letter in the guess string
        for i in range(0, len(guess_string)):
            
            user_input = input(f"Enter (Y if letter {guess_string[i]} matches) (N if no match) (M if exists in word)")
            log.debug("validateResults() -> user just entered: {}".format(user_input))
            user_input = user_input.strip()    # remove any whitespace/newline characters
            # YES -> the letter is in the correct position
            if user_input == 'y' or user_input == 'Y':
                log.debug("validateResults() -> i: {}, CORRECT_WORD[i]: {}, guess_string[i]: {}".format(i, self.CORRECT_WORD[i], guess_string[i]))
                
                self.CORRECT_WORD_IN_TUPLE.append((i, guess_string[i]))
                log.debug("validateResults() -> Added {} to the CORRECT_WORD at position {}".format(guess_string[i], i))
                log.debug("validateResults() -> CORRECT_WORD_IN_TUPLE is now: {}".format(self.CORRECT_WORD_IN_TUPLE)) 

            # NO -> the letter is NOT in the word at all
            elif user_input == 'n' or user_input == 'N':
                log.debug("validateResults() -> removing {} because user input was N".format(guess_string[i]))
                # need to remove the letter from any word where it has this letter in this spot.
                self.removeWordIfDoesntHaveLetter(guess_string[i])

            # MAYBE -> the letter is in the word, but not in this position
            elif user_input == 'm' or user_input == 'M':
                log.debug("validateResults() -> letter {} in incorrect position, but exists in the word.".format(guess_string[i]))
                # add to the dictionary of letters by <letter, list of indices> of where the letter was in the wrong place.
                self.RIGHT_LETTER_WRONG_POSITION[guess_string[i]].append(i)
                # remove words that have this letter in this index cuz it's wrong
                self.removeFromWordBank(guess_string[i], i) 

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

    def displayCurrentWord(self):
        if len(self.CORRECT_WORD_IN_TUPLE) == 0:
            print(f"There are no correctly guessed words...")
            print("Let's try generating a new word...")
            print(f"-------------------------------------")
            print(f"Guess this word: {self.getRandomString().upper()}")
        
        else:
            print(f"Correctly guessed letters so far: ")
            print(f"So your word would look something like this: {self.makeWordFromTuple().upper()}")
            print(f"-------------------------------------")
            print(f"Guess this word: {self.getRandomString().upper()}")
    
    # a helper to make a word-as-a-string from the tuple
    def makeWordFromTuple(self) -> str:
        word = ""
        for i in range(0, 5):
            if not any(x[0] == i for x in self.CORRECT_WORD_IN_TUPLE):
                word += "?"
                log.debug('makeWordFromTuple() -> no letter found for position {}, adding ?'.format(i))
            else:
                word += self.CORRECT_WORD_IN_TUPLE[i][1]
                log.debug('makeWordFromTuple() -> found letter {} for position {}, adding it.'.format(self.CORRECT_WORD_IN_TUPLE[i][1], i))
        return word
    
    # check if word is solved
    def isSolved(self) -> bool:
        if len(self.CORRECT_WORD_IN_TUPLE) != 5:
            return False
        
        for i in range(0, 5):
            if self.CORRECT_WORD_IN_TUPLE[i][0] != i:
                return False
        
        return True
            
    def play(self):
        
        self.initWordbank()
        guess_string = self.getRandomString().upper()
        log.info("play() -> generated random string: {}".format(guess_string))
        print(f"First Guess: {guess_string}")

        while self.GUESSES != 0 and not self.testMode:
            # verifying how the first guess went.
            self.validateResults(guess_string)       
            self.GUESSES -= 1
            log.info("play() -> {} guesses remaining.".format(self.GUESSES))
            if self.GUESSES == 0:
                print("Out of guesses!")
                log.info("play() -> out of guesses, exiting...")
                return
            
            if self.GUESSES != 0:
                if self.isSolved():
                    print("Congratulations! You've solved the Wordle!")
                    print("Your word was: {}".format(self.makeWordFromTuple()))
                    log.info("play() -> Wordle solved successfully.")
                    log.debug(f'play() -> solved word: {self.makeWordFromTuple()}')
                    return
                print("Here is the result of your first round...")
                self.displayCurrentWord()
                
        
        if self.testMode:
            log.info('play() -> running in testMode')
            while self.GUESSES != 0:
                self.validateResults(guess_string)       
                self.GUESSES -= 1
                log.info("play() -> {} guesses remaining.".format(self.GUESSES))
                if self.GUESSES == 0:
                    print("Out of guesses!")
                    log.info("play() -> out of guesses, exiting...")
                    return
                
                if self.GUESSES > 0:
                    print("Here is the result of your first round...")
                    self.displayCurrentWord()
            
            

    # Tracks the average number of solves to effectively solve the daily Wordle.
    # open a file in append mode and write the most recent data to the file. 
    def trackMetrics(self):
        pass

# --------------------------------- END OF CLASS DEFINITION -----------------------------------------------------------------------



# wordle = Wordle()
# wordle.play()