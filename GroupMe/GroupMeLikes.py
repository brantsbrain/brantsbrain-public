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

# Like a number of or all messages in a group
def liker(groupname, reqlikes):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())

    if reqlikes == "all":
        reqlikes = len(messagelist)
    else:
        reqlikes = int(reqlikes)

    for num in range(reqlikes):
        messagelist[num].like()

# Find number of consecutive messages liked by each member
def likeStreak(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    memberdict = {}

    for member in group.members:
        memberdict[member.user_id] = {"name" : member.name, "totallikes" : 0, "currstreak" : 0, "beststreak" : 0}

    for message in messagelist:
        for key, val in memberdict.items():
            if key in message.favorited_by:
                val["currstreak"] += 1
                val["totallikes"] += 1
            # While this is technically innacurate, it may be more "applicable"
            # because users usually don't like their own messages
            elif message.user_id == key:
                pass
            else:
                if val["currstreak"] > val["beststreak"]:
                    val["beststreak"] = val["currstreak"]
                val["currstreak"] = 0

    print("Like Stats:")
    for val in memberdict.values():
        if val["beststreak"] > 0:
            print(f"{val['name']}\n\tBest Streak - {val['beststreak']}\n\tTotal Likes - {val['totallikes']}\n")

# How many likes has each member given another member
def likeStats(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    memberdict = {}
    memberlist = list(group.members)

    for outer in memberlist:
        memberdict[outer.user_id] = {}
        for inner in memberlist:
            memberdict[outer.user_id][inner.user_id] = 0

    for message in messagelist:
        if len(message.favorited_by) > 0:
            for index in message.favorited_by:
                try:
                    memberdict[message.user_id][index] += 1
                except:
                    # print(message.data)
                    pass

    with open("./ExtendedLikeStats.txt", "w") as writer:
        for key, val in memberdict.items():
            writer.write(f"{findMember(group, key).name}\n")
            for ikey, ival in val.items():
                if ival > 0:
                    writer.write(f"\tLiked {findMember(group, ikey).name} - {ival}\n")
            writer.write("\n\n")

# Find message(s) from text and return number of likes it got
def messLikes(groupname, text):
    group = findGroup(groupname)

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    print("Searching for text...")
    while text != "0":
        textlist = []
        for message in messagelist:
            try:
                if text.lower() in message.text.lower():
                    textlist.append(message)
            except:
                pass
        if len(textlist) > 0:
            for message in textlist:
                print(f"{convertCreatedAt(message)} - {message.name} - {message.text} - {len(message.favorited_by)} likes")
        else:
            print("No message found with that text")
        text = input("Enter new text or 0 to exit: ")

# Quickly like/unlike messages then reverse changes to hide them
def stealthLikeOthers(groupname, choice):
    group = findGroup(groupname)
    likeddict = {}
    # Defines whether we are going to only like or only unlike in the beginning. Those changes will be reversed in the second half
    if choice.lower() == "like":
        like = True
    else:
        like = False

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    print("Liking/Unliking messages...")
    for message in messagelist:
        # Store message in likeddict only if we liked it already...
        if myuser.id in message.favorited_by:
            likeddict[message.created_at] = message
            # Try to unlike the message if like is False since we know that we originally liked it
            if like == False:
                try:
                    message.unlike()
                except Exception as e:
                    print(f"Encountered error in the unlike: {e}")
        # If we didn't like it already but like is True, try to like it
        elif like:
            try:
                message.like()
            except Exception as e:
                print(f"Encountered error in the like: {e}")

    print("Undoing changes now...")
    for message in messagelist:
        if myuser.id in message.favorited_by:
            # If we had originally liked the message and and like is False, it means we unliked it. Try to like it again
            if message.created_at in likeddict.keys() and like == False:
                try:
                    message.like()
                except Exception as e:
                    print(f"Encountered error in the reverse like: {e}")
        # If we didn't originally like the message, but like is true, it means we liked it. Now we need to unlike it
        elif like:
            try:
                message.unlike()
            except Exception as e:
                print(f"Encountered error in the reverse unlike: {e}")

# Write a list of the most liked messages
def mostLikedMessages(groupname, nummessages):
    group = findGroup(groupname)
    nummessages = int(nummessages)
    mostlikeddict = {}

    print("Filling messagelist...")
    messagelist = group.messages.list().autopage()
    for message in messagelist:
        mostlikeddict[message.text] = {"numfavorites" : len(message.favorited_by), "sendername" : message.name, "timestamp" : convertCreatedAt(message)}

    print("Sorting by number of likes...")
    sorted_mostlikeddict = sorted(mostlikeddict.items(), key=lambda x: x[1]["numfavorites"], reverse=True)

    path = f".\\MostLikes\\MostLikes_{group.name}.txt"
    print(f"Writing top {nummessages} messages to {path}...")
    with open(path, "w") as writer:
        for num in range(nummessages):
            likes = sorted_mostlikeddict[num][1]["numfavorites"]
            time = sorted_mostlikeddict[num][1]["timestamp"]
            name = sorted_mostlikeddict[num][1]["sendername"]
            text = sorted_mostlikeddict[num][0]

            try:
                writer.write(f"{likes} likes: {time} - {name} - {text}\n\n" )
            except:
                writer.write(f"{likes} likes: {time} - {name} - ")
                if text != None:
                    for character in text:
                        try:
                            writer.write(character)
                        except:
                            pass
                writer.write("\n\n")

# Write a sorted list of the people that got 1+ likes
def numLikes(groupname):
    group = findGroup(groupname)

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    print("Creating memberdict...")
    memberdict = {}
    for member in group.members:
        memberdict[member.user_id] = {"name" : member.name, "likedmessages" : 0, "messages" : 0}

    print("Counting likes...")
    for message in messagelist:
        try:
            memberdict[message.user_id]["messages"] += 1
            if len(message.favorited_by) > 0:
                memberdict[message.user_id]["likedmessages"] += 1
        except:
            pass

    print("Sorting memberdict...")
    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1]["likedmessages"], reverse=True)

    likedict = {}
    for entry in sorted_memberdict:
        try:
            likedict[entry[1]["name"]] = round(entry[1]["likedmessages"]/entry[1]["messages"]*100,2)
        except:
            print(f"{entry[1]['name']} had a division issue")
            pass

    print("Sorting likedict...")
    sorted_likedict = sorted(likedict.items(), key=lambda x: x[1], reverse=True)

    print("Writing results...")
    with open(".\MoreLikes.txt", "a") as writer:
        writer.write("\nPosts that got 1+ likes\n")
        for entry in sorted_likedict:
            writer.write(f"{entry[0]}: {entry[1]}% of {memberdict[findMember(group, entry[0]).user_id]['messages']} posts\n")

# Find the percentage of likes per member given to messages that are not each individual member's
def numLikesGiven(groupname):
    group = findGroup(groupname)
    totalposts = 0

    print("Filling memberdict...")
    memberdict = {}
    for member in group.members:
        memberdict[member.user_id] = {"name" : member.name, "likesgiven" : 0, "posts" : 0}

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    print("Filling likes...")
    for message in messagelist:
        # Add one to the total posts
        totalposts += 1
        try:
            # Add one to the relevant member's total posts
            memberdict[message.user_id]["posts"] += 1
        except KeyError:
            pass
        except Exception as e:
            print(f"Error occurred {e}")

        for messagelike in message.favorited_by:
            try:
                # Add a like to each member in the favorited_by list
                memberdict[messagelike]["likesgiven"] += 1
            except KeyError:
                pass
            except Exception as e:
                print(f"Error occurred {e}")

    # Sort by number of likes given
    print("Sorting memberdict...")
    sorted_memberdict = sorted(memberdict.items(), key=lambda x: x[1]["likesgiven"], reverse=True)

    print("Writing results...")
    with open(f"./PercentageLikes.txt", "a") as writer:
        writer.write(f"\n\nPercentage of likes given of messages not posted by member in {group.name}...\n")
        for entry in sorted_memberdict:
            name = entry[1]["name"]
            likedmessages = entry[1]["likesgiven"]
            posts = entry[1]["posts"]
            otherposts = totalposts - posts
            writer.write(f"{name} liked {round(likedmessages/otherposts*100,2)}% of {otherposts} messages\n")


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

    path = f".\\LikeSpread\\LikeSpread_{group.name}.txt"
    print(f"Writing results to {path}...")
    with open(path, "w") as writer:
        writer.write(f"Writing {posts} total posts w/ a spread of {spread} and staggered by {stagger}\n\n")
        for likes in range(posts):
            try:
                writer.write(f"Message: {sorted_likeddict[likes][0]} - Likes: {sorted_likeddict[likes][1]}\n")
            except:
                writer.write("Message: ")
                for character in str(sorted_likeddict[likes][0]):
                    try:
                        writer.write(character)
                    except:
                        pass
                writer.write(f" - Likes: {sorted_likeddict[likes][1]}\n")
        writer.write("\n\n")

        # indexdict values are the position of the message in messagelist
        for entry in indexdict.values():
            # Create an index equal to the last message to be written for each entry
            index = entry + spread - stagger
            while index >= entry - spread - stagger:
                try:
                    writer.write(f"{convertCreatedAt(messagelist[index])} - {messagelist[index].name} - {messagelist[index].text}\n")
                except:
                    writer.write(f"{convertCreatedAt(messagelist[index])} - {messagelist[index].name} - ")
                    for character in str(messagelist[index].text):
                        try:
                            writer.write(character)
                        except:
                            pass
                    writer.write("\n")

                index -= 1
            writer.write("\n\n")
