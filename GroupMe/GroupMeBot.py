# Groupy is a downloadable package: https://pypi.org/project/GroupyAPI/
# GroupMe Developer page has instructions on how to get your GroupMe token: https://dev.groupme.com/
# Make a creds.py file in the same directory as this file, create a variable called token and paste your token as a string
from creds import token
from groupy.client import Client
import datetime, re, sys
from requests.exceptions import HTTPError

client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()

# Search for keyword only posted by a certain member
def searchKeyByMem(groupname, keyword, membername):
        count = 0
        group = findGroup(groupname)
        member = findMember(groupname, membername)
        messagelist = group.messages.list().autopage()
        for message in messagelist:
            try:
                if keyword.lower() in message.text.lower() and message.user_id == member.user_id:
                    count += 1
            except:
                pass
        return count

# Kick users after a certain number of posts within a certain amount of time?
def kickNow():
    # Insert logic
    return

# List percentage of posts for all users
def allMemberPercentPosts(groupname):
    details = ""
    counter = 0
    memberdict = {}
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()

    # Instantiate the memberdict member objects with counters at 0
    for member in group.members:
        memberdict[member.user_id] = 0

    # For each message, iterate through memberdict and check to see if message.user_id matches x.
    # If so, increase that member's counter by 1 and the total counter by 1
    for message in messagelist:
        for x,y in memberdict.items():
            if message.user_id == x:
                memberdict[x] += 1
                counter += 1

    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1], reverse=True)
    details = "Percentage of total posts:\n"
    for i in sorted_memberdict:
        membername = findMember(groupname, i[0]).nickname
        details = details + membername + " - " + str(round(i[1]/counter*100, 2)) + "%\n"
    details = details + "\nTotal posts - " + str(counter)

    return details

# List member details for a given group name (string)
def listMembers(groupname):
    details = ""
    group = findGroup(groupname)
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

# List number of posts for all members
def allNumPosts(groupname):
    details = ""
    counter = 0
    memberdict = {}
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()

    # Instantiate the memberdict member objects with counters at 0
    for member in group.members:
        memberdict[member.user_id] = 0

    # For each message, iterate through memberdict and check to see if message.user_id matches x.
    # If so, increase that member's counter by 1 and the total counter by 1
    for message in messagelist:
        for x,y in memberdict.items():
            if message.user_id == x:
                memberdict[x] += 1
                counter += 1

    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1], reverse=True)
    for i in sorted_memberdict:
        membername = findMember(groupname, i[0]).nickname
        details = details + membername + " posts - " + str(i[1]) + "\n"
    details = details + "\nTotal posts - " + str(counter)

    return details

# Count the number of times a keyword(s) appears in a given group. Takes (string, list)
def countKeywords(groupname, keywordlist):
    count = 0
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()
    for message in messagelist:
        for keyword in keywordlist:
            try:
                if keyword.lower() in message.text.lower():
                    count += 1
            except:
                pass
    return count

# Temp method used for testing different attributes of the group and message objects
def getAttributes(groupname):
    group = findGroup(groupname)
    print(str(dir(group.messages.list()[0])))
    print(str(group.messages.list()[0].data))
    print(str(group.messages.list()[0].user_id))
    print(str(type(group.messages.list()[0].user_id)))
    print(str(findMember(groupname, "Brant Goings").user_id))
    print(str(type(findMember(groupname, "Brant Goings").user_id)))
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
        if member.name == membername or member.nickname == membername or member.user_id == membername:
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
    help1 = ""
    help2 = ""

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
                help1 = ("Standard User(s): \n"
                        "1. !numPosts:membername: - Replace membername with a member of the group and return the number of posts that user has posted\n\n"
                        "2. !searchKey:keyword: - Replace keyword with a word to search the group for and return the number of times it occurs\n\n"
                        "3. !listMembers - List member names, nicknames, and user ids in group\n\n"
                        "4. !allNumPosts - List number of posts per member and total number of posts in group\n\n"
                        "5. !percentPosts - List percentage of total posts per member\n\n"
                        "6. !keyByMem:keyword,membername: - Lists how many times a given member posted a message with a keyword in it\n\n")
                help2 = ("Admin(s): \n"
                        "1. !postMess:message,num: - Replace message with the desired message and num with the desired number of posts\n\n"
                        "2. !addAdmin:membername: - Replace membername with member to elevate to admin privilege\n\n"
                        "3. !removeAdmin:membername: - Replace membername with member to revoke admin privilege\n\n"
                        "4. !endBot - Ends running bot and refreshes to original admin list\n\n"
                        "Bot authored by Brant Goings. All rights reserved.")
                group.post(text="BOT: " + help1)
                group.post(text="BOT: " + help2)
                print("Help command posted")

            # Collect the number of posts from a supplied user
            elif "!numPosts" in newestmessage.text and newestmessage.text != help1 and newestmessage.text != help2:
                print(newestmessage.name + " executed numPosts")
                try:
                    searchMember = re.search(":(.*):", newestmessage.text).group(1)
                    group.post(text="BOT: " + searchMember + " has posted " + str(numMemberPosts(groupname, searchMember)) + " time(s)")
                    print("Ran command")
                except:
                    print("Couldn't find member")

            # Search for a keyword and return number of messages it occurred in
            elif "!searchKey" in newestmessage.text and newestmessage.text != help1 and newestmessage.text != help2:
                print(newestmessage.name + " executed searchKey")
                try:
                    searchKey = re.search(":(.*):", newestmessage.text).group(1)
                    list = []
                    list.append(searchKey)
                    group.post(text="BOT: " + searchKey + " has appeared in " + str(countKeywords(groupname, list)) + " message(s)")
                    print("Ran command")
                except:
                    print("An error occurred")

            # List member details (name, nickname, and user_id) of the group
            elif "!listMembers" == newestmessage.text:
                print(newestmessage.name + " executed listMembers")
                group.post(text="BOT: " + listMembers(groupname))
                print("Ran command")

            # Post number of posts for each member and total posts in a group
            elif "!allNumPosts" in newestmessage.text and newestmessage.text != help1  and newestmessage.text != help2:
                print(newestmessage.name + " executed allNumPosts")
                group.post(text="BOT: " + allNumPosts(groupname))
                print("Ran command")

            # Post percentage of total posts per member
            elif "!percentPosts" in newestmessage.text and newestmessage.text != help1 and newestmessage.text != help2:
                print(newestmessage.name + " executed allMemberPercentPosts")
                group.post(text="BOT: " + allMemberPercentPosts(groupname))
                print("Ran command")

            # Search for a keyword posted by a given member
            elif "!keyByMem" in newestmessage.text and newestmessage.text != help1 and newestmessage.text != help2:
                print(newestmessage.name + " executed keyByMem")
                passedarg = re.search(":(.*):", newestmessage.text).group(1)
                searchargs = passedarg.split(",")
                keyword = searchargs[0]
                membername = searchargs[1]
                group.post(text=("BOT: " + membername + " posted " + str(searchKeyByMem(groupname, keyword, membername)) + " message(s) with " + keyword + " in it"))
                print("Ran command")

            ########## Begin admin commands ##########
            # Post a message a given number of times
            elif "!postMess" in newestmessage.text and newestmessage.text != help1 and newestmessage.text != help2:
                userid = findMember(groupname, newestmessage.name).user_id
                if userid in admins:
                    passedarg = re.search(":(.*):", newestmessage.text).group(1)
                    searchargs = passedarg.split(",")
                    message = searchargs[0]
                    numtimes = int(searchargs[1])
                    postMessage(groupname, message, numtimes)
                else:
                    group.post(text="BOT: " + "Sorry " + newestmessage.name + ", you are not an admin")
                    print(newestmessage.name + " attempted to run postMess")

            # Add a new admin
            elif "!addAdmin" in newestmessage.text and newestmessage.text != help1 and newestmessage.text != help2:
                addAdmin = re.search(":(.*):", newestmessage.text).group(1)
                userid = findMember(groupname, addAdmin).user_id
                if userid in admins:
                    group.post("BOT: " + addAdmin + " is already an admin")
                elif newestmessage.user_id in admins:
                    admins.append(userid)
                    group.post(text="BOT: " + "Added " + addAdmin + " to the admins list")
                    print(newestmessage.name + " added " + addAdmin + " to the admins list")
                else:
                    group.post(text="BOT: " + "Sorry " + newestmessage.name + ", you are not an admin")
                    print(newestmessage.name + " attempted to elevate " + addAdmin + " to admin")

            # Remove an admin
            elif "!removeAdmin" in newestmessage.text and newestmessage.text != help1 and newestmessage.text != help2:
                removeAdmin = re.search(":(.*):", newestmessage.text).group(1)
                userid = findMember(groupname, removeAdmin).user_id
                if admins[0] == userid:
                    group.post("BOT: " + "Consider " + removeAdmin + " a 'super admin'. Can't remove from the admin list")
                    print(newestmessage.name + " attempted to remove " + removeAdmin + " from the admin list")
                elif userid not in admins:
                    group.post(text="BOT: " + removeAdmin + " isn't an admin")
                elif newestmessage.user_id in admins:
                    admins.remove(userid)
                    group.post(text="BOT: " + "Removed " + removeAdmin + " from the admins list")
                    print("Removed " + removeAdmin + " from the admins list")
                else:
                    group.post(text="BOT: " + "Sorry, you are not an admin")
                    print(newestmessage.name + " attempted to elevate " + addAdmin + " to admin")

            # End the bot
            elif "!endBot" == newestmessage.text:
                if newestmessage.user_id in admins:
                    group.post(text="BOT: " + "Stopping bot")
                    print(newestmessage.name + " ended bot")
                    exit()
                else:
                    group.post(text="BOT: " + "Sorry, you are not an admin")
                    print(newestmessage.name + " attempted to end the bot")

            # If none of the above commands were run, it must not be a command
            elif newestmessage.text[0] == "!":
                group.post("Unrecognized command")
                print(newestmessage.name + " attempted to run " + newestmessage.text)

        # Need to catch a network exception
        except requests.exceptions.HTTPError as net:
            print("Broke network connection")
            try:
                print("Rebuilding network connection")
                monBot(groupname)
            except Exception as e:
                print("Couldn't rebuild connection: " + str(e))
                exit()

        # Print any exception that occurs and end runtime
        except Exception as e:
            print(str(e))
            exit()

if str(sys.argv[1]) == "help":
    print("Available options:\n\t"
            "monBot takes a groupname\n\t"
            "repeater takes groupname, membername, and boolean quiet start\n\t"
            "getAttr prints information about different GroupMe objects\n\t"
            "")
elif str(sys.argv[1]) == "monBot":
    monBot(sys.argv[2])
elif str(sys.argv[1]) == "repeater":
    repeater(sys.argv[2], sys.argv[3], sys.argv[4])
elif str(sys.argv[1]) == "getAttr":
    getAttributes(sys.argv[2])
elif str(sys.argv[1]) == "percentPosts":
    print(allMemberPercentPosts(sys.argv[2]))
