import os

# Instantiate variables
initiallist = list()
writelist = list()

# Print welcome message
print(""
        "\n-------------------------------------------------------------------------------------------------------------------------------\n"
        "\nWelcome to the Dictionary Builder:\n"
        "\nThis is meant to take in a dictionary of original passwords (like birthday, significant other, pet names, etc.) \nand generate "
        "iterations of those passwords using special characters, capitlization, etc.\n"
        "\nCreate a dictionary (e.g. dict.txt) beforehand and enter any number of phrases that pertain to the owner separated by the Enter key.\n"
        "\nNOTE: The dictionary file must be in the same folder DictinoaryBuilder.py is being run from.\n"
        "\nDictionary lines will be systematically combined, any lines that begin with a hyphen will be ignored, "
        "and any duplicate lines will be deleted automatically.\n"
        "\nEnjoy!\n"
        "\n- Brant\n"
        "\n-------------------------------------------------------------------------------------------------------------------------------\n")

# ------------------------------------------------------------ INPUT ------------------------------------------------------------ #
# Pull filename
filenameanswer = input("Is the dictionary named dict.txt? Y/N: ").upper()

if filenameanswer == "Y":
    dictionarypath = "./dict.txt"
elif filenameanswer == "N":
    print("\n")
    dictionarypath = "./" + input("Dictionary Name: ")
    print("\n")
else:
    print("Not a valid answer. Exiting...")
    exit()

# Pull OS
osanswer = input("Windows or Linux? W/L: ").upper()

if osanswer == "W":
    print("\n")
elif osanswer == "L":
    print("\n")
else:
    print("Not a valid answer. Exiting...")
    exit()

# Enforce minimum character limit?
enflen = input("Enforce minimum character limit? Y/N: ").upper()

if enflen == "Y":
    minlen = int(input("Minimum Length: "))

# ------------------------------------------------------------ METHODS ------------------------------------------------------------ #
# Delete empty lines
def emptyLineDelete():
    with open(dictionarypath, "r") as dictionaryread:
        lines = dictionaryread.readlines()
    with open(dictionarypath, "w") as dictionarywrite:
        for line in lines:
            if line.strip("\n") != "":
                dictionarywrite.write(line)

# Print entire dictionary
def printLines():
    with open(dictionarypath, "r") as dictionaryread:
        for line in dictionaryread:
            print(line.strip())

# startsHyphen Boolean
def startsHyphen(line):
    if line.startswith("-"):
        return True
    else:
        return False

# Delete lines less than defined minlen
def passLen(passlen):
    with open(dictionarypath, "r") as dictionaryread:
        lines = dictionaryread.readlines()
    with open(dictionarypath, "w") as dictionarywrite:
        for line in lines:
            if len(line) > passlen:
                dictionarywrite.write(line)

# Finds and deletes duplicates
def verboseDupFinder():
    emptyLineDelete()
    dup = 0
    with open(dictionarypath, "r") as dictionaryread:
        lines = dictionaryread.readlines()
    with open("dict.txt", "w") as dictionarywrite:
        for line in lines:
            if line not in seen:
                dictionarywrite.write(line)
                seen.add(line)
            else:
                dup = dup + 1
                print("Duplicate Found -- " + line.rstrip() + " -- Deleted Successfully\n")
        if dup == 0:
            print("No duplicates found")
        else:
            print("Deleted " + str(dup) + " duplicates")

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

# Swap a character for another character
def swapFor(pre, post):
    message = "---------------------------- Swapping " + pre + " For " + post + " ----------------------------"
    with open(dictionarypath, "r") as dictionaryread:
        with open(dictionarypath, "a+") as dictionaryappend:
            dictionaryappend.write("\n" + message + "\n")
            for line in dictionaryread:
                if not startsHyphen(line):
                    if pre in line:
                        dictionaryappend.write(line.replace(pre, post))

# Add a given number of exclamation points to the end of each line
def addExcl(num):
    message = "---------------------------- Incrementing Exclamation Points Up To " + str(num) + " ----------------------------"
    needMore = 0
    with open(dictionarypath, "a+") as dictionaryappendmessage:
        dictionaryappendmessage.write("\n" + message + "\n")
    with open(dictionarypath, "r") as dictionaryread:
        while needMore < num:
            emptyLineDelete()
            lines = dictionaryread.readlines()
            with open(dictionarypath, "a+") as dictionaryappend:
                for line in lines:
                    if not startsHyphen(line):
                        newString = "" + line[:-1] + "!\n"
                        dictionaryappend.write(newString)
                dictionaryappend.write("\n--- Added " + str(needMore + 1) + " exclamation point(s) ---\n")
                needMore = needMore + 1
        emptyLineDelete()

# Swap the case of a given letter
def swapCase(letter):
    message = "---------------------------- Swapping the Case of " + letter + " ----------------------------"
    with open(dictionarypath, "r") as dictionaryread:
        with open(dictionarypath, "a+") as dictionaryappend:
            dictionaryappend.write("\n" + message + "\n")
            for line in dictionaryread:
                if not startsHyphen(line):
                    if letter.lower() == letter:
                        if letter in line:
                            dictionaryappend.write(line.replace(letter, letter.upper()))
                    elif letter.upper() == letter:
                        if letter in line:
                            dictionaryappend.write(line.replace(letter, letter.lower()))

# Attach number to the end of each line
def tagNum(num):
    message = "---------------------------- Tagging on a Tail Number Up To " + str(num) + " ----------------------------"
    currentNum = 1
    with open(dictionarypath, "a+") as dictionaryappendmessage:
        dictionaryappendmessage.write("\n" + message + "\n")
    with open(dictionarypath, "r") as dictionaryread:
        lines = dictionaryread.readlines()
        while currentNum <= num:
            emptyLineDelete()
            with open(dictionarypath, "a+") as dictionaryappend:
                for line in lines:
                    if not startsHyphen(line):
                        newString = "" + line[:-1] + str(currentNum) + "\n"
                        dictionaryappend.write(newString)
                currentNum = currentNum + 1

# Replace number at end of line (if it exists) with another number
def replTailNum(num):
    message = "---------------------------- Replacing Tail Number (if exists) with Integers up to " + str(num) + " ----------------------------"
    currentNum = 1
    with open(dictionarypath, "a+") as dictionaryappendmessage:
        dictionaryappendmessage.write("\n" + message + "\n")
    with open(dictionarypath, "r") as dictionaryread:
        while currentNum <= num:
            lines = dictionaryread.readlines()
            emptyLineDelete()
            with open(dictionarypath, "a+") as dictionaryappend:
                for line in lines:
                    if not startsHyphen(line):
                        if currentNum == 1:
                            newString = "" + line[:-1] + str(currentNum) + "\n"
                            dictionaryappend.write(newString)
                        else:
                            newString = "" + line[:-2] + str(currentNum) + "\n"
                            dictionaryappend.write(newString)
                currentNum = currentNum + 1

# Make all characters upper case
def upperCase():
    message = "---------------------------- Making All Upper Case ----------------------------"
    with open(dictionarypath, "a+") as dictionaryappendmessage:
        dictionaryappendmessage.write("\n" + message + "\n")
    with open(dictionarypath, "r") as dictionaryread:
        with open(dictionarypath, "a+") as dictionaryappend:
            for line in dictionaryread:
                if not startsHyphen(line):
                    dictionaryappend.write(line.upper())

# Make all characters lower case
def lowerCase():
    message = "---------------------------- Making All Lower Case ----------------------------"
    with open(dictionarypath, "a+") as dictionaryappendmessage:
        dictionaryappendmessage.write("\n" + message + "\n")
    with open(dictionarypath, "r") as dictionaryread:
        with open(dictionarypath, "a+") as dictionaryappend:
            for line in dictionaryread:
                if not startsHyphen(line):
                    dictionaryappend.write(line.lower())

# Need an alternating case
def alterCase():
    message = "---------------------------- Alternating Cases ----------------------------"
    index = 0
    with open(dictionarypath, "a+") as dictionaryappendmessage:
        dictionaryappendmessage.write("\n" + message + "\n")
    with open(dictionarypath, "r") as dictionaryread:
        lines = dictionaryread.readlines()
    with open(dictionarypath, "a+") as dictionaryappend:
        for line in lines:
            if not startsHyphen(line):
                while index < len(line):
                    if index % 2 == 0:
                        dictionaryappend.write(line[index].upper().rstrip())
                    elif index == (len(line) - 1):
                        pass
                    else:
                        dictionaryappend.write(line[index].rstrip())
                    index = index + 1
                dictionaryappend.write("\n")
                index = 0

def cleanUp():
    with open(dictionarypath, "r") as dictionaryread:
        lines = dictionaryread.readlines()
    with open(dictionarypath, "w") as dictionarywrite:
            for line in lines:
                if not startsHyphen(line):
                    dictionarywrite.write("")
                else:
                    dictionarywrite.write(line)
            print("\nHyphenated lines deleted\n")

# Combine initial passwords in all possible combinations
# Not exhaustive
def combineInitial():
    index = 0
    iteration = 0
    message = "---------------------------- Exhaustively Combining Original Passwords ----------------------------"
    with open(dictionarypath, "a+") as dictionaryappendmessage:
        dictionaryappendmessage.write("\n" + message + "\n")
    with open(dictionarypath, "r") as dictionaryread:
        lines = dictionaryread.readlines()
    with open(dictionarypath, "a+") as dictionarywrite:
            emptyLineDelete()
            for line in lines:
                if not startsHyphen(line):
                    initiallist.append(line.rstrip())
            writelist = initiallist
            while iteration < 4:
                index = 0
                num = 0
                retchar = 1
                while index < len(initiallist):
                    while retchar < len(initiallist):
                        dictionarywrite.write(writelist[num])
                        if num == retchar:
                            dictionarywrite.write("\n")
                            retchar = retchar + 1
                            num = 0
                        else:
                            num = num + 1
                    index = index + 1
                initiallist.insert(0, initiallist.pop(len(initiallist) - 1))
                iteration = iteration + 1
    dupFinder()

# Revamp for initial three lines
def combineInitialThree():
    index = 0
    iteration = 0
    message = "---------------------------- Exhaustively Combining First Three Lines ----------------------------"
    with open(dictionarypath, "a+") as dictionaryappendmessage:
        dictionaryappendmessage.write("\n" + message + "\n")

# ------------------------------------------------------------ MAIN ------------------------------------------------------------ #
commands = input("Enter commands separated by commas (no spaces). Commands run in order of being typed, not numerically.\nDictionary file "
                    "will be modified after each command.\nPress 'Enter' when finished.\n\n\t"
                   "1) Print Dictionary Into Console \n\t"
                   "2) Find Duplicates \n\t"
                   "3) Swap a for @ \n\t"
                   "4) Swap s for $ \n\t"
                   "5) Swap i for 1 \n\t"
                   "6) Swap e for 3 \n\t"
                   "7) Swap o for 0 \n\t"
                   "8) Custom Swap (Note: May swap a phrase for a different length phrase) \n\t"
                   "9) Incrementally Add Exclamation Point(s) \n\t"
                   "10) Swap Case of a Given Letter \n\t"
                   "11) Tag on an Integer to Tail of Password Incrementally \n\t"
                   "12) Replace Tail of Password with an Integer Incrementally \n\t"
                   "13) Make All Letters Upper Case \n\t"
                   "14) Make All Letters Lower Case \n\t"
                   "15) Alternate Case of Letters in Line \n\t"
                   "W) The Works (Preselected values for previous commands. May take some time to finish if there are any more than 4 provided passwords) \n\t"
                   "D) Delete Hyphenated Lines (run last) \n\t"
                   "\nCommand(s): ")

runcommands = commands.split(",")

combineInitial()

for runcommand in runcommands:
    if runcommand == "1":
        printLines()
    elif runcommand == "2":
        verboseDupFinder()
    elif runcommand == "3":
        swapFor("a", "@")
    elif runcommand == "4":
        swapFor("s", "$")
    elif runcommand == "5":
        swapFor("i", "1")
    elif runcommand == "6":
        swapFor("e", "3")
    elif runcommand == "7":
        swapFor("o", "0")
    elif runcommand == "8":
        first = input("\nCharacter(s) being replaced: ")
        second = input("\nCharacter(s) to replace with: ")
        swapFor(first, second)
    elif runcommand == "9":
        addExcl(int(input("Up to how many exclamation points should be added? ")))
    elif runcommand == "10":
        letter = input("Letter to swap case of (input is case-sensitive): ")
        swapCase(letter)
    elif runcommand == "11":
        tagNum(int(input("Up to what integer should be added to the end of each line? ")))
    elif runcommand == "12":
        replTailNum(int(input("Up to what integer should be replaced? ")))
    elif runcommand == "13":
        upperCase()
    elif runcommand == "14":
        lowerCase()
    elif runcommand == "15":
        alterCase()
    elif runcommand.upper() == "W":
        swapFor("a", "@")
        swapFor("s", "$")
        swapFor("i", "1")
        swapFor("e", "3")
        swapFor("o", "0")
        replTailNum(2)
        addExcl(1)
        # tagNum(2)
        upperCase()
        lowerCase()
        alterCase()
    elif runcommand.upper() == "D":
        cleanUp()
    elif osanswer == "W":
        print("Invalid entry. Press any key to close...")
        os.system("pause")
        exit()
    elif osanswer == "L":
        print("Invalid entry. Press any key to close...")
        # command to pause on linux?
        exit()
    else:
        exit()

# Enforce pass length here
if enflen == "Y":
    passLen(minlen)

dupFinder()
emptyLineDelete()

print("\nProgram Complete -- Thank You")
