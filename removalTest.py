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

# function loads all the words into the WORD_BANK list from the file.
def initLoad():
    with open("wordbank.txt", 'r') as file:
        for line in file:
            line = line.rstrip()        # strips word of newline.
            line = line.upper()         # capitalizes everyone.
            WORD_BANK.append(line)
    WORD_BANK.sort()

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
    
    # Parse the word_bank and remove any words that don't contain the letters at the correct index.
    letter = CORRECT_WORD[0][1]
    index = CORRECT_WORD[0][0] - 1
    print("Going to remove {} from {}".format(letter, index))

    for word in TEST_BANK:
        if word[index] != letter:
            TEST_BANK.remove(word)
    print(TEST_BANK)

# CORRECT: GRIPS
# CORRECT_WORD: G R I T S

def main():
    print("Is it running?")
    # initializing our correct word.
    CORRECT_WORD.append((1, 'G'))
    CORRECT_WORD.append((2, 'R'))
    CORRECT_WORD.append((3, 'I'))
    CORRECT_WORD.append((5, 'S'))
    TEST_BANK.append("TESTS")
    TEST_BANK.append("GRIPS")
    TEST_BANK.append("GRITS")
    TEST_BANK.append("GREPS")
    TEST_BANK.append("GREAT")
    TEST_BANK.append("PESTS")
    #testInitCorrectWord()
    removeFromList()

main()