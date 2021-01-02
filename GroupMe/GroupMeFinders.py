# Get modules/packages
import sys
from groupy.client import Client
from datetime import datetime, timezone
from creds import token, skipgrouplist, refgroup

# Instantiate variables to be used throughout
client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()
chats = client.chats.list_all()
grouplist = list(groups.autopage())

# Find all names members have had in a group
def findNames(groupname, findoutmem):
    group = findGroup(groupname)
    memberdict = {}

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    print("Populating memberdict...")
    print(f"Length of members list: {len(group.members)}")
    if len(group.members) > 1:
        for member in group.members:
            memberdict[member.user_id] = {"memberobject" : member, "namelist" : []}
    else:
        print("Member list is empty...")
        for message in messagelist:
            if message.user_id not in memberdict.keys():
                memberdict[message.user_id] = {"memberobject" : None, "namelist" : []}
        if findoutmem == "True":
            print(f"Using reference group: {refgroup}")
            refgroupobject = findGroup(refgroup)
            for key, value in memberdict.items():
                member = findMember(refgroupobject, key)
                if member:
                    value["memberobject"] = member

    print("Searching messagelist...")
    for message in messagelist:
        try:
            if message.name not in memberdict[message.user_id]["namelist"]:
                memberdict[message.user_id]["namelist"].append(message.name)
        except:
            pass

    print("Writing to file...")
    with open(f".\\FindNames\\FindNames_{group.name}.txt", "w") as writer:
        for value in memberdict.values():
            try:
                print(f"{value['memberobject'].name} has had {len(value['namelist'])} name aliases: {value['namelist']}\n")
                writer.write(f"{value['memberobject'].name} has had {len(value['namelist'])} name aliases: {value['namelist']}\n\n")
            except:
                pass

# Capture the spread and stagger surrounding messages of keyword messages in a group
def searchKeywordSprints(groupname, keyword, spread, stagger):
    group = findGroup(groupname)
    # How many surrounding messages should be written for each post
    spread = int(spread)
    # How far forward should the surrounding messages be staggered
    stagger = int(stagger)

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    # Fill with any messages that contain the provided keyword
    print("Searching for keyword...")
    keywordlist = []
    for message in messagelist:
        if keyword.lower() in str(message.text).lower():
            keywordlist.append(message)

    # Open writeable group file
    path = f".\\KeywordSprints\\{group.name}_KeywordSprints.txt"
    print(f"Writing to {path}...")
    with open(path, "w") as writer:
        writer.write(f"Searched for '{keyword}'...\n\n")
        # Iterate through messages that matched the keyword
        for message in keywordlist:
            # Assign the index of the current message in messagelist
            messageindex = messagelist.index(message)
            # Create the index to begin the current block of messages
            index = messageindex + spread - stagger
            # The index variable will decrease by one each iteration of the while loop
            # until it's equal to the low end of the spread
            while index >= messageindex - spread - stagger:
                try:
                    writer.write(f"{convertCreatedAt(messagelist[index])} - {messagelist[index].name} - {messagelist[index].text}\n")
                except Exception as e:
                    # print(f"Exception occurred: {e}")
                    pass
                index -= 1
            writer.write("\n\n")

# Searches given group(s) for keyword(s)/phrase(s) posted by member(s)
def searchForKeyword(groupname, membername, keyword):
    # Arguments are strings provided as "CSVs"
    groupnamelist = groupname.split(",")
    memberlist = membername.split(",")
    keywordlist = keyword.split(",")

    # Powershell doesn't allow empty strings anyway, but this is a backup
    if groupnamelist[0] == "" or memberlist[0] == "" or keywordlist[0] == "":
        print("Empty arguments are not permitted...")
        exit()

    # Search all groups except those in ./creds.py skipgrouplist
    if groupname == "any":
        grouplist = list(groups.autopage())
        # Evaluate skipgrouplist if it has values
        if len(skipgrouplist) > 0:
            for group in grouplist:
                if group.name in skipgrouplist:
                    print(f"Skipping {group.name} during execution...")
                    grouplist.remove(group)
        # Else evaluate all groups
        else:
            print("Searching all groups...")
    # Fill grouplist w/ CSV names from groupnamelist
    else:
        print("Filling grouplist...")
        grouplist = []
        for name in groupnamelist:
            grouplist.append(findGroup(name))

    # 1st layer of for loop
    # Declare fresh variables for each iteration
    for group in grouplist:
        print(f"\nWorking on {group.name}")
        memberexists = True
        memberdict = {}
        matchlist = []
        counter = 0
        errors = 0

        # Only fill memberdict with provided name(s) unless "any" was entered
        if membername == "any":
            print("Searching all members...")
            for member in group.members:
                memberdict[member.user_id] = {"memberobject" : member, "messages" : 0}
        else:
            for name in memberlist:
                member = findMember(group, name)
                # Only fill the dictionary if the member exists in the group
                if member:
                    memberdict[member.user_id] = {"memberobject" : member, "messages" : 0}
            # If length of the dictionary is 0, then no specified members exist in current group. Skip.
            if len(memberdict) == 0:
                print("No specified members in current group, skipping...")
                memberexists = False

        # Only search group if at least one member exists in it or if "any" was specified
        if memberexists:
            print("Filling messagelist...")
            messagelist = list(group.messages.list().autopage())

            print("Searching messages...")
            if membername == "any":
                # 2nd layer of for loop
                for message in messagelist:
                    match = False
                    try:
                        # This is the 3rd layer of for loops. Is there any way to make this more efficient?
                        for keyword in keywordlist:
                            if keyword.lower() in message.text.lower() and match == False:
                                matchlist.append(message)
                                memberdict[message.user_id]["messages"] += 1
                                counter += 1
                                match = True
                    except Exception as e:
                        # The error is typically NoneType for image posts
                        # print(f"Error: {e}")
                        errors += 1
                        pass
            else:
                for message in messagelist:
                    match = False
                    try:
                        for keyword in keywordlist:
                            if keyword.lower() in message.text.lower() and message.user_id in memberdict.keys() and match == False:
                                matchlist.append(message)
                                memberdict[message.user_id]["messages"] += 1
                                counter += 1
                                match = True
                    except Exception as e:
                        # The error is typically NoneType for image posts
                        # print(f"Error: {e}")
                        errors += 1
                        pass

            with open(f".\\KeywordSearch\\KeywordSearch_{group.name}.txt", "w") as writer:
                writer.write(f"Keyword/Phrase '{keyword}' appeared in this search {counter} time(s) or in {round(counter/len(messagelist)*100, 2)}% of messages with {errors} errors in {group.name}\n\n")

                # Print and write all occurences of the keyword/phrase to console (in chronological order)
                num = len(matchlist) - 1
                while num >= 0:
                    print(f"{convertCreatedAt(matchlist[num])} - {matchlist[num].name} - {matchlist[num].text}")
                    try:
                        writer.write(f"{convertCreatedAt(matchlist[num])} - {matchlist[num].name} - {matchlist[num].text}\n")
                    except:
                        pass
                    num -= 1
                print()

                # Sort memberdict by number of messages posted
                sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1]["messages"], reverse=True)

                # Print and write how many times each of the members in the dictionary posted a message w/ the keyword/phrase
                writer.write("\nKeyword Occurences:\n")
                print(f"{keywordlist} Occurences:")
                for index in sorted_memberdict:
                    print(f"{index[1]['memberobject'].name}: {index[1]['messages']}")
                    writer.write(f"{index[1]['memberobject'].name}: {index[1]['messages']}\n")

                # Print stats
                print(f"Keyword/Phrase '{keyword}' appeared in this search {counter} time(s) or in {round(counter/len(messagelist)*100, 2)}% of messages with {errors} errors in {group.name}\n")

# Find group and return group object
def findGroup(groupname):
    print("Looking for " + groupname)
    for group in grouplist:
        if group.name.lower() == groupname.lower():
            print("Found " + group.name)
            return group
    print("Couldn't find group: " + repr(groupname))
    return None

# Given a group object and member name string, return the member object
def findMember(group, membername):
    for member in group.members:
        if member.name == membername \
        or member.nickname == membername \
        or member.user_id == membername:
            print("Found " + member.name)
            return member
    print("Couldn't find " + repr(membername))
    return None

# Convert message object to string EST timezone
def convertCreatedAt(message):
    return f"{message.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S')} EST"

# Display attributes of the group, member, message, and user.get_me() objects
def getAttributes():
    # Take arbitrary first group in groups list
    group = grouplist[0]

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
