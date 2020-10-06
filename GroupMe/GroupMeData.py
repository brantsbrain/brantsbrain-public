# Groupy is a downloadable package: https://pypi.org/project/GroupyAPI/
# GroupMe Developer page has instructions on how to get your GroupMe token: https://dev.groupme.com/
# Make a creds.py file in the same directory as this file, create a variable called token and paste your token as a string
from creds import token, exceptionlist
from groupy.client import Client
import datetime, sys

client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()
chats = client.chats.list_all()

# Write DMs to file
def writeChats():
    counter = 0
    with open("DirectMessages.txt", "w") as writer:
        for chat in chats:
            chatlist = list(chat.messages.list().autopage())
            num = len(chatlist) - 1
            writer.write("---------- " + chat.other_user["name"] + " - " + str(num + 1) + " ----------\n")
            while num >= 0:
                message = chatlist[num]
                try:
                    writer.write(message.created_at.strftime('%Y-%m-%d %H:%M:%S') + " - " + message.name + " - " + message.text + "\n")
                except:
                    try:
                        writer.write(message.created_at.strftime('%Y-%m-%d %H:%M:%S') + " - " + message.name + " - ")
                        for character in message.text:
                            writer.write(character)
                    except:
                        writer.write("\n")
                        pass
                num -= 1
            writer.write("\n")

# List number of shared groups with all users
def sharedGroups():
    memberdict = {}
    for group in groups.autopage():
        for member in group.members:
            if member.name == myuser["name"]:
                pass
            elif member.user_id in memberdict.keys():
                memberdict[member.user_id][1] += 1
            else:
                memberdict[member.user_id] = [member.name, 1]

    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1][1], reverse=True)

    with open("SharedGroups.txt", "w") as writer:
        writer.write("--- Descending Order of Shared Groups ---\n")
        for i in sorted_memberdict:
            try:
                writer.write(str(i[1][0]) + " - " + str(i[1][1]) + "\n")
            except:
                pass

# Ordered list by total number of posts
def totalPostsPerGroup():
    counter = 0
    failedcount = 0
    groupdict = {}
    details = ""
    numgroups = 0

    for group in groups.autopage():
        try:
            print("Building " + group.name + "...")
            for message in group.messages.list().autopage():
                try:
                    counter += 1
                except:
                    failedcount += 1
            groupdict[group.name] = counter
            counter = 0
        except:
            print("Error finding " + group.name)
        numgroups += 1

    sorted_groupdict = sorted(groupdict.items(), key=lambda x: x[1], reverse=True)
    with open("TotalPosts.txt", "a+") as writer:
        writer.write("--- Descending Order of Total Posts per Group ---\n")
        for i in sorted_groupdict:
            try:
                writer.write(str(i[0]) + " - " + str(i[1]) + "\n")
            except:
                pass
        writer.write("\nFailed messages: " + str(failedcount) + "\nTotal Groups: " + str(numgroups))

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
    for i in sorted_memberdict:
        membername = findMember(groupname, i[0]).nickname
        details = details + membername + " - " + str(round(i[1]/counter*100, 2)) + "%\n"
    details = details + "\nTotal posts - " + str(counter)

    with open("PercentagePosts.txt", "a+") as writer:
        writer.write("\n\n--- Percentage of Total Posts for " + groupname + " out of " + str(len(group.members)) + " members and " + str(counter) + " posts ---\n" + details)

# List most common words used per member
def commonWords(groupname):
    memberdict = {}
    wordlist = []
    num = 5
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
        writer.write("\n---------- Results for " + groupname + " ----------")
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
    likefloor = 3
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()

    for member in group.members:
        memberdict[member.user_id] = [0,0]

    for message in messagelist:
        for x,y in memberdict.items():
            if message.user_id == x:
                if len(message.favorited_by) >= likefloor:
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
    totalposts = 0
    memberdict = {}
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()
    failedmessages = 0

    # memberdict value has a two index list.
    # index 0 = number of characters posted
    # index 1 = number of messages posted
    for member in group.members:
        memberdict[member.user_id] = [0,0]

    for message in messagelist:
        totalposts += 1
        for member in memberdict.keys():
            if message.user_id == member:
                memberdict[member][1] += 1
                try:
                    for character in message.text:
                        memberdict[member][0] += 1
                except:
                    failedmessages += 1
                    pass

    # Sort by number of posts per member
    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1][1], reverse=True)

    with open(".\\SortedCharCount\\SortedCharCount_" + groupname + ".txt", "w") as writer:
        writer.write("--- " + groupname + " Character Averages Sorted by Total Messages ---\n")
        for member in sorted_memberdict:
            try:
                writer.write(str(findMember(groupname,member[0]).nickname) + "\n\tAverage character count per message - " + str(round(member[1][0]/member[1][1]))+ "\n\tTotal messages - " + str(member[1][1]) + "\n\tPercentage of group's posts - " + str(round(member[1][1]/totalposts*100, 2)) + "%\n")
            except:
                # Common exception is going to be divide by zero
                pass
        writer.write("\n")
    print("Total messages - " + str(totalposts))
    print("Failed messages - " + str(failedmessages))

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
    print(myuser["name"])

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
            "averMessLength - Find individualized stats for a group\n\t"
            "numLikes - Find number of messages per member that meet a like floor\n\t"
            "mostLikedMessages - Return the top five most liked messages\n\t"
            "commonWords - Return most said words per member\n\t"
            "myinfo - Return current user info\n\t"
            "percent - Return sorted list of percentage of posts per member\n\t"
            "groupNum - Return sorted list of total posts per group\n\t"
            "sharedGroups - Return list of shared groups per member\n\t"
            "writeChats - Write DMs to file\n\t"
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
elif str(sys.argv[1]) == "myinfo":
    print("Running myinfo()")
    printMyInfo()
elif str(sys.argv[1]) == "percent":
    print("Running allMemberPercentPosts()")
    allMemberPercentPosts(sys.argv[2])
elif str(sys.argv[1]) == "groupNum":
    print("Running totalPostsPerGroup()")
    totalPostsPerGroup()
elif str(sys.argv[1]) == "sharedGroups":
    print("Running sharedGroups()")
    sharedGroups()
elif (str(sys.argv[1])) == "writeChats":
    writeChats()
