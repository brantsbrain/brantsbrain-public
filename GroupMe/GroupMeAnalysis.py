# Import necessary methods from Finders
from GroupMeFinders import findGroup, findMember, convertCreatedAt

# Get modules/packages
import sys
from creds import token, exceptionlist, bulklist
from groupy.client import Client
from datetime import datetime, timezone

# Instantiate variables to be used throughout
client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()
chats = client.chats.list_all()

# Find the total number of messages sent from provided members in a given list across all groups
# bulklist is imported from creds.py
def boardMessages():
    memberdict = {}
    grouplist = list(groups.autopage())

    print("Finding bulklist members...")
    for group in grouplist:
        if len(bulklist) == len(memberdict):
            print("Found all members...")
            break

        # Only looking for members in the bulklist
        for index in bulklist:
            member = findMember(group, index)
            # findMember() will return None if it couldn't find the member. Check to make sure member is True
            if member:
                # If true, check to see if the user id is in memberdict keys yet
                if member.user_id not in memberdict.keys():
                    memberdict[member.user_id] = {"messages" : 0, "memberobject" : member, "sharedgroups" : 0}
                    print(f"Created {member.name} in dictionary")

    # Print which members weren't found if any
    if len(bulklist) != len(memberdict):
        print("Couldn't find all members")
        checklist = bulklist
        for index in checklist:
            for value in memberdict.values():
                if value["memberobject"].name in checklist:
                    checklist.remove(value["memberobject"].name)
                elif value["memberobject"].nickname in checklist:
                    checklist.remove(value["memberobject"].nickname)
        for index in checklist:
            print(f"{index} won't be recorded")

    print("\nBegin working on groups...")
    for group in grouplist:
        print(f"Working on {group.name}...")

        # Instantiate evallist boolean to skip listing messsages if possible
        evallist = False
        for member in group.members:
            # Only looking for members created in the memberdict dictionary earlier
            if member.user_id in memberdict.keys():
                evallist = True
                print(f"Shared with {member.name}")
                # Increase shared groups by 1
                memberdict[member.user_id]["sharedgroups"] += 1

        # If not shared by any members, skip
        if evallist == False:
            print("No shared members, skipping messages...")
        # else iterate through the message list and increase counters by one for each bulklist member
        else:
            print("Building and searching messagelist...")
            messagelist = list(group.messages.list().autopage())
            for message in messagelist:
                if message.user_id in memberdict.keys():
                    memberdict[message.user_id]["messages"] += 1
        # Space out groups
        print()

    print("Printing results...")
    for valuelist in memberdict.values():
        print(f"{valuelist['memberobject'].name} posted {valuelist['messages']} total messages in all {valuelist['sharedgroups']} shared groups")

# Find the longest message(s) sent in the group
def longestMess(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    longestmesslen = 0
    longestmesslist = []

    for message in messagelist:
        try:
            # Create a new list if the message is longer than the length of the previous list messages
            if len(str(message.text)) > longestmesslen:
                longestmesslist = [message]
                longestmesslen = len(str(message.text))
            # Otherwise, append the same length message to the current list
            elif len(str(message.text)) == longestmesslen:
                longestmesslist.append(message)
        except Exception as e:
            print(f"Exception occurred: {e}")
            pass

    for longestmess in longestmesslist:
        print(f"{convertCreatedAt(longestmess)} - {longestmess.name} - {longestmess.text}\n")
    print(f"Length: {longestmesslen}")

# List number of shared groups with all users
def sharedGroups():
    memberdict = {}
    for group in groups.autopage():
        for member in group.members:
            if member.name == myuser["name"]:
                pass
            elif member.user_id in memberdict.keys():
                memberdict[member.user_id]["sharedgroups"] += 1
            else:
                memberdict[member.user_id] = {"name" : member.name, "sharedgroups" : 1}

    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1]["sharedgroups"], reverse=True)

    with open("SharedGroups.txt", "w") as writer:
        writer.write("--- Descending Order of Shared Groups ---\n")
        for i in sorted_memberdict:
            try:
                writer.write(f"{i[1]['name']} - {i[1]['sharedgroups']}\n")
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
            print(f"Error building {group.name}")
        numgroups += 1

    sorted_groupdict = sorted(groupdict.items(), key=lambda x: x[1], reverse=True)
    with open("TotalPosts.csv", "w") as writer:
        # writer.write("--- Descending Order of Total Posts per Group ---\n")
        for i in sorted_groupdict:
            try:
                writer.write(f"{i[0]}, {i[1]}\n")
            except:
                pass
        writer.write(f"\n\nFailed messages (not groups): {failedcount}\nTotal Groups: {numgroups}")

# List percentage of posts for all users
def allMemberPercentPosts(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    memberdict = {}
    details = ""
    counter = 0

    # Instantiate the memberdict member objects with counters at 0
    for member in group.members:
        memberdict[member.user_id] = 0

    # For each message, increase message.user_id value by 1 and total counter by 1.
    for message in messagelist:
        memberdict[message.user_id] += 1
        counter += 1

    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1], reverse=True)
    for i in sorted_memberdict:
        membername = findMember(group, i[0]).name
        details = details + membername + " - " + str(round(i[1]/counter*100, 2)) + "%\n"
    details = details + "\nTotal posts - " + str(counter)

    with open("PercentagePosts.txt", "a+") as writer:
        writer.write(f"\n\n--- Percentage of Total Posts for {groupname} out of {len(group.members)} members and {counter} posts ---\n")
        writer.write(details)

# List most common words used per member
def commonWords(groupname, num):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    num = int(num)
    memberdict = {}
    wordlist = []

    print("Filling memberdict...")
    for member in group.members:
        memberdict[member.user_id] = {}

    print("Searching messages...")
    # This can be optimized...
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
    with open(f".\\CommonWords\\TopWords_{group.name}.txt", "w") as writer:
        writer.write(f"\n---------- Results for {group.name} ----------")
        writer.write(f"\n--- Words greater than {num} letters ---")
        for member in memberdict.items():
            writer.write(f"\n{findMember(group, member[0]).name}'s most common words - \n")
            sorted_list = sorted(member[1].items(), key=lambda x: x[1], reverse=True)
            for x in range(10):
                try:
                    writer.write(sorted_list[x][0] + " - " + str(sorted_list[x][1]) + "\n")
                except:
                    pass
        writer.write("\n")

# Find average length of message in characters per member
def averMessLength(groupname):
    group = findGroup(groupname)
    totalposts = 0
    memberdict = {}
    failedmessages = 0

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    print("Creating memberdict...")
    for member in group.members:
        memberdict[member.user_id] = {"numchars" : 0, "messages" : 0}

    print("Filling memberdict...")
    for message in messagelist:
        totalposts += 1
        memberdict[message.user_id]["messages"] += 1
        try:
            for character in message.text:
                memberdict[member.user_id]["numchars"] += 1
        except:
            failedmessages += 1
            pass

    # Sort by number of posts per member
    print("Sorting memberdict...")
    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1]["messages"], reverse=True)

    print("Writing data...")
    with open(".\\SortedCharCount\\SortedCharCount_" + group.name + ".txt", "w") as writer:
        writer.write("--- " + group.name + " Character Averages Sorted by Total Messages ---\n")
        for member in sorted_memberdict:
            try:
                writer.write(""
                            f"{findMember(group,member[0]).name}\n\t"
                            f"Average character count per message - {round(member[1]['numchars']/member[1]['messages'])}\n\t"
                            f"Total messages - {member[1]['messages']}\n\t"
                            f"Percentage of group's posts - {round(member[1]['messages']/totalposts*100, 2)}%\n"
                            "")
            # Common exception is going to be divide by zero
            except Exception as e:
                print(f"Exception occurred with {findMember(group,member[0]).name}: {e}")
                pass
        writer.write("\n")

    print("Total messages - " + str(totalposts))
    print("Failed messages - " + str(failedmessages))

# Display attributes of the group, member, message, and user.get_me() objects
def getAttributes():
    # Take arbitrary first group in groups list
    group = groups[0]

    print("\n--- Group Attributes ---")
    for key, value in group.data.items():
        # The members key is unique, so skip for now
        if key == "members":
            print(f"{key} - List of dictionary items in '--- Member Attributes ---' below")
        # Print all attributes of the group object
        else:
            print(f"{key} - {value}")

    print("\n--- Member Attributes ---")
    for key in group.data.keys():
        # Find the members key and print attributes of first member in it
        if key == "members":
            for index in group.data[key]:
                for key, value in index.items():
                    print(f"{key} - {value}")
                # Only print details for first member, then break out to top layer in function
                break

    print("\n--- Message Attributes ---")
    for key, value in group.messages.list()[0].data.items():
        # Print attributes of arbitrary first message in group
        print(f"{key} - {value}")

    print("\n--- My User Attributes ---")
    # Print attributes of the myuser dictionary
    for key, value in myuser.items():
        print(f"{key} - {value}")
