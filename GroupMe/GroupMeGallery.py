# Import necessary methods from Finders
from GroupMeFinders import findGroup, findMember, convertCreatedAt

# Get modules/packages
import sys, requests, json, os
import urllib.request
from creds import token, exceptionlist, bulklist
from groupy.client import Client
from groupy import attachments
from datetime import datetime, timezone

# Instantiate variables to be used throughout
client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()
chats = client.chats.list_all()
grouplist = list(groups.autopage())

def convertCreatedAtPic(message):
    return f"{message.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y%m%d')}"

# Download Pictures
def downPicsByMem(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    urlmemdict = {}

    if not os.path.exists(f"./Groups/{group.name}/Pictures"):
        os.makedirs(f"./Groups/{group.name}/Pictures")

    for member in group.members:
        urlmemdict[member.user_id] = {"name" : member.name, "urllist" : []}

    for message in messagelist:
        try:
            if len(message.attachments) > 0:
                if (message.attachments[0].type) == "image":
                    urlmemdict[message.user_id]["urllist"].append(message.attachments[0].url)
        except Exception as e:
            print(f"Exception {e}\n{message.data}")

    for val in urlmemdict.values():
        num = 1
        for index in val["urllist"]:
            if "png" in index:
                ext = ".png"
            elif "gif" in index:
                ext = ".gif"
            elif "jpeg" in index:
                ext = ".jpeg"
            else:
                ext = ".txt"

            with open(f"./Groups/{group.name}/Pictures/{val['name']}_{num}{ext}", "wb") as handle:
                try:
                    response = requests.get(index, stream=True)
                    if not response.ok:
                        print(response)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
                except Exception as e:
                    print(f"Error on {val['name']}_{num}{ext}: {e}")
                    pass
            num += 1

# Download pictures by date
def downPics(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())
    urllist = []

    if not os.path.exists(f"./Groups/{group.name}/Pictures"):
        os.makedirs(f"./Groups/{group.name}/Pictures")

    for message in messagelist:
        try:
            if len(message.attachments) > 0:
                if (message.attachments[0].type) == "image":
                    # Append individual lists of URL, timestamp, and name
                    urllist.append([message.attachments[0].url, convertCreatedAtPic(message), message.name])
        except Exception as e:
            print(f"Exception {e}\n{message.data}")

    # Flip list to write chronologically
    urllist.reverse()

    # Write to folder
    num = 1
    for index in urllist:
        if "png" in index[0]:
            ext = ".png"
        elif "gif" in index[0]:
            ext = ".gif"
        elif "jpeg" in index[0]:
            ext = ".jpeg"
        else:
            ext = ".txt"

        try:
            with open(f"./Groups/{group.name}/Pictures/{num}_{index[2]}_{index[1]}{ext}", "wb") as handle:
                try:
                    response = requests.get(index[0], stream=True)
                    if not response.ok:
                        print(response)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
                except Exception as e:
                    print(f"Error on {index[2]}_{num}{ext}: {e}")
                    pass
        except Exception as e:
            print(e)
            pass
        num += 1

# Download Videos
def fullDownVids(groupname):
    group = findGroup(groupname)
    urlmemdict = {}

    if not os.path.exists(f"./Groups/{group.name}/Videos"):
        os.makedirs(f"./Groups/{group.name}/Videos")

    for member in group.members:
        urlmemdict[member.user_id] = {"name" : member.name, "urllist" : []}

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    print("Searching messages...")
    for message in messagelist:
        try:
            if "v.groupme.com" in message.text:
                textlist = message.text.split(" ")
                longeststring = textlist[0]
                for index in textlist:
                    if len(index) > len(longeststring):
                        longeststring = index
                urlmemdict[message.user_id]["urllist"].append(longeststring)
        except:
            pass

    for val in urlmemdict.values():
        num = 1
        for index in val["urllist"]:
            try:
                urllib.request.urlretrieve(index.strip(), f"./Groups/{group.name}/Videos/{val['name']}_{num}.mp4")
                num += 1
            except:
                pass

# Download profile pics
def downProfilePics(groupname):
    group = findGroup(groupname)
    memberdict = {}

    if not os.path.exists(f"./Groups/{group.name}/ProfilePics"):
        os.mkdir(f"./Groups/{group.name}/ProfilePics")

    for member in group.members:
        try:
            if "png" in member.image_url:
                ext = ".png"
            elif "jpeg" in member.image_url:
                ext = ".jpeg"
            else:
                ext = ".old"
        except:
            print(f"Unable to capture URL: {member.data}")
            ext = ".old"
        memberdict[member.user_id] = {"name" : member.name, "url" : member.image_url, "ext" : ext}

    # Code inside with statement used from Stack Overflow answer on downloading images using requests
    for val in memberdict.values():
        with open(f"./Groups/{group.name}/ProfilePics/{val['name']}{val['ext']}", "wb") as handle:
            try:
                response = requests.get(val['url'], stream=True)
                if not response.ok:
                    print(response)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
            except Exception as e:
                print("Error: " + str(e))
                pass

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
                writer.write(""
                            f"{findMember(group, item[0]).name} posted\n\t"
                            f"{item[1]} images"
                            f"\n\t{round(item[1]/total*100, 2)}%\n"
                            "")
            except Exception as e:
                print(str(e))
                pass