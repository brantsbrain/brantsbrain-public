from itertools import permutations
dictionarypath = "./dict.txt"

# Delete empty lines
def emptyLineDelete():
    with open(dictionarypath, "r") as dictionaryread:
        lines = dictionaryread.readlines()
    with open(dictionarypath, "w") as dictionarywrite:
        for line in lines:
            if line.strip("\n") != "":
                dictionarywrite.write(line)

# Hyphen Boolean
def hyphen(line):
    if line.startswith("-"):
        return True
    else:
        return False

# DupFinder
def dupFinder():
    emptyLineDelete()
    seen = set()
    with open(dictionarypath, "r") as dictionaryread:
        lines = dictionaryread.readlines()
    with open("dict.txt", "w") as dictionarywrite:
        for line in lines:
            if line.rstrip() not in seen:
                dictionarywrite.write(line)
                seen.add(line.rstrip())

def combineInitialThree():
    firstthree = list()
    x = 1

    with open(dictionarypath, "r") as dictionaryread:
        dictionaryread.readline() # Skip first line
        while x <= 3:
            firstthree.append(dictionaryread.readline().rstrip())
            x = x + 1
        print(firstthree)

    compthree = list(permutations(firstthree))

    with open(dictionarypath, "a+") as dictionarywrite:
        dictionarywrite.write("\n")

        # Two word combinations
        for index in range(len(compthree) - 1):
            if index == len(compthree) - 1:
                joinedwords = "".join(compthree[0][index])
                joinedwords += "".join(compthree[0][0])
                print(joinedwords)
            elif index == len(compthree[index]) - 1:
                joinedwords = "".join(compthree[0][index])
                joinedwords += "".join(compthree[0][0])
                print(joinedwords)
            else:
                joinedwords = "".join(compthree[0][index])
                joinedwords += "".join(compthree[0][index + 1])
                print(joinedwords)

        # Three word combinations -- WORKS
        index = 0
        needtwo = 0
        for index in range(len(compthree)):
            dictionarywrite.write("".join(compthree[index]) + "\n")




    # dupFinder()
    # with open(dictionarypath, "r") as dictionaryread:
    #     lines = dictionaryread.readlines()
    #     with open(dictionarypath, "w") as dictionarywrite:
    #         for line in lines:
    #             if not line in firstThree:
    #                 dictionarywrite.write(line)


combineInitialThree()
