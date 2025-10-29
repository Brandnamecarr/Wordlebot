from wordle import Wordle
import argparse

testMode = False
parser = argparse.ArgumentParser(description='Play Wordle game.')
parser.add_argument('--test', action='store_true', help='Run in test mode')
args = parser.parse_args()
if args.test:
    testMode = True
    print(f"Running in test mode: {testMode}")

# create Worlde object 
worlde = Wordle(testMode)
worlde.play()