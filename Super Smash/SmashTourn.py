from random import randint

# TODO:
# Change winlist to windict and display the match statistics
# Certain aspects only work for two players

characters = ["Bayonetta", "Bowser", "Bowser Jr.", "Captain Falcon", "Charizard", "Chrom", "Cloud", "Corrin", "Daisy", "Dark Pit", "Dark Samus", "Diddy Kong", "Donkey Kong",
                "Dr. Mario", "Duck Hunt", "Falco", "Fox", "Ganandorf", "Greninja", "Ice Climbers", "Ike", "Incineroar", "Inkling", "Isabelle", "Ivysaur", "Jigglypuff", "Ken",
                "King Dedede", "King K Rool", "Kirby", "Link", "Little Mac", "Lucario", "Lucas", "Lucina", "Luigi", "Mario", "Marth", "Mega Man", "Meta Knight", "Mewtwo",
                "Mr. Game & Watch", "Ness", "Olimar", "Pac-Man", "Palutena", "Peach", "Pichu", "Pikachu", "Pit", "Richter", "Ridley", "R.O.B.", "Robin", "Rosalina & Luma", "Roy", "Ryu",
                "Samus", "Sheik", "Shulk", "Simon", "Snake", "Sonic", "Squirtle", "Toon Link", "Villager", "Wario", "Wii Fit Trainer", "Wolf", "Yoshi", "Young Link", "Zelda", "Zero Suit Samus"]

class Player:
    def __init__(self,name):
        self.name = name
        self.characterlist = []
        self.id = id
        self.wins = 0
        self.winlist = []
        self.randomnum = 0
        self.wonagainstdict = {}
        self.makeCharacterList()

    def makeCharacterList(self):
        for character in characters:
            self.characterlist.append(character)

def playGame():
    playerdict = {}
    winner = ""
    player = ""
    playerlist = []
    samelist = []
    beatlist = []

    # Enter player names
    while player != "0":
        player = input("Enter player names or '0' if done: ")
        if player != "0":
            playerlist.append(player)
    print("\n")

    # Create player objects and add them to the player dictionary w/ key = string of player name and value = player object
    for name in playerlist:
        playerdict[name] = Player(name)

    # Begin run time
    while 1 == 1:
        # The character lists for every player decrement by one each round. When their length equals 0, stop the game and print results
        if len(playerdict[playerlist[0]].characterlist) == 0:
            print("Game Over! Here are the standings...\n")
            for x,y in playerdict.items():
                print(x + "'s wins = " + str(y.wins))
                print(x + " won with these characters: " + str(y.winlist))
                for c,w in wonagainstdict.items():
                    print(c + " beat " + w)
            return
        # Post an update after every five rounds
        elif len(playerdict[playerlist[0]].characterlist) % 5 == 0:
            for x, y in playerdict.items():
                print(x + " Checkpoint...\n")
                print(x + " won with these characters: " + str(y.winlist))
                print(x + " has these characters left to play: " + str(y.characterlist) + "\n")

        # Display randomly selected characters per player
        for x,y in playerdict.items():
            y.randomnum = randint(0,(len(y.characterlist) - 1))
            print(x + ": " + y.characterlist[y.randomnum])

        # Begin "Who won" scenario
        answer = False
        while answer == False:
            try:
                # Prompt for winner
                winner = input("\nWho won? (Enter 'quit' to quit and 'update' to get standings) ")

                # Escape method if "quit" is entered
                if winner == "quit":
                    return

                # Print current details if "update" is entered
                elif winner == "update":
                    print("There are " + str(len(playerdict.get(playerlist[0]).characterlist)) + " characters left")
                    for x,y in playerdict.items():
                        print(x + "'s wins = " + str(y.wins))
                        print(x + "'s remaining characters: " + str(y.characterlist) + "\n")
                    for x,y in playerdict.items():
                        try:
                            print("\n" + x + "'s winners - ")
                            for key, value in y.wonagainstdict.items():
                                print("\t" + str(key) + " beat " + str(value))
                        except Exception as e:
                            print(e)

                # Update scenario attributes if valid name is entered
                else:
                    beatlist = []
                    playerdict[winner].wins += 1
                    playerdict[winner].winlist.append(playerdict[winner].characterlist[playerdict[winner].randomnum])

                    #################################################
                    # BUGS - beatlist contains the winning character
                    # key = playerdict[winner].characterlist[playerdict[winner].randomnum] (The character that the player won with)
                    # value = (a for loop iterating through the players that didn't win and their characterlists randomnum values) (The characters that the winning player's character beat)
                    for x,y in playerdict.items():
                        if x != playerdict[winner]:
                            beatlist.append(y.characterlist[y.randomnum])
                    playerdict[winner].wonagainstdict[playerdict[winner].characterlist[playerdict[winner].randomnum]] = beatlist
                    ##################################################

                    # Display wins and remove the played characters from each player's respective character list
                    for x,y in playerdict.items():
                        del y.characterlist[y.randomnum]

                    print("\n")
                    answer = True

            # Throw exception if name doesn't exist in playerlist or error occurs within other if statements and reprompt
            except:
                print("Error. Try again...")

playGame()
