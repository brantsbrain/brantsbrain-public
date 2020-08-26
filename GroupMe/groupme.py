# Groupy is a downloadable package: https://pypi.org/project/GroupyAPI/
# GroupMe Developer page has instructions on how to get your GroupMe token: https://dev.groupme.com/
# Make a creds.py file in the same directory as this file, create a variable called token and paste your token as a string
from creds import token
from groupy.client import Client
from time import sleep
import datetime, re

client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()

# Create backups for all groups
def backupAll():
    # printGroupNamesToFile()
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
def printGroupNamesToFile():
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

# List member details for a given group name (string)
def listMembers(groupname):
    group = findGroup(groupname)
    details = ""
    for member in group.members:
        details = (details + "Member name - " + member.name + "\n"
                    "Member nickname - " + member.nickname + "\n"
                    "Member ID - " + member.user_id + "\n\n")
    return details

# Post message in group a given number of times. Takes (string, string, int)
def postMessage(groupname, message, numtimes):
    group = findGroup(groupname)
    for num in range(numtimes):
        group.post(text=message)

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

# Find the number of posts from a member in a given group (string)
def numMemberPosts(groupname, membername):
    memberdict = {}
    counter = 0
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()
    member = findMember(groupname, membername)
    for message in messagelist:
        try:
            if message.user_id == member.user_id:
                counter += 1
        except:
            pass
    return counter

# Count the number of times a keyword(s) appears in a given group. Takes (string, list)
def countKeywords(groupname, keywordlist):
    count = 0
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()
    for message in messagelist:
        for keyword in keywordlist:
            try:
                if keyword in message.text:
                    count += 1
            except:
                pass
    return count

# Temp method used for testing different attributes of the group and message objects
def getAttributes(groupname):
    group = findGroup(groupname)
    print(str(dir(group.messages.list()[0])))
    print(str(group.messages.list()[0].data))
    print(group.messages.list()[0].created_at.strftime('%Y-%m-%d %H:%M:%S'))

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

# Returns list of member objects
def roster(groupname):
    group = findGroup(groupname)
    roster = []
    for member in group.members:
        roster.append(member)
    return roster

# Repeat everything a provided user (string) in a provided group (string) says starting and ending with a key string
def repeater(groupname, membername, quietstart):
    counter = 0
    startbot = False

    group = findGroup(groupname)
    member = findMember(groupname, membername)

    while startbot == False and quietstart == False:
        newestmessage = group.messages.list()[0]
        if str(newestmessage.name) == "Brant Goings" and str(newestmessage.text) == "Execute Order 66":
            group.post(text="It will be done, my lord. The youngling is " + member.name)
            startbot = True
            print("Start order given")
        else:
            print("Waiting for start order")
            sleep(sleeptime)

    while True:
        try:
            newestmessage = group.messages.list()[0]
            if str(newestmessage.name) == "Brant Goings" and str(newestmessage.text) == "It is done, my lord.":
                group.post(text="Well done, Lord Goings. Once more the Sith shall rule the galaxy!")
                print("Kill order given")
                break
            elif str(newestmessage.name) == member.name:
                group.post(text= ("I love " + member.name.split(" ")[0]))
                print(str(newestmessage.name) + " said " + str(newestmessage.text))
        except:
            repeater(groupname, membername, True)
    print("Bot ended")
    return

# Constantly run the bot in a given group and allow input from other users (all posts will be from current token)
def monBot(groupname):
    group = findGroup(groupname)
    help = ""

    # The admin list is filled w/ user_id strings to avoid name change issues
    # admins[0] should always be the owner. There is logic to avoid admin priv being removed from admins[0]
    admins = [findMember(groupname, "Brant Goings").user_id]

    # Should there be a timeout list?
    # timeout = []

    # Allows the program to run indefinitely
    while True:
        try:
            # The top of the while loop should always be collecting the newest message
            newestmessage = group.messages.list()[0]

            ########## Standard user commands ##########
            # Post help options
            if newestmessage.text == "!help":
                help = ("Standard User(s): \n"
                        "1. !numPosts:membername: - Replace membername with a member of the group and return the number of posts that user has posted\n\n"
                        "2. !searchKey:keyword: - Replace keyword with a word to search the group for and return the number of times it occurs\n\n"
                        "3. !listMembers - List member name, nickname, and user id in group\n\n"
                        "Admin(s): \n"
                        "1. !addAdmin:membername: - Replace membername with member to elevate to admin privilege\n\n"
                        "2. !removeAdmin:membername: - Replace membername with member to revoke admin privilege\n\n"
                        "3. !endBot - Ends running bot and refreshes to original admin list: " + str(admins) + "\n\n"
                        "Bot authored by Brant Goings. All rights reserved.")
                group.post(text=help)
                print("Help command posted")

            # Collect the number of posts from a supplied user
            elif "!numPosts" in newestmessage.text and newestmessage.text != help:
                try:
                    searchMember = re.search(":(.*):", newestmessage.text).group(1)
                except:
                    print("Couldn't find member")
                if searchMember:
                    group.post(text=searchMember + " has posted " + str(numMemberPosts(groupname, searchMember)) + " time(s)")
                else:
                    print("No member found")

            # Search for a keyword and return number of messages it occurred in
            elif "!searchKey" in newestmessage.text and newestmessage.text != help:
                searchKey = re.search(":(.*):", newestmessage.text).group(1)
                list = []
                list.append(searchKey)
                group.post(text=searchKey + " has appeared in " + str(countKeywords(groupname, list)) + " message(s)")

            # List member details (name, nickname, and user_id) of the group
            elif "!listMembers" == newestmessage.text:
                group.post(text=listMembers(groupname))

            ########## Begin admin commands ##########
            # Add a new admin
            elif "!addAdmin" in newestmessage.text and newestmessage.text != help:
                addAdmin = re.search(":(.*):", newestmessage.text).group(1)
                userid = findMember(groupname, addAdmin).user_id
                if userid in admins:
                    group.post(addAdmin + " is already an admin")
                elif newestmessage.user_id in admins:
                    admins.append(userid)
                    group.post(text="Added " + addAdmin + " to the admins list")
                    print("Added " + addAdmin + " to the admins list")
                else:
                    group.post(text="Sorry, you are not an admin")
                    print(newestmessage.name + " attempted to elevate " + addAdmin + " to admin")

            # Remove an admin
            elif "!removeAdmin" in newestmessage.text and newestmessage.text != help:
                removeAdmin = re.search(":(.*):", newestmessage.text).group(1)
                userid = findMember(groupname, removeAdmin).user_id
                if admins[0] == userid:
                    group.post("Consider " + removeAdmin + " a 'super admin'. Can't remove from the admin list")
                    print(newestmessage.name + " attempted to remove " + removeAdmin + " from the admin list")
                elif userid not in admins:
                    group.post(text=removeAdmin + " isn't an admin")
                elif newestmessage.user_id in admins:
                    admins.remove(userid)
                    group.post(text="Removed " + removeAdmin + " from the admins list")
                    print("Removed " + removeAdmin + " from the admins list")
                else:
                    group.post(text="Sorry, you are not an admin")
                    print(newestmessage.name + " attempted to elevate " + addAdmin + " to admin")

            # End the bot
            elif "!endBot" == newestmessage.text:
                if newestmessage.user_id in admins:
                    group.post(text="Stopping bot")
                    print(newestmessage.name + " ended bot")
                    exit()
                else:
                    group.post(text="Sorry, you are not an admin")
                    print(newestmessage.name + " attempted to end the bot")

            # If none of the above commands were run, it must not be a command
            elif newestmessage.text[0] == "!":
                group.post("Unrecognized command")
                print(newestmessage.name + " attempted to run " + newestmessage.text)

        # Print any exception that occurs and end runtime
        except Exception as e:
            # monBot(groupname)
            print(str(e))
            exit()

monBot("TestGroup")
