# Groupy is a downloadable package: https://pypi.org/project/GroupyAPI/
# GroupMe Developer page has instructions on how to get your GroupMe token: https://dev.groupme.com/
# Make a creds.py file in the same directory as this file, create a variable called token and paste your token as a string
from creds import token
from groupy.client import Client
import datetime

client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()

# Write all group message data from all groups to files
def backupAll():
    writeGroupNamesToFile()
    failedNames = []
    counter = 0
    with open("GroupNames.txt", "r") as reader:
        for line in reader:
            try:
                writeAllMessages(line.strip("\n"), True)
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
    group = findGroup(groupname)
    allmess = list(group.messages.list().autopage())

    if easyread:
        sep = " - "
        extension = ".txt"
    else:
        sep = "`"
        extension = ".csv"

    with open(groupname + " Messages" + extension, "w") as messagewriter:
        num = len(allmess) - 1
        while num >= 0:
            message = allmess[num]
            try:
                messagewriter.write(message.created_at.strftime('%Y-%m-%d %H:%M:%S') + sep + message.name + sep + message.text + "\n")
            except:
                counter += 1
                pass
            num -= 1
    print(str(counter) + " errors occurred")

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
    print("Looking for " + groupname)
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
        if member.name == membername or member.nickname == membername:
            print("Found " + member.name)
            return member
    print("Couldn't find " + membername)
    return None
