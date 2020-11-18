# Groupy is a downloadable package: https://pypi.org/project/GroupyAPI/
# GroupMe Developer page has instructions on how to get your GroupMe token: https://dev.groupme.com/
# Make a creds.py file in the same directory as this file, create a variable called token and paste your token as a string
from creds import token, exceptionlist
from groupy.client import Client
from groupy import attachments
import datetime, sys, requests, json

client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()
chats = client.chats.list_all()

# Find the percentage of likes per member given to messages that are not each individual member's
def numLikesGiven(groupname):
    group = findGroup(groupname)
    totalposts = 0

    print("Filling memberdict...")
    memberdict = {}
    for member in group.members:
        # key = member user ID, value = [member name, likes given, and posts posted]
        memberdict[member.user_id] = [member.name, 0, 0]

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    print("Filling likes...")
    for message in messagelist:
        # Add one to the total posts
        totalposts += 1
        try:
            # Add one to the relevant member's total posts
            memberdict[message.user_id][2] += 1
        except KeyError:
            pass
        except Exception as e:
            print(f"Error occurred {e}")

        for messagelike in message.favorited_by:
            try:
                # Add a like to each member in the favorited_by list
                memberdict[messagelike][1] += 1
            except KeyError:
                pass
            except Exception as e:
                print(f"Error occurred {e}")

    print("Sorting memberdict...")
    # Sort by number of likes given
    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1][1], reverse=True)

    print("Writing results...")
    with open(f"./PercentageLikes.txt", "a") as writer:
        writer.write(f"\n\nPercentage of likes given of messages not posted by member in {group.name}...\n")
        for entry in sorted_memberdict:
            name = entry[1][0]
            likedmessages = entry[1][1]
            posts = entry[1][2]
            otherposts = totalposts - posts
            writer.write(f"{name} liked {round(likedmessages/otherposts*100,2)}% of {otherposts} messages\n")

# Pull GroupMe gallery URLs and user IDs into file as .csv
# Code from https://github.com/xkel/GroupMe-Image-Bot/blob/master/bot.py was heavily used
def pullGallery(groupname):
    group = findGroup(groupname)
    base_url = "https://api.groupme.com/v3"
    url = f"/groups/{group.id}/messages"
    params = {"token": token}
    messagesResponse = requests.get(base_url + url, params = params).json()
    msg_count = messagesResponse["response"]["count"]
    img_list = []
    usr_list = []
    i = 0
    x = 0

    print("Filling image list...")
    while i < msg_count:
        if(x < 20):
            if(messagesResponse["response"]["messages"][x]["attachments"] == []):
                pass
            else:
                if(messagesResponse["response"]["messages"][x]["attachments"][0]["type"] == "image"):
                    img_url = messagesResponse["response"]["messages"][x]["attachments"][0]["url"]
                    usr_url = messagesResponse["response"]["messages"][x]["user_id"]
                    img_list.append(img_url)
                    usr_list.append(usr_url)
                    print("Image " + str(i) + "/" + str(msg_count) + " collected", end="\r")
            if(x == 19):
                id = messagesResponse["response"]["messages"][x]["id"]
            x += 1
        else:
            params = {"token": token, "before_id": id}
            try:
                messagesResponse = requests.get(base_url + url, params = params).json()
                x = 0
            except:
                pass
                x = 20
        i += 1

    print("Writing to file...")
    num = 0
    with open(f".\\Images\\Images_{group.name}.csv", "w") as writer:
        for index in img_list:
            writer.write(index + "," + usr_list[num] + "\n")
            num += 1

# Download images from URLs in stored file from pullGallery() and label with member name
def downImages(groupname):
    group = findGroup(groupname)
    ext = ""
    filenum = 1
    memberdict = {}

    print("Filling memberdict...")
    for member in group.members:
        memberdict[member.user_id] = member.name

    print("Reading file...")
    with open(f".\\Images\\Images_{group.name}.csv", "r") as reader:
        lines = reader.readlines()

    print("Downloading images...")
    for line in lines:
        splitline = line.strip().split(",")

        if "png" in splitline[0]:
            ext = ".png"
        elif "gif" in splitline[0]:
            ext = ".gif"
        elif "jpeg" in splitline[0]:
            ext = ".jpeg"
        else:
            ext = ".txt"

        try:
            membername = memberdict[splitline[1]]
        except:
            membername = "None"

        # Code inside with statement used from Stack Overflow answer on downloading images using requests
        with open(f".\\Images\\Image_{group.name}_{str(filenum)}_{membername}{ext}", "wb") as handle:
            try:
                response = requests.get(splitline[0], stream=True)
                if not response.ok:
                    print(response)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
            except Exception as e:
                print("Error on", filenum, ":", e)
                pass

        filenum += 1

# Write percentage of total images posted per member
def percentImagePost(groupname):
    group = findGroup(groupname)
    userdict = {}
    total = 0

    print("Reading file...")
    with open(f".\\Images\\Images_{group.name}.csv", "r") as reader:
        lines = reader.readlines()

    print("Creating user dictionary and counting images...")
    for line in lines:
        splitline = line.strip().split(",")
        if splitline[1] not in userdict.keys():
            userdict[splitline[1]] = 1
        else:
            userdict[splitline[1]] += 1

    for value in userdict.values():
        total += value

    print("Sorting list...")
    sorted_userdict = sorted(userdict.items(), key=lambda x: x[1], reverse=True)

    print("Writing file...")
    with open(f".\\Images\\PercentImages_{group.name}.txt", "w") as writer:
        try:
            writer.write("Total images: " + str(total) + "\n\n")
        except:
            print("Error")

        for item in sorted_userdict:
            try:
                writer.write(findMember(group, item[0]).name + " posted\n\t" + str(item[1]) + " images\n\t" + str(round(item[1]/total*100, 2)) + "%\n")
            except Exception as e:
                print(str(e))
                pass

# Write GroupMe video URLs from messages
def pullURL(groupname):
    group = findGroup(groupname)
    urllist = []

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    print("Searching messages...")
    for message in messagelist:
        try:
            if "v.groupme.com" in message.text:
                urllist.append(message.text)
        except:
            pass

    print("Writing URLs...")
    with open(f".\\URLs\\URLs_{group.name}.txt", "w") as writer:
        for index in urllist:
            try:
                writer.write(index + "\n")
            except:
                for character in index:
                    try:
                        writer.write(character)
                    except:
                        pass
                writer.write("\n")

# Capture the spread and stagger surrounding messages of the top posts most liked messages in a group
def mostLikedSprints(groupname, posts, spread, stagger):
    # Find group
    group = findGroup(groupname)
    # How many top posts should be written
    posts = int(posts)
    # How many surrounding messages should be written for each post
    spread = int(spread)
    # How far forward should the surrounding messages be staggered
    stagger = int(stagger)

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    # Create dictionary with key = message text and value = number of likes that message received
    likeddict = {}
    print("Finding number of likes/message...")
    for message in messagelist:
        likeddict[message.text] = len(message.favorited_by)

    # Sort likeddict by number of likes received
    print("Sorting messages...")
    sorted_likeddict = sorted(likeddict.items(), key=lambda x: x[1], reverse=True)

    print("Finding indexes for top liked messages...")
    num = 0
    # Create indexdict with key = message text and value = position of message in messagelist
    indexdict = {}
    while num < posts:
        # Create boolean to save time if message text is already found. Unsure if break is useable here
        done = False
        for message in messagelist:
            if done:
                pass
            elif message.text == sorted_likeddict[num][0]:
                indexdict[message.text] = messagelist.index(message)
                done = True
        num += 1

    print("Writing results...")
    with open(".\\LikeSpread\\LikeSpread_" + group.name + ".txt", "w") as writer:
        writer.write("Writing " + str(posts) + " total posts w/ a spread of " + str(spread) + " and staggered by " + str(stagger) + "\n\n")
        for likes in range(posts):
            try:
                writer.write("Message: " + sorted_likeddict[likes][0] + " - Likes: " + str(sorted_likeddict[likes][1]) + "\n")
            except:
                writer.write("Message: ")
                for character in str(sorted_likeddict[likes][0]):
                    try:
                        writer.write(character)
                    except:
                        pass
                writer.write(" - Likes: " + str(sorted_likeddict[likes][1]) + "\n")

        writer.write("\n\n")

        # indexdict values are the position of the message in messagelist
        for entry in indexdict.values():
            # Create an index equal to the last message to be written for each entry
            index = entry + spread - stagger
            while index >= entry - spread - stagger:
                try:
                    writer.write(messagelist[index].created_at.strftime('%Y-%m-%d %H:%M:%S') + " - " + messagelist[index].name + " - " + messagelist[index].text + "\n")
                except:
                    writer.write(messagelist[index].created_at.strftime('%Y-%m-%d %H:%M:%S') + " - " + messagelist[index].name + " - ")
                    for character in str(messagelist[index].text):
                        try:
                            writer.write(character)
                        except:
                            pass
                    writer.write("\n")

                index -= 1
            writer.write("\n\n")

# Find average number of posts per group w/o including outliers
def aveNumPostsPerGroup():
    return

# Find the longest message(s) sent in the group
def longestMess(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    longestmesslen = 0
    longestmesslist = []

    for message in messagelist:
        try:
            # Create a new list if the message is longer than the length of the previous list messages
            if len(list(message.text)) > longestmesslen:
                longestmesslist = [message]
                longestmesslen = len(list(message.text))
            # Otherwise, append the same length message to the current list
            elif len(list(message.text)) == longestmesslen:
                longestmesslist.append(message)
        except Exception as e:
            print("Exception occurred: ", e)
            pass

    for longestmess in longestmesslist:
        print((longestmess.created_at.strftime('%Y-%m-%d %H:%M:%S') + " - " + longestmess.name + " - " + longestmess.text + "\n"))
    print(str(longestmesslen))

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
    with open("TotalPosts.csv", "w") as writer:
        # writer.write("--- Descending Order of Total Posts per Group ---\n")
        for i in sorted_groupdict:
            try:
                writer.write(str(i[0]) + "," + str(i[1]) + "\n")
            except:
                pass
        # writer.write("\nFailed messages: " + str(failedcount) + "\nTotal Groups: " + str(numgroups))

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
        membername = findMember(group, i[0]).nickname
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
        writer.write("\n---------- Results for " + group.name + " ----------")
        writer.write("\n--- Words greater than " + str(num) + " letters ---")
        for member in memberdict.items():
            writer.write("\n" + findMember(group, member[0]).nickname + "'s most common words - \n")
            sorted_list = sorted(member[1].items(), key=lambda x: x[1], reverse=True)
            for x in range(10):
                try:
                    writer.write(sorted_list[x][0] + " - " + str(sorted_list[x][1]) + "\n")
                except:
                    pass
        writer.write("\n")

# Write a list of the most liked messages
def mostLikedMessages(groupname):
    mostlikeddict = {}
    nummessages = 50
    group = findGroup(groupname)
    messagelist = group.messages.list().autopage()

    for message in messagelist:
        mostlikeddict[message.text] = [len(message.favorited_by), message.name, message.created_at.strftime('%Y-%m-%d %H:%M:%S')]

    sorted_mostlikeddict = sorted(mostlikeddict.items(), key=lambda x: x[1][0], reverse=True)

    with open(".\\MostLikes\\MostLikes_" + group.name + ".txt", "w") as writer:
        for num in range(nummessages):
            try:
                writer.write(sorted_mostlikeddict[num][1][2] + " - " + sorted_mostlikeddict[num][1][1] + " - " + sorted_mostlikeddict[num][0] + " --- got " + str(sorted_mostlikeddict[num][1][0]) + " likes\n\n" )
            except:
                pass
                writer.write(sorted_mostlikeddict[num][1][2] + " - " + sorted_mostlikeddict[num][1][1] + " - ")
                if sorted_mostlikeddict[num][0] != None:
                    for character in sorted_mostlikeddict[num][0]:
                        try:
                            writer.write(character)
                        except:
                            pass
                writer.write(" --- got " + str(sorted_mostlikeddict[num][1][0]) + " likes\n\n")

# Print a sorted list of the people that got 1+ likes
def numLikes(groupname):
    group = findGroup(groupname)

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    print("Creating memberdict...")
    memberdict = {}
    for member in group.members:
        # Key = member user id, value = member name, messages that got at least one like, number of messages posted
        memberdict[member.user_id] = [member.name, 0, 0]

    print("Counting likes...")
    for message in messagelist:
        try:
            memberdict[message.user_id][2] += 1
            if len(message.favorited_by) > 0:
                memberdict[message.user_id][1] += 1
        except:
            pass

    print("Sorting memberdict...")
    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1][1], reverse=True)

    likedict = {}
    for entry in sorted_memberdict:
        try:
            likedict[entry[1][0]] = round(entry[1][1]/entry[1][2]*100,2)
        except:
            print(f"{entry[1][0]} had a division issue")
            pass

    print("Sorting likedict...")
    sorted_likedict = sorted(likedict.items(), key=lambda x: x[1], reverse=True)

    print("Writing results...")
    with open(".\MoreLikes.txt", "a") as writer:
        writer.write("\nPosts that got 1+ likes\n")
        for entry in sorted_likedict:
            writer.write(f"{entry[0]}: {entry[1]}% of {memberdict[findMember(group, entry[0]).user_id][2]} posts\n")

# Find average length of message in characters per member
def averMessLength(groupname):
    totalposts = 0
    memberdict = {}
    failedmessages = 0
    group = findGroup(groupname)

    print("Filling messagelist...")
    messagelist = group.messages.list().autopage()

    # memberdict value has a two index list.
    # index 0 = number of characters posted
    # index 1 = number of messages posted
    print("Creating memberdict...")
    for member in group.members:
        memberdict[member.user_id] = [0,0]

    print("Filling memberdict...")
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
    print("Sorting memberdict...")
    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1][1], reverse=True)

    print("Writing data...")
    with open(".\\SortedCharCount\\SortedCharCount_" + group.name + ".txt", "w") as writer:
        writer.write("--- " + group.name + " Character Averages Sorted by Total Messages ---\n")
        for member in sorted_memberdict:
            try:
                writer.write(str(findMember(group,member[0]).nickname) + "\n\tAverage character count per message - " + str(round(member[1][0]/member[1][1]))+ "\n\tTotal messages - " + str(member[1][1]) + "\n\tPercentage of group's posts - " + str(round(member[1][1]/totalposts*100, 2)) + "%\n")
            # Common exception is going to be divide by zero
            except Exception as e:
                print("Exception occurred: ", e)
                pass
        writer.write("\n")

    print("Total messages - " + str(totalposts))
    print("Failed messages - " + str(failedmessages))

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

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    if easyread:
        sep = " - "
        extension = ".txt"

        with open(".\\EasyRead\\" + group.name + " Messages" + extension, "w") as messagewriter:
            num = len(messagelist) - 1
            while num >= 0:
                message = messagelist[num]
                try:
                    messagewriter.write(message.created_at.strftime('%Y-%m-%d %H:%M:%S') + sep + message.name + sep + message.text + "\n")
                except:
                    counter += 1
                    pass
                num -= 1
    else:
        sep = "`"
        extension = ".csv"

        with open(".\\Backup CSVs\\" + group.name + " Messages" + extension, "w") as messagewriter:
            num = len(messagelist) - 1
            while num >= 0:
                message = messagelist[num]
                try:
                    messagewriter.write(message.created_at.strftime('%Y-%m-%d %H:%M:%S') + sep + message.name + sep + message.user_id + sep + message.text + "\n")
                except:
                    counter += 1
                    pass
                num -= 1

    print(str(counter) + " errors occurred in writing messages\n")

# Searches given group for keyword (string, string)
def searchForKeyword(groupname, keyword):
    keywordlist = []
    group = findGroup(groupname)

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    print("Searching messages...")
    for message in messagelist:
        try:
            if keyword in message.text:
                keywordlist.append(message)
        except:
            pass

    for index in keywordlist:
        print(index.name + ": " + index.text)

# Find group and return group object
def findGroup(groupname):
    print("Looking for " + groupname)
    for group in groups.autopage():
        if group.name.lower() == groupname.lower():
            print("Found " + group.name)
            return group
    print("Couldn't find group: " + repr(groupname))
    return None

# Given a group object and member name string, return the member object
def findMember(group, membername):
    for member in group.members:
        if member.name == membername or member.nickname == membername or member.user_id == membername:
            print("Found " + member.name)
            return member
    print("Couldn't find " + membername)
    return None

if str(sys.argv[1]) == "help":
    print("Available options:\n\n\t"
            "delta - only make backups of changed groupmes\n\t"
            "find - search for a given group name\n\t"
            "names - create GroupNames.txt containing all active groups\n\t"
            "averMessLength - Find individualized stats for a group (takes group name)\n\t"
            "numLikes - Find number of messages per member that got 1+ like (takes group name) \n\t"
            "mostLikedMessages - Return the top five most liked messages (takes group name)\n\t"
            "commonWords - Return most said words per member (takes group name)\n\t"
            "myinfo - Return current user info\n\t"
            "percent - Return sorted list of percentage of posts per member (takes group name)\n\t"
            "groupNum - Return sorted list of total posts per group\n\t"
            "sharedGroups - Return list of shared groups per member\n\t"
            "writeChats - Write DMs to file\n\t"
            "longestMess - Print longest message from specified group (takes group name)\n\t"
            "mostLikedSprints - Write most liked posts surrounded by provided number of messages (takes group name, number of posts to write, number of messages behind and in front, and stagger)\n\t"
            "pullURL - Write GroupMe video URLs to file (takes group name)\n\t"
            "pullGallery - Write gallery URLs to file (takes group name)\n\t"
            "downImages - Download gallery photos from pullGallery() file (takes group name)\n\t"
            "percentImagePost - Write percentage of images posted per member (takes group name)\n\t"
            "numLikesGiven - Show the percentage of posts liked that weren't posted by the member (takes group name)\n\t"
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
elif (str(sys.argv[1])) == "longestMess":
    longestMess(str(sys.argv[2]))
elif sys.argv[1] == "mostLikedSprints":
    mostLikedSprints(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
elif sys.argv[1] == "pullURL":
    pullURL(sys.argv[2])
elif sys.argv[1] == "pullGallery":
    pullGallery(sys.argv[2])
elif sys.argv[1] == "downImages":
    downImages(sys.argv[2])
elif sys.argv[1] == "percentImagePost":
    percentImagePost(sys.argv[2])
elif sys.argv[1] == "numLikesGiven":
    numLikesGiven(sys.argv[2])
else:
    print("Command doesn't exist")
