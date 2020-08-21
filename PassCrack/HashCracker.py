import hashlib, os

# Instantiate variables
cracked = list()

# Instantiate loud variable as true. This will determine whether output is printed to console
loud = True

# Print welcome message
print(
        "\n-----------------------------------------------------------------------------------------------------------------\n"
        "\nWelcome to the Hash Cracker:\n"
        "\nThis is meant to take in a dictionary of passwords and a table of hashes that may coincide with one or more\n"
        "of the passwords in the dictionary, then output whichever pairs match.\n"
        "\nIf you haven't created a comprehensive dictionary file yet, you may want to check out DictionaryBuilder.py first.\n"
        "\nWe recommend naming your dictionary file 'dict.txt' and hash file 'hash.txt' to make life easier.\n"
        "\nNOTE: The dictionary and hash files must be in the same folder HashCracker.py is being run from.\n"
        "\nHashCracker.py recognizes MD5, SHA-256, and SHA-512 hashes.\n"
        "\nAny lines that begin with a hyphen will be ignored.\n"
        "\nEnjoy!\n"
        "\n- Brant\n"
        "\n-----------------------------------------------------------------------------------------------------------------\n")

# ------------------------------------------------------------ INPUT ------------------------------------------------------------ #
# Pull OS
osanswer = input("Windows or Linux? W/L: ").upper()

if osanswer == "W":
    print("\nFiles available in this directory\n")
    os.system("dir")
    print("\n")
elif osanswer == "L":
    print("\nFiles available in this directory\n")
    os.system("ls")
    print("\n")
else:
    print("Not a valid answer")
    exit()

# Pull hash and dictionary files
filenameanswer = input("Are the dictionary and hash tables named dict.txt and hash.txt? Y/N: ").upper()

if filenameanswer == "Y":
    hashes = "./hash.txt"
    dictionary = "./dict.txt"
else:
    hashes = "./" + input("Hash Table Name: ")
    dictionary = "./" + input("Dictionary Name: ")

print("\n")

# ------------------------------------------------------------ METHODS ------------------------------------------------------------ #
# Delete empty lines
def emptyLineDelete():
    with open(hashes, "r") as dictionaryread:
        lines = dictionaryread.readlines()
    with open(hashes, "w") as dictionarywrite:
        for line in lines:
            try:
                if line.strip("\n") != "":
                    dictionarywrite.write(line)
            except:
                pass
    with open(dictionary, "r") as dictionaryread:
        lines = dictionaryread.readlines()
    with open(dictionary, "w") as dictionarywrite:
        for line in lines:
            try:
                if line.strip("\n") != "":
                    dictionarywrite.write(line)
            except:
                pass

# Hyphen Boolean
def startsHyphen(line):
    if line.startswith("-"):
        return True
    else:
        return False

# Crack hashes based on algorithms provided in MAIN
def crack(algorithm):
    with open(dictionary, "r") as dictionaryreader:
        if algorithm == "md5":
            try:
                for dictline in dictionaryreader:
                    with open(hashes, "r") as hashreader:
                        for hashline in hashreader:
                            if not startsHyphen(dictline) or not startsHyphen(hashline):
                                if hashlib.md5(dictline.rstrip().encode()).hexdigest().lower() == hashline.rstrip().lower():
                                    if loud == True:
                                        print("MD5 hash cracked -- " + hashline.lower().rstrip() + " : " + dictline)
                                    cracked.append("MD5 hash cracked -- " + hashline.lower().rstrip() + " : " + dictline)
                                else:
                                    pass
            except:
                pass
        elif algorithm == "sha256":
            try:
                for dictline in dictionaryreader:
                     with open(hashes, "r") as hashreader:
                         for hashline in hashreader:
                             if not startsHyphen(dictline) or not startsHyphen(hashline):
                                 if hashlib.sha256(dictline.rstrip().encode()).hexdigest().lower() == hashline.rstrip().lower():
                                     if loud == True:
                                         print("SHA256 hash cracked -- " + hashline.lower().rstrip() + " : " + dictline)
                                     cracked.append("SHA256 hash cracked -- " + hashline.lower().rstrip() + " : " + dictline)
                                 else:
                                     pass
            except:
                pass
        elif algorithm == "sha512":
            try:
                for dictline in dictionaryreader:
                    with open(hashes, "r") as hashreader:
                        for hashline in hashreader:
                            if not startsHyphen(dictline) or not startsHyphen(hashline):
                                if hashlib.sha512(dictline.rstrip().encode()).hexdigest().lower() == hashline.rstrip().lower():
                                    if loud == True:
                                        print("SHA512 hash cracked -- " + hashline.lower().rstrip() + " : " + dictline)
                                    cracked.append("SHA512 hash cracked -- " + hashline.lower().rstrip() + " : " + dictline)
                                else:
                                    pass
            except:
                pass

# Make cracked.txt
def makeCracked():
    try:
        with open("./cracked.txt", "w") as crackedwriter:
            for line in cracked:
                crackedwriter.write(line)
        print("\n./cracked.txt created successfully")
    except:
        print("Error Occurred. Exiting...")
        exit()

# ------------------------------------------------------------ MAIN ------------------------------------------------------------ #
commands = input("Enter command numbers separated by commas (no spaces).\nCommands run in order of being typed, not numerically.\n"
                    "Press 'Enter' when finished.\n\n\t"
                   "1) MD5 \n\t"
                   "2) SHA256 \n\t"
                   "3) SHA512 \n\t"
                   "4) Export to ./cracked.txt when done? (Run last) \n\t"
                   "A) All of the above (this should be the only command submitted to prevent overlap) \n\t"
                   "\nCommand(s): ")

runcommands = commands.split(",")

# Don't print to console since output is going to ./cracked.txt
if "4" in runcommands or "a" in runcommands or "A" in runcommands:
    loud = False

for runcommand in runcommands:
    # emptyLineDelete() # Not working with rockyou.txt -- Unicode error
    if runcommand == "1":
        crack("md5")
    elif runcommand == "2":
        crack("sha256")
    elif runcommand == "3":
        crack("sha512")
    elif runcommand == "4":
        makeCracked()
    elif runcommand.upper() == "A":
        crack("md5")
        crack("sha256")
        crack("sha512")
        makeCracked()
    else:
        exit()

print("\nProgram Complete -- Thank You")
