# GroupMe Developer page has instructions on how to get your GroupMe token: https://dev.groupme.com/
from creds import token
# Groupy is a downloadable package: https://pypi.org/project/GroupyAPI/
from groupy.client import Client
from time import sleep
import datetime

client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()

# Print all your active groups
def printGroupNames():
    counter = 0
    for group in groups.autopage():
        print(group.name)
        counter += 1
    print("Number of Groups: " + str(counter))

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

# List members of a given group name (string)
def listMembers(groupname):
    group = findGroup(groupname)
    for member in group.members:
        print("Member name - " + member.name)
        print("Member nickname - " + member.nickname)
        print("Member ID - " + member.user_id)

# Post message in group a given number of times. Takes (string, string, int)
def postMessage(groupname, message, numtimes):
    group = findGroup(groupname)
    for num in range(numtimes):
        group.post(text=message)

# List all messages in a given group (string)
def listAllMessages(groupname):
    counter = 0
    group = findGroup(groupname)
    allmess = list(group.messages.list().autopage())
    # print(str(allmess[len(allmess) - 1]))
    num = len(allmess) - 1
    with open(groupname + " MessagesID.csv", "w") as messagewriter:
        while num >= 0:
            message = allmess[num]
            num -= 1
            try:
                # if message != None or message.name != None or not None in message.text:
                messagewriter.write(message.created_at.strftime('%Y-%m-%d %H:%M:%S') + "`" + message.name + "`" + message.user_id + "`" + message.text + "\n")
            except:
                counter += 1
                pass
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

# Find the number of posts from each member in a given group (string)
def numMemberPosts(groupname):
    memberdict = {}
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()
    for message in messagelist:
        try:
            if "GroupMe" in message.name:
                pass
            elif message.name not in memberdict:
                memberdict[message.name] = 1
            else:
                memberdict[message.name] += 1
            if message.name.user_id not in memberdict:
                memberdict[message.name.user_id] = 1
            else:
                memberdict[message.name.user_id] += 1
        except:
            pass
    sorted_members = sorted((value, key) for (key, value) in memberdict.items())
    for index in sorted_members:
        print(index)
    return

# Count the number of times a keyword(s) appears in a given group. Takes (string, list)
def countKeywords(groupname, keywordlist):
    count = 0
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()
    for message in messagelist:
        for keyword in keywordlist:
            try:
                if keyword in message.text:
                    # print(message)
                    count += 1
            except:
                pass
    print(str(count))
    return

def getAttributes(groupname):
    group = findGroup(groupname)
    print(str(dir(group.messages.list()[0])))
    print(str(group.messages.list()[0].data))
    # timestamp = datetime.datetime.fromtimestamp(group.messages.list()[0].created_at)
    print(group.messages.list()[0].created_at.strftime('%Y-%m-%d %H:%M:%S'))

# Find group and return group object
def findGroup(groupname):
    print("Looking for " + groupname)
    for group in groups.autopage():
        if group.name == groupname:
            print("Found " + group.name)
            return group
    print("Couldn't find group. Exiting...")
    exit()

# Given a string name, return the member object in a group
def findMember(groupname, membername):
    group = findGroup(groupname)
    for member in group.members:
        if member.name == membername:
            print("Found " + member.name)
            return member
    print("Couldn't find member. Exiting...")
    exit()

# Repeat everything a provided user (string) in a provided group (string) says starting and ending with a key string
def repeater(groupname, membername):
    counter = 0
    startbot = False
    sleeptime = 3

    group = findGroup(groupname)
    member = findMember(groupname, membername)

    while startbot == False:
        newestmessage = group.messages.list()[0]
        if str(newestmessage.name) == "Brant Goings" and str(newestmessage.text) == "Execute Order 66":
            group.post(text="It will be done, my lord. The youngling is " + member.name)
            startbot = True
            print("Start order given")
        else:
            print("Waiting for start order")
            sleep(sleeptime)

    while True:
        newestmessage = group.messages.list()[0]
        if str(newestmessage.name) == "Brant Goings" and str(newestmessage.text) == "It is done, my lord.":
            group.post(text="Well done, Lord Goings. Once more the Sith shall rule the galaxy!")
            print("Kill order given")
            break
        elif str(newestmessage.name) == member.name:
            group.post(text= ("'" + newestmessage.text + "' is something a Jedi would say. We are watching you."))
            print(str(newestmessage.name) + " said " + str(newestmessage.text))
        sleep(sleeptime)
    print("Bot ended")
    return

def runTime():
    commands = input("Welcome to the Python GroupMe program\n\n"
                        "You have some options (separate multiple options by commas without spaces):\n"
                        "\t 1. Print group names to console\n"
                        "\t 2. Print group names to file\n"
                        "\t 3. Post a message x number of times\n"
                        "\t 4. Print all messages of a group to the console\n"
                        "\t 5. Print any message that contains a keyword in a group\n"
                        "\t 6. Print the number of times each member has posted in a group\n"
                        "\t 7. Run repeater for a given group and user\n"
                        "Enter an option: ")
    runcommands = commands.split(",")

    for runcommand in runcommands:
        if runcommand == "1":
            printGroupNames()
        elif runcommand == "2":
            printGroupNamesToFile()
            print("All group names printed to GroupNames.txt")
        elif runcommand == "3":
            group = input("What's the group name? ")
            message = input("What's the message ")
            numtimes = (int)(input("How many times should this message be posted? "))
            postMessage(group, message, numtimes)
        elif runcommand == "4":
            group = input("What's the group name? ")
            listAllMessages(group)
        elif runcommand == "5":
            group = input("What's the group name? ")
            keyword = input("What's the keyword/phrase? ")
            searchForKeyword(group, keyword)
        elif runcommand == "6":
            group = input("What's the group name? ")
            numMemberPosts(group)
        elif runcommand == "7":
            group = input("What's the group name? ")
            member = input("What's the target member name? ")
            repeater(group, member)
