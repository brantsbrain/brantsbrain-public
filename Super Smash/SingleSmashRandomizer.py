# Single player Smash randomizer that records progress and picks up where you left off

# Needed imports for script
from random import randint
from datetime import datetime
import os

# List of all characters in Super Smash Bros.
characters = ["Bayonetta", "Bowser", "Bowser Jr.", "Captain Falcon", "Charizard", "Chrom", "Cloud", "Corrin", "Daisy", "Dark Pit", "Dark Samus", "Diddy Kong", "Donkey Kong",
                "Dr. Mario", "Duck Hunt", "Falco", "Fox", "Ganandorf", "Greninja", "Ice Climbers", "Ike", "Incineroar", "Inkling", "Isabelle", "Ivysaur", "Jigglypuff", "Ken",
                "King Dedede", "King K Rool", "Kirby", "Link", "Little Mac", "Lucario", "Lucas", "Lucina", "Luigi", "Mario", "Marth", "Mega Man", "Meta Knight", "Mewtwo",
                "Mr. Game & Watch", "Ness", "Olimar", "Pac-Man", "Palutena", "Peach", "Pichu", "Pikachu", "Pit", "Richter", "Ridley", "R.O.B.", "Robin", "Rosalina & Luma", "Roy", "Ryu",
                "Samus", "Sheik", "Shulk", "Simon", "Snake", "Sonic", "Squirtle", "Toon Link", "Villager", "Wario", "Wii Fit Trainer", "Wolf", "Yoshi", "Young Link", "Zelda", "Zero Suit Samus"]

# Method that runs the game
def playGame():
    ########## PREP WORK ##########
    # Replicate characters and declare/instantiate needed variables
    characterlist = characters
    playerfile = ""
    filedict = {}
    filenum = 1
    name = input("Enter singleplayer name: ")

    # Add any CSV files in the current directory as value to dictionary w/ key equal to a number
    for file in os.listdir():
        if file.endswith(".csv"):
            filedict[filenum] = file
            filenum += 1

    # If there aren't any files in the dictionary, skip choosing one
    if len(filedict) == 0:
        chosenfile = 0
    # else print the dictionary and ask which to use or offer to create a new one
    else:
        for file in filedict.items():
            print(f"{file}\n")
        try:
            chosenfile = int(input("Which file would you like to use? Enter the number or 0 for new file: "))
        except Exception as e:
            print(f"Error occured: {e}")

    # If creating new one, assign naming convention and make writeable
    if chosenfile == 0:
        playerfile = f"{name}_{datetime.strftime(datetime.today(), '%m%d%Y_%H%M')}.csv"
        writetype = "w"
    # else assign name, make appendable, read lines from chosen file, and remove recorded characters from character list
    else:
        playerfile = filedict[chosenfile]
        writetype = "a"
        with open(playerfile, "r") as reader:
            lines = reader.readlines()
        for line in lines:
            try:
                characterlist.remove(line.strip())
            except Exception as e:
                print(f"Error occurred: {e}")

    ########## BEGIN GAME ##########
    # Open the chosen file and begin iterating through remaining characters
    with open(f".\\{playerfile}", writetype) as writer:
        # True is always true, so this is an indefinite loop
        while True:
            # Exit if there aren't any characters left
            if len(characterlist) == 0:
                print("Game Over...")
                return
            # Print stats if length of list is divisble by five
            elif len(characterlist) % 5 == 0:
                print(f"Number of characters left: {len(characterlist)}")
                print(f"Characters left to play:\n{characterlist}")

            # Pick a random index and print the character list value of that index
            randomnum = randint(0, len(characterlist) - 1)
            print(f"Play {characterlist[randomnum]}")

            # Pause as user plays that character. Wait to write the character until user presses enter
            pause = input("Press enter when ready for next player or Q and enter to quit... ")

            # Quit if player entered "q"
            if pause.upper() == "Q":
                print("Exiting...")
                return

            # Write the character and delete from the list now that the user pressed enter
            writer.write(f"{characterlist[randomnum]}\n")
            del characterlist[randomnum]

# Start the game
playGame()
