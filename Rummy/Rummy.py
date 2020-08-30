from itertools import permutations

class Player:
    # Player should have a name, seat position, and an empty hand to start
    def __init__(self, name, seat):
        self.name = name
        self.seat = seat
        self.hand = []

    # Player should be able to check if a meld is possible each turn
    def checkMeld(self):
        allpermlist = []
        for num in range(len(self.hand) + 1):
            perm = permutations(self.hand, num)
            permutationlist = list(perm)
            allpermlist += permutationlist
        for index in allpermlist:
            if len(index) == 3:
                if checkStraight(index) or checkThree(index):
                    return index

    # Check to see if a straight exists
    def checkStraight(self, cards):
        firstcard = cards[0]
        cardval = cards[0][0]
        for card in cards:
            if card == firstcard:
                pass
            elif cardval + 1 == card[0]:
                # Revise logic
                pass

    # Check to see if three of a kind exists
    def checkThree(self, cards):
        firstcard = cards[0]
        cardval = cards[0][0]
        for card in cards:
            if card == firstcard:
                pass
            elif card[0] != cardval
                return False
        return True

# class Card:
#     def __init__(self,label,suit,value):
#         self.label = label
#         self.suit = suit
#         self.value = value
#
#     def getValue():
#         return self.value
#
#     def getSuit():
#         return self.suit
#
#     def getLabel():
#         return self.label
