# sandbox for the removal aspect.
import random

WORD_BANK = []
CORRECT_WORD = []   # list of tuples.
TEST_BANK = []

# function writes the contents of the wordbank to the specified filename.
def writeToTestFile(filename):
    counter = 1
    with open(filename, "a+") as file:
        for word in WORD_BANK:
            s = f"{counter}. {word} \n"
            file.write(s)
            s = ""
            counter = counter + 1

def writeToFile(filename, message=None):
    with open(filename, "a+") as file:
        s = f"{message}\n"
        file.write(s)
        s=""

# function loads all the words into the WORD_BANK list from the file.
def initLoad():
    with open("wordbank.txt", 'r') as file:
        for line in file:
            line = line.rstrip()        # strips word of newline.
            line = line.upper()         # capitalizes everyone.
            WORD_BANK.append(line)
    WORD_BANK.sort() #alphabetize. :) 

#generate some fake values for the CORRECT_WORD list.
def testInitCorrectWord():
    entries = int(input("How many letters would you like to initialize in the correct words?"))
    while entries != 0:
        letter = input("What letter would you like to add?")
        index = int(input("What index does this letter belong in? Enter (1-5)"))
        CORRECT_WORD.append((index, letter))
        letter = ''
        index = -1
        entries = entries - 1

    # removes words from the dictionary that don't fit the requirements.
def removeFromList():
    # Base Case: if the dictionary is length 0
    if len(WORD_BANK) == 0:
        return 
    print(len(CORRECT_WORD))

    finished = False
    i = len(CORRECT_WORD)
    j = 0
    while finished != True:
        index = CORRECT_WORD[j][0] - 1
        letter = CORRECT_WORD[j][1]
        #writeToFile("letter_checking.txt", f"index:{index} and letter:{letter}")
        for word in WORD_BANK:
            if word[index] != letter:
                writeToFile("removals.txt", f"{word[index]} != {letter}")
                WORD_BANK.remove(word)
                writeToFile("removals.txt", f"removed {word} from WORD_BANK.")
        i = i - 1
        j = j + 1
        if i == 0:
            finished = True
    print("AFTER REMOVALS:")
    writeToTestFile("removal1.txt")
    print(len(WORD_BANK))

# CORRECT: GRIPS
# CORRECT_WORD: G R I T S

def main():
    WORD_BANK = initLoad()
    print("Length of wordbank {}".format(len(WORD_BANK)))
    testInitCorrectWord()
    removeFromList()

main()