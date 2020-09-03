# Groupy is a downloadable package: https://pypi.org/project/GroupyAPI/
# GroupMe Developer page has instructions on how to get your GroupMe token: https://dev.groupme.com/
# Make a creds.py file in the same directory as this file, create a variable called token and paste your token as a string
from creds import token
from groupy.client import Client
import datetime, sys

client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()

# List most common words used per member
def commonWords(groupname):
    memberdict = {}
    wordlist = []
    num = 5
    exceptionlist = ["ben", "jake", "wil", "jackson", "jakey", "justin", "vitkus", "kubal", "phil", "brant"]
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()

    print("Filling memberdict...")
    for member in group.members:
        memberdict[member.user_id] = {}

    print("Searching messages...")
    for message in messagelist:
        for member in memberdict.items():
            if message.user_id == member[0]:
                try:
                    wordlist = message.text.split(" ")
                    for word in wordlist:
                        word = word.lower()
                        if word in member[1].keys():
                            member[1][word] += 1
                        elif len(word) > num or word in exceptionlist:
                            member[1][word] = 1
                except:
                    pass

    print("Writing results...")
    with open("TopWords.txt", "a+") as writer:
        writer.write("\n--- Words greater than " + str(num) + " letters ---")
        for member in memberdict.items():
            writer.write("\n" + findMember(groupname, member[0]).nickname + "'s most common words - \n")
            sorted_list = sorted(member[1].items(), key=lambda x: x[1], reverse=True)
            for x in range(10):
                try:
                    writer.write(sorted_list[x][0] + " - " + str(sorted_list[x][1]) + "\n")
                except:
                    pass
        writer.write("\n")

# Print a list of the most liked messages
def mostLikedMessages(groupname):
    mostlikedlist = []
    mostlikes = 0
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()

    for message in messagelist:
        if len(message.favorited_by) >= mostlikes:
            mostlikedlist.append(message)
            mostlikes = len(message.favorited_by)

    for index in mostlikedlist:
        try:
            print(index.created_at.strftime('%Y-%m-%d %H:%M:%S') + " - " + index.name + ": " + index.text + " - " + str(len(index.favorited_by)) + " likes")
        except:
            pass

# Print a sorted list of the people that got 3+ likes
# Not using memberdict[x][1] right now
def numLikes(groupname):
    details = ""
    counter = 0
    memberdict = {}
    mostlikes = 0
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()

    for member in group.members:
        memberdict[member.user_id] = [0,0]

    for message in messagelist:
        for x,y in memberdict.items():
            if message.user_id == x:
                if len(message.favorited_by) >= 3:
                    memberdict[x][0] += 1
                memberdict[x][1] += 1
                counter += len(message.favorited_by)

    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1], reverse=True)
    details = "Messages that got 3+ likes - \n"
    for i in sorted_memberdict:
        membername = findMember(groupname, i[0]).nickname
        details = details + membername + " - " + str(i[1][0]) + "\n"
    details = details + "\nTotal likes - " + str(counter)
    print(details)

# Find average length of message in characters
def averMessLength(groupname):
    memberdict = {}
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()

    # memberdict value has a two index list.
    # index[0] = number of characters posted
    # index[1] = number of messages posted
    for member in group.members:
        memberdict[member.user_id] = [0,0]

    for message in messagelist:
        for member in memberdict.keys():
            if message.user_id == member:
                memberdict[member][1] += 1
                try:
                    for character in message.text:
                        memberdict[member][0] += 1
                except:
                    pass

    with open("CharCount.txt", "a+") as writer:
        writer.write("\n--- " + groupname + " Character Averages ---\n")
        for member in memberdict.keys():
            writer.write(str(findMember(groupname,member).nickname) + "\n\tAverage character count per message - " + str(round(memberdict[member][0]/memberdict[member][1], 2)) + "\n\tTotal messages - " + str(memberdict[member][1]) + "\n")

# Need to only write files for groups where the most recent message has changed
def backupChanged():
    failedNames = []
    counter = 0
    updatelist = []
    with open("GroupNames.txt", "r") as reader:
        for line in reader:
            try:
                # Find most recent groupme message
                newestmessage = findGroup(line.strip("\n")).messages.list()[0]

                # Return last line of most recent .csv backup
                with open(".\\Backup CSVs\\" + line.strip("\n") + " Messages.csv", "r") as backupreader:
                    for last in backupreader:
                        pass
                    recentmess = last.split("`")

                # Compare lines and backup groupme if not equal
                if(newestmessage.text.strip("\n") == recentmess[3].strip("\n")):
                    print(line.strip("\n") + " doesn't need to be updated\n")
                    pass
                else:
                    print("\nUpdating " + line.strip("\n"))
                    updatelist.append(line.strip("\n"))
                    writeAllMessages(line.strip("\n"), False)
            except Exception as e:
                print("Error occurred in " + line + " : " + str(e))
                failedNames.append(line.strip())
                counter += 1
                pass
    print("Failed to access " + str(counter) + " groupmes: " + str(failedNames))
    print(str(len(updatelist)) + " group chats were updated: " + str(updatelist))

# Write all group message data from all groups to files
def backupAll():
    failedNames = []
    counter = 0
    with open("GroupNames.txt", "r") as reader:
        for line in reader:
            try:
                writeAllMessages(line.strip("\n"), False)
            except Exception as e:
                print("Error occurred in " + line + " : " + str(e))
                failedNames.append(line)
                counter += 1
                pass
    print("Failed " + str(counter) + " files: " + str(failedNames))

# Print all your active groups
def printGroupNames():
    counter = 0
    for group in groups.autopage():
        print(group.name)
        counter += 1
    print("Number of Groups: " + str(counter))

# Write all your group names to a file
def writeGroupNamesToFile():
    counter = 0
    failed = 0
    with open("GroupNames.txt", "w") as groupnamewriter:
        for group in groups.autopage():
            try:
                groupnamewriter.write(group.name + "\n")
                counter += 1
            except:
                print("Couldn't write " + group.name)
                failed += 1
                pass
    print("Wrote " + str(counter) + " out of " + str(counter + failed) + " groups")

# Print attributes about your user
def printMyInfo():
    for x,y in myuser.items():
        print(str(x) + " : " + str(y))

# Write all messages in a given group to file (string)
def writeAllMessages(groupname, easyread):
    counter = 0
    sep = ""
    extension = ""
    user = False
    group = findGroup(groupname)
    allmess = list(group.messages.list().autopage())

    if easyread:
        sep = " - "
        extension = ".txt"

        with open(".\\EasyRead\\" + groupname + " Messages" + extension, "w") as messagewriter:
            num = len(allmess) - 1
            while num >= 0:
                message = allmess[num]
                try:
                    messagewriter.write(message.created_at.strftime('%Y-%m-%d %H:%M:%S') + sep + message.name + sep + message.text + "\n")
                except:
                    counter += 1
                    pass
                num -= 1
    else:
        sep = "`"
        extension = ".csv"

        with open(".\\Backup CSVs\\" + groupname + " Messages" + extension, "w") as messagewriter:
            num = len(allmess) - 1
            while num >= 0:
                message = allmess[num]
                try:
                    messagewriter.write(message.created_at.strftime('%Y-%m-%d %H:%M:%S') + sep + message.name + sep + message.user_id + sep + message.text + "\n")
                except:
                    counter += 1
                    pass
                num -= 1

    print(str(counter) + " errors occurred in writing messages")

# Searches given group for keyword (string, string)
def searchForKeyword(groupname, keyword):
    keywordlist = []
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()
    for message in messagelist:
        try:
            if keyword in message.text:
                keywordlist.append(message)
        except:
            pass
    for index in keywordlist:
        print(index.name + ": " + index.text)
    return

# Find group and return group object
def findGroup(groupname):
    print("Looking for '" + groupname + "'")
    for group in groups.autopage():
        if group.name == groupname:
            print("Found " + group.name)
            return group
    print("Couldn't find group")
    return None

# Given a string name, return the member object in a group
def findMember(groupname, membername):
    group = findGroup(groupname)
    for member in group.members:
        if member.name == membername or member.nickname == membername or member.user_id == membername:
            print("Found " + member.name)
            return member
    print("Couldn't find " + membername)
    return None

if str(sys.argv[1]) == "help":
    print("Available options:\n\t"
            "delta - only make backups of changed groupmes\n\t"
            "find - search for a given group name\n\t"
            "names - create GroupNames.txt containing all active groups\n\t"
            "")
elif str(sys.argv[1]) == "delta":
    print("Running backupChanged()")
    backupChanged()
elif str(sys.argv[1]) == "find":
    print("Running findGroup()")
    findGroup(sys.argv[2])
elif str(sys.argv[1]) == "names":
    print("Running writeGroupNamesToFile()")
    writeGroupNamesToFile()
elif str(sys.argv[1]) == "averMessLength":
    print("Running averMessLength()")
    averMessLength(sys.argv[2])
elif str(sys.argv[1]) == "numLikes":
    print("Running numlikes()")
    numLikes(sys.argv[2])
elif str(sys.argv[1]) == "mostLikedMessages":
    print("Running mostLikedMessages()")
    mostLikedMessages(sys.argv[2])
elif str(sys.argv[1]) == "commonWords":
    print("Running commonWords()")
    commonWords(sys.argv[2])
