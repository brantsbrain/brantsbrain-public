# Import necessary methods from Finders
from GroupMeFinders import findGroup, findMember, convertCreatedAt
# from GroupMePresenter import client, groups, grouplist

# Get modules/packages
import sys, os
from datetime import datetime, timezone
from creds import token, exceptionlist, bulklist

# Instantiate variables to be used throughout
from groupy.client import Client
client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()
chats = client.chats.list_all()
grouplist = list(groups.autopage())

# Print owners of groups
def groupOwners():
    ownerdict = {}
    for group in grouplist:
        ownerid = group.data["creator_user_id"]
        for member in group.members:
            if ownerid == member.user_id:
                if ownerid not in ownerdict.keys():
                    ownerdict[ownerid] = {"name" : member.name, "owns" : 1, "ownsnames" : [group.name], "admin" : 0, "adminsnames" : []}
                else:
                    ownerdict[ownerid]["owns"] += 1
                    ownerdict[ownerid]["ownsnames"].append(group.name)
            elif "admin" in member.roles:
                if member.user_id not in ownerdict.keys():
                    ownerdict[member.user_id] = {"name" : member.name, "owns" : 0, "ownsnames" : [], "admin" : 1, "adminsnames" : [group.name]}
                else:
                    ownerdict[member.user_id]["admin"] += 1
                    ownerdict[member.user_id]["adminsnames"].append(group.name)

    for val in ownerdict.values():
        print(f"{val['name']} -\n\tOwns {val['owns']}: {val['ownsnames']}\n\n\tAdmins {val['admin']}: {val['adminsnames']}\n\n")

# How many users have interacted in the past x month(s)?
def lastInteraction(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())

    memberdict = {}
    for member in group.members:
        memberdict[member.user_id] = {"name" : member.name, "lastinteraction" : None}

    # Iterate chronologically
    index = len(messagelist) - 1
    while index >= 0:
        message = messagelist[index]
        try:
            memberdict[message.user_id]["lastinteraction"] = message.created_at
            if len(message.favorited_by) > 0:
                for member in message.favorited_by:
                    memberdict[member]["lastinteraction"] = message.created_at
        except:
            pass
        index -= 1

    # Need to clean None values out of memberdict to avoid error in sorting
    nopostsdict = {}
    for key, val in memberdict.items():
        if not val["lastinteraction"]:
            nopostsdict[key] = val
    for key in nopostsdict.keys():
        if key in memberdict.keys():
            del memberdict[key]

    sortedmemberdict = dict(sorted(memberdict.items(), key=lambda item: item[1]["lastinteraction"]))

    path = f"./Groups/{group.name}"
    with open(f"{path}/lastinteraction.txt", "w") as writer:
        writer.write("Member - Last Interaction\n")
        for value in sortedmemberdict.values():
            if value["lastinteraction"]:
                try:
                    writer.write(f"{value['name']} - {value['lastinteraction']}\n")
                except:
                    pass
            else:
                value["lastinteraction"] = "No Interactions"
                writer.write(f"{value['name']} - {value['lastinteraction']}\n")
        for value in nopostsdict.values():
            try:
                writer.write(f"{value['name']} - {value['lastinteraction']}\n")
            except:
                pass

# Find average/quickest response times per member
def responseTime(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    maxtime = 10
    floor = 0

    memberdict = {}
    for member in group.members:
        memberdict[member.user_id] = {"name" : member.name, "quickest" : maxtime, "instances" : 0, "aver" : 0, "prev": None, "curr" : None}

    index = 0
    while index < len(messagelist) - 1:
        prev = messagelist[index + 1]
        curr = messagelist[index]
        delta = (curr.created_at - prev.created_at).total_seconds()

        if floor < delta < maxtime and prev.user_id != curr.user_id:
            try:
                memberdict[curr.user_id]["instances"] += 1
                if floor < delta < memberdict[curr.user_id]["quickest"]:
                    memberdict[curr.user_id]["quickest"] = delta
                    memberdict[curr.user_id]["prev"] = prev
                    memberdict[curr.user_id]["curr"] = curr
            except:
                pass
        index += 1

    with open(f"./Groups/{group.name}/responsetime.txt", "w") as writer:
        for val in memberdict.values():
            try:
                writer.write(f"{val['name']} had {val['instances']} instances w/ quickest response: {val['quickest']}\nPrev: {val['prev']}\nCurr: {val['curr']}\n\n")
            except:
                pass

# When did members join group?
def dateJoined(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    joineddict = {}

    for message in messagelist:
        try:
            if message.data["event"]["type"] == "membership.announce.added":
                for member in message.data["event"]["data"]["added_users"]:
                    joineddict[member["nickname"]] = convertCreatedAt(message)

            elif message.data["event"]["type"] == "membership.announce.joined":
                joineddict[message.data['event']['data']['user']['nickname']] = convertCreatedAt(message)
        except:
            pass

    sortedjoineddict = dict(sorted(joineddict.items(), key=lambda item: item[1]))

    for key, val in sortedjoineddict.items():
        print(f"{val} - {key}")

# Who has attended the most events?
def eventsAttended(groupname, sincedate):
    import pytz
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    if sincedate:
        sincedate = datetime.strptime(sincedate, '%m/%d/%Y')
        sincedate = pytz.UTC.localize(sincedate)
    else:
        sincedate = datetime.strptime("01/01/1999")

    memberdict = {}
    eventlist = []
    for member in group.members:
        memberdict[member.nickname] = {"name" : member.name, "attended" : 0, "idlist" : []}

    for message in messagelist:
        if message.created_at > sincedate:
            try:
                # Don't count duplicate "going" responses
                if message.data["event"]["type"] == "calendar.event.user.going" and message.data["event"]["data"]["event"]["id"] not in memberdict[message.data["event"]["data"]["user"]["nickname"]]["idlist"]:
                    memberdict[message.data["event"]["data"]["user"]["nickname"]]["attended"] += 1
                    memberdict[message.data["event"]["data"]["user"]["nickname"]]["idlist"].append(message.data["event"]["data"]["event"]["id"])
            except:
                pass

            try:
                if message.data["event"]["type"] == "calendar.event.user.going" and message.data["event"]["data"]["event"]["name"] not in eventlist:
                    eventlist.append(message.data["event"]["data"]["event"]["name"])
            except:
                pass

    # {k: v for k, v in sorted(memberdict.items(), key=lambda item: item[1]["attended"])}
    sortedmemberdict = dict(sorted(memberdict.items(), key=lambda item: item[1]["attended"], reverse=True))

    print(f"Events attended since {sincedate}")
    for key, val in sortedmemberdict.items():
        if val['attended'] > 0:
            print(f"{val['name']} attended {val['attended']}")
    print(eventlist)

# How many users left in the past x amount of time
# NOT WORKING
def usersLeft(groupname, date):
    import pytz
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    sincedate = datetime.strptime(date, '%m/%d/%Y')
    sincedate = pytz.UTC.localize(sincedate)
    usersleft = 0

    for message in messagelist:
        if message.created_at > sincedate:
            try:
                if message.data["event"]["type"] == "membership.notifications.exited":
                    usersleft += 1
            except:
                pass

    print(f"{usersleft} users left since {sincedate.strftime('%m/%d/%Y')}")

# Find highest number of consecutive posts per member
def consecPosts(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    memberdict = {}
    previd = ""

    for member in group.members:
        memberdict[member.user_id] = {"name" : member.name, "curr" : 0, "high" : 0, "currlist" : [], "highlist" : []}

    for message in messagelist:
        currid = message.user_id
        if previd == currid:
            try:
                memberdict[currid]["curr"] += 1
                try:
                    memberdict[currid]["currlist"].append(message.text)
                except:
                    memberdict[currid]["currlist"].append("Message")

                if memberdict[currid]["curr"] > memberdict[currid]["high"]:
                    memberdict[currid]["high"] = memberdict[currid]["curr"]
                    memberdict[currid]["highlist"] = memberdict[currid]["currlist"]
            except KeyError as e:
                print(f"Encountered Key Error: {e}")
        else:
            try:
                memberdict[currid]["curr"] = 1
                memberdict[currid]["currlist"] = []
                try:
                    memberdict[currid]["currlist"].append(message.text)
                except:
                    memberdict[currid]["currlist"].append("Message")
            except KeyError as e:
                print(f"Encountered Key Error: {e}")
            previd = currid

    for val in memberdict.values():
        if val['high'] > 1:
            print(f"{val['name']} : {val['high']}")
            print(f"{val['highlist']}\n\n")

# How many shared groups based on members within a given group
def scopedSharedGroups(sourcegroupname):
    sourcegroup = findGroup(sourcegroupname)
    memberdict = {}

    for member in sourcegroup.members:
        memberdict[member.user_id] = {"name" : member.name, "shared" : 0}

    for group in grouplist:
        for member in group.members:
            if member.user_id in memberdict.keys():
                memberdict[member.user_id]["shared"] += 1

    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1]["shared"], reverse=True)
    print(f"Shared groups with source group: {sourcegroup.name}")
    for index in sorted_memberdict:
        if index[1]['shared'] > 1 and index[1]['name'] != myuser['name']:
            print(f"{index[1]['name']} - {index[1]['shared']}")

# Number of members that have chat muted
def mutedChat(groupname):
    group = findGroup(groupname)
    muted = 0

    for member in group.members:
        if member.muted:
            muted += 1

    print(f"{muted} members have {group.name} muted")

# Time since last post/member
def lastPost(groupname):
    group = findGroup(groupname)
    memberdict = {}
    allmemdict = {}
    nopostlist = []
    messagelist = list(group.messages.list().autopage())

    for member in group.members:
        allmemdict[member.user_id] = member.name

    for message in messagelist:
        if message.user_id not in memberdict.keys():
            memberdict[message.user_id] = {"name" : message.name, "date" : message.created_at}

    print("Most recent message per member:")
    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1]["name"], reverse=True)
    for index in sorted_memberdict:
        print(f"{index[1]['name']} - {index[1]['date'].strftime('%m-%d-%Y')}")

    for key, val in allmemdict.items():
        if key not in memberdict.keys():
            nopostlist.append(val)

    print(f"\n{len(nopostlist)} members that haven't posted in {group.name}:\n{nopostlist}")

# Print total groups
def totalGroups():
    totalgroups = 0

    for group in grouplist:
        try:
            totalgroups += 1
        except:
            print("Error occurred...")
    print(f"{totalgroups} groups")

# How many groups two people share with each other that I'm also a member of?
def peersShareGroups(name1, name2):
    member1 = None
    member2 = None
    member1name = None
    member2name = None
    sharedgroups = 0

    for group in grouplist:
        member1 = findMember(group, name1)
        member2 = findMember(group, name2)
        if member1 and member2:
            member1name = member1.name
            member2name = member2.name
            sharedgroups += 1
    print(f"{member1name} and {member2name} share {sharedgroups} groups (where you're a member also)")

# Print as many stats for a particular member(s) as possible
def memberStats(groupname, membername):
    group = findGroup(groupname)
    member = findMember(group, membername)
    messagelist = list(group.messages.list().autopage())
    messagesposted = 0
    likes = 0
    counter = 0
    receivedlikes = 0
    totallikes = 0
    found = False

    for message in messagelist:
        counter += 1
        totallikes += len(message.favorited_by)
        # Figure out when member joined/was added
        if message.system and not found:
            # Check to see if the users were added
            if message.event["type"] == "membership.announce.added":
                # Iterate the added_users list
                for index in range(len(message.event['data']['added_users'])):
                    if str(message.event['data']['added_users'][index]['id']) == str(member.user_id):
                        print(f"Added by {message.event['data']['adder_user']['nickname']} on {convertCreatedAt(message)}")
                        found = True
            # Check to see if the user joined
            elif message.event["type"] == "membership.announce.joined":
                if str(message.event['data']['user']['id']) == str(member.user_id):
                    print(f"Joined {group.name} on {convertCreatedAt(message)}")
                    found = True
        # Count messages posted
        if message.user_id == member.user_id:
            messagesposted += 1
        # Count likes
        if member.user_id in message.favorited_by:
            likes += 1
        # Count number of likes received
        if message.user_id == member.user_id:
            receivedlikes += len(message.favorited_by)

    # Print results
    print(f"Posted {messagesposted} out of {counter} ({round(messagesposted/counter*100,2)}%) messages")
    print(f"Liked {likes} out of {counter} ({round(likes/counter*100,2)}%) messages")
    print(f"Received {receivedlikes} out of {totallikes} ({round(receivedlikes/totallikes*100,2)}%) likes")

# Print list of dates all current members were added
def dateUserAdded(groupname):
    # Attributes of a message reading "x added y to the group"
    # {'attachments': [], 'avatar_url': None, 'created_at': datenum, 'favorited_by': ['numid', 'numid'], 'group_id': 'numid', 'id': 'numid', 'name': 'GroupMe', 'sender_id': 'system', 'sender_type': 'system', 'source_guid': 'redacted', 'system': True, 'text': 'x added y to the group.', 'user_id': 'system', 'event': {'type': 'membership.announce.added', 'data': {'added_users': [{'id': numid, 'nickname': 'y'}], 'adder_user': {'id': numid, 'nickname': 'x'}}}, 'platform': 'gm'}
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    currmemlist = []

    # Add current member ids to list
    for member in group.members:
        currmemlist.append(str(member.user_id))
    print(f"Total Members - {len(currmemlist)}")

    # Print list chronologically
    num = len(messagelist) - 1
    while num >= 0:
        message = messagelist[num]
        # Check to see if it's a system message
        if message.system:
            # Check to see if the users were added
            if message.event["type"] == "membership.announce.added":
                # Iterate the added_users list
                for index in range(len(message.event['data']['added_users'])):
                    # Only print if the user is still in the group
                    if str(message.event['data']['added_users'][index]['id']) in currmemlist:
                        print(f"{convertCreatedAt(message)} - {message.event['data']['added_users'][index]['nickname']}")
            # Check to see if the user joined
            elif message.event["type"] == "membership.announce.joined":
                # Only print if user is still in the group
                if str(message.event['data']['user']['id']) in currmemlist:
                    print(f"{convertCreatedAt(message)} - {message.event['data']['user']['nickname']}")
        num -= 1

# Find number of messages sent in a given month
def messInMonth(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    memberdict = {}
    monthlist = [10]

    for member in group.members:
        memberdict[member.user_id] = {"name" : member.name, "mess": 0}

    for message in messagelist:
        # print(message.created_at.month)
        if message.created_at.month in monthlist and message.created_at.year == datetime.today().year:
            try:
                memberdict[message.user_id]["mess"] += 1
            except:
                pass

    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1]["mess"], reverse=True)

    for index in sorted_memberdict:
        # if index[1]["mess"] > 0:
        print(f'{index[1]["name"]} - {index[1]["mess"]}')

# Find the average number of messages sent per month since the member joined
def averMessPerMonth(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    memberdict = {}
    counter = 0

    path = f"./Groups/{group.name}"

    # Instantiate the memberdict member objects with counters at 0
    for member in group.members:
        memberdict[member.user_id] = {"name": member.name, "messcount" : 0, "firstmessdate" : "", "aver" : 1, "diffmonths" : 1}

    # For each message, increase message.user_id value by 1 and total counter by 1.
    for message in messagelist:
        try:
            memberdict[message.user_id]["messcount"] += 1
            memberdict[message.user_id]["firstmessdate"] = message.created_at
            counter += 1
        except:
            pass

    # Format results
    for val in memberdict.values():
        if not val["messcount"] == 0:
            diffmonths = (datetime.today().year - val["firstmessdate"].year) * 12 + (datetime.today().month - val["firstmessdate"].month)
            if diffmonths == 0:
                diffmonths = 1
            val["aver"] = round(val["messcount"] / diffmonths)
            val["diffmonths"] = diffmonths

    # Sort and write results
    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1]["aver"], reverse=True)
    with open(f"{path}/AverPostsPerMonth.txt", "w") as writer:
        writer.write(f"--- Average Posts per Month for {group.name} out of {len(group.members)} members and {counter} posts as of {datetime.now().strftime('%m/%d/%Y')} ---\n")
        for i in sorted_memberdict:
            try:
                writer.write(f"{i[1]['name']}\n\tMessages Sent - {i[1]['messcount']}\n\tMembership in Months - {i[1]['diffmonths']}\n\tAverage Messages per Month - {i[1]['aver']}\n")
            except Exception as e:
                print(f"Exception occurred: {e}")

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
    for group in grouplist:
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
    groupdict = {}

    for group in grouplist:
        groupdict[group.name] = group.data["messages"]["count"]

    sorted_groupdict = sorted(groupdict.items(), key=lambda x: x[1], reverse=True)
    with open("TotalPosts.csv", "w") as writer:
        writer.write("Group Name, Number of Messages\n")
        for i in sorted_groupdict:
            try:
                writer.write(f"{i[0]}, {i[1]}\n")
            except:
                pass
        writer.write(f"\nTotal Groups: {len(grouplist)}")

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
    try:
        for message in messagelist:
            memberdict[message.user_id] += 1
            counter += 1
    except:
        pass

    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1], reverse=True)
    for i in sorted_memberdict:
        try:
            membername = findMember(group, i[0]).name
            details = details + membername + " - " + str(round(i[1]/counter*100, 2)) + "%\n"
        except:
            pass
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

    path = f"./Groups/{group.name}"
    print(f"Writing results to {path}/commonwords.txt...")
    with open(path + "/commonwords.txt", "w") as writer:
        writer.write(f"--- Words greater than {num} letters ---")
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

    path = f"./Groups/{group.name}"
    if not os.path.exists(path):
        os.makedirs(path)

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    print("Creating memberdict...")
    for member in group.members:
        memberdict[member.user_id] = {"numchars" : 0, "messages" : 0}

    print("Filling memberdict...")
    for message in messagelist:
        if message.user_id in memberdict.keys():
            totalposts += 1
            memberdict[message.user_id]["messages"] += 1
            try:
                for character in message.text:
                    try:
                        memberdict[message.user_id]["numchars"] += 1
                    except:
                        # failedmessages += 1
                        pass
            except:
                pass

    # Sort by number of posts per member
    print("Sorting memberdict...")
    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1]["messages"], reverse=True)

    print(f"Writing data to {path}/avermesslength.txt...")
    with open(path + "/avermesslength.txt", "w") as writer:
        x = 1
        writer.write(f"--- Character Averages for {group.name.encode('utf-8')} Sorted by Total Messages as of {datetime.now().strftime('%m/%d/%Y')}---\n")
        for member in sorted_memberdict:
            try:
                writer.write(""
                            f"{x}. {findMember(group,member[0]).name}\n\t"
                            f"Average character count per message - {round(member[1]['numchars']/member[1]['messages'])}\n\t"
                            f"Total messages sent - {member[1]['messages']}\n\t"
                            f"Percentage of group's posts - {round(member[1]['messages']/totalposts*100, 2)}%\n"
                            "")
            # Common exception is going to be divide by zero
            except Exception as e:
                print(f"Exception occurred with {findMember(group,member[0]).name}: {e}")
                pass
            x += 1
        writer.write("\n")

    print("Total messages - " + str(totalposts))
    print("Failed messages - " + str(failedmessages))
