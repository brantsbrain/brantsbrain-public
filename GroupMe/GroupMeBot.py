# Groupy is a downloadable package: https://pypi.org/project/GroupyAPI/
# GroupMe Developer page has instructions on how to get your GroupMe token: https://dev.groupme.com/
# Make a creds.py file in the same directory as this file, create a variable called token and paste your token as a string
from creds import token
from groupy.client import Client
import datetime, re, sys

client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()

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

# Search groups list for groupname and return group object
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

# Constantly run the bot in a given group and allow input from other users (all posts will be from current token)
def monBot(groupname):
    group = findGroup(groupname)
    help = ""

    # The admin list is filled w/ user_id strings to avoid name change issues
    # admins[0] should always be the owner. There is logic to avoid admin priv being removed from admins[0]
    # Need to move this outside the monBot method in case monBot needs to be restarted due to network error
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
                print(newestmessage.name + " executed numPosts")
                try:
                    searchMember = re.search(":(.*):", newestmessage.text).group(1)
                    group.post(text=searchMember + " has posted " + str(numMemberPosts(groupname, searchMember)) + " time(s)")
                except:
                    print("Couldn't find member")

            # Search for a keyword and return number of messages it occurred in
            elif "!searchKey" in newestmessage.text and newestmessage.text != help:
                print(newestmessage.name + " executed numPosts")
                try:
                    searchKey = re.search(":(.*):", newestmessage.text).group(1)
                    list = []
                    list.append(searchKey)
                    group.post(text=searchKey + " has appeared in " + str(countKeywords(groupname, list)) + " message(s)")
                except:
                    print("An error occurred")

            # List member details (name, nickname, and user_id) of the group
            elif "!listMembers" == newestmessage.text:
                print(newestmessage.name + " executed listMembers")
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
        # Need to catch a network exception as well
        except Exception as e:
            # monBot(groupname)
            print(str(e))
            exit()

if str(sys.argv[1]) == "help":
    print("Available options:\n\t"
            "monBot takes a groupname\n\t"
            "repeater takes groupname, membername, and boolean quiet start"
            "")
elif str(sys.argv[1]) == "monBot":
    monBot(sys.argv[2])
elif str(sys.argv[1]) == "repeater":
    repeater(sys.argv[2], sys.argv[3], sys.argv[4])
