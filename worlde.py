# Wordle Bot
import requests
from bs4 import BeautifulSoup
import pyautogui

# CONSTANTS
WORD_BANK = []
GUESSES = 6
GAME_URL = "https://www.nytimes.com/games/wordle/index.html"

#initalize the wordbank.
def initLoad():
    with open("Wordlebot\wordbank.txt", 'r') as file:
        for line in file:
            line = line.rstrip()        # strips word of newline.
            WORD_BANK.append(line)

def checkForMembership(s):
    if s in WORD_BANK:
        return True
    else:
        return False

def loadPage():
    page = requests.get(GAME_URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    link = soup.find('game-app')
    for i in link:
        test = link.find("#shadow-root")
        print(test)

# driver code
def main():
    initLoad()
    loadPage()

main()