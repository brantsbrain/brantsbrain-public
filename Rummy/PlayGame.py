import random
from Rummy import *

drawpile = [[1,"S"],[2,"S"],[3,"S"],[4,"S"],[5,"S"],[6,"S"],[7,"S"],[8,"S"],[9,"S"],[10,"S"],[11,"S"],[12,"S"],[13,"S"],
        [1,"C"],[2,"C"],[3,"C"],[4,"C"],[5,"C"],[6,"C"],[7,"C"],[8,"C"],[9,"C"],[10,"C"],[11,"C"],[12,"C"],[13,"C"],
        [1,"H"],[2,"H"],[3,"H"],[4,"H"],[5,"H"],[6,"H"],[7,"H"],[8,"H"],[9,"H"],[10,"H"],[11,"H"],[12,"H"],[13,"H"],
        [1,"D"],[2,"D"],[3,"D"],[4,"D"],[5,"D"],[6,"D"],[7,"D"],[8,"D"],[9,"D"],[10,"D"],[11,"D"],[12,"D"],[13,"D"]]

# Shuffle deck
random.shuffle(drawpile)

def playGame():
    player = ""
    playerlist = []
    playerdict = {}
    seat = 1
    hand = 0

    # Enter and append player names to playerlist
    while player != "0":
        player = input("Enter player names or '0' if done: ")
        if player != "0":
            playerlist.append(player)
    print("\n")

    # Create playerdict and Player objects
    for name in playerlist:
        playerdict[name] = Player(name, seat)
        seat += 1

    # Deal first hand to all players
    while hand < 7:
        for x,y in playerdict.items():
            y.hand.append(drawpile.pop())
        hand += 1

    # Print first hand
    for x,y in playerdict.items():
        print(x + "'s hand: " + str(y.hand))
    print("Remaining cards: " + str(len(drawpile)))

    while True:
        for x,y in playerdict.items():
            y.checkRun()
        break

playGame()
