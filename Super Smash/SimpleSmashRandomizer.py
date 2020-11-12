# RNG for Super Smash Bros. Ultimate Characters
from random import randint

# Create list of Smash characters
characters = ["Bayonetta", "Bowser", "Bowser Jr.", "Captain Falcon", "Charizard", "Chrom", "Cloud", "Corrin", "Daisy", "Dark Pit", "Dark Samus", "Diddy Kong", "Donkey Kong", "Dr. Mario", "Duck Hunt", "Falco", "Fox", "Ganandorf", "Greninja", "Ice Climbers", "Ike", "Incineroar", "Inkling", "Isabelle", "Ivysaur", "Jigglypuff", "Ken", "King Dedede", "King K Rool", "Kirby", "Link", "Little Mac", "Lucario", "Lucas", "Lucina", "Luigi", "Mario", "Marth", "Mega Man", "Meta Knight", "Mewtwo", "Mr. Game & Watch", "Ness", "Olimar", "Pac-Man", "Palutena", "Peach", "Pichu", "Pikachu", "Pit", "Richter", "Ridley", "R.O.B.", "Robin", "Rosalina & Luma", "Roy", "Ryu", "Samus", "Sheik", "Shulk", "Simon", "Snake", "Sonic", "Squirtle", "Toon Link", "Villager", "Wario", "Wii Fit Trainer", "Wolf", "Yoshi", "Young Link", "Zelda", "Zero Suit Samus"]

# Gather number of players with default option of 4
numplayers = input("How many players? [4]: ")

# If no input is given, assume default of 4
if numplayers == "":
    for x in range(4):
        print("Player " + str(x + 1) + " : " + characters[randint(0, (len(characters) - 1))])
# Otherwise, cast the given string as an int and iterate through
else:
    try:
        for x in range((int)(numplayers)):
            print("Player " + str(x + 1) + " : " + characters[randint(0, (len(characters) - 1))])
    except:
        print("Not a valid number. Exiting...")
