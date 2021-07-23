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

# Write image URLs and user_ids to file for download
def imageURLs(groupname):
    group = findGroup(groupname)
    messagelist = list(group.messages.list().autopage())

    with open(f".\\Images\\Images_{group.name}.csv", "w") as writer:
        for message in messagelist:
            try:
                if len(message.attachments) > 0:
                    if (message.attachments[0].type) == "image":
                        writer.write(f"{message.attachments[0].url},{message.user_id}\n")
            except Exception as e:
                print(f"Exception {e}\n{message.data}")

# Download galleries from all GMs
def downAllGalleries():
    for group in grouplist:
        if not group.name == "The Graveyard":
            try:
                print(f"Downloading images for {group.name}...")
                downImages(group.name)
            except Exception as e:
                print(f"Exception occurred within {group.name}: {e}")

# Pull gallery from all GMs
def pullAllGalleries():
    for group in grouplist:
        if not group.name == "The Graveyard":
            try:
                print(f"Checking for {group.name} images folder...")
                if not os.path.exists(f".\\Images\\Images_{group.name}"):
                    print(f"Creating {group.name} images folder...")
                    os.mkdir(f".\\Images\\Images_{group.name}")
                else:
                    print(f"{group.name} images folder already exists...")

                print(f"Checking for {group.name} images URL CSV...")

                if not os.path.exists(f".\\Images\\Images_{group.name}.csv"):
                    print(f"Creating {group.name} images URL CSV...")
                    pullGallery(group.name)
                else:
                    print(f"{group.name} images URL CSV already exists...")
            except Exception as e:
                print(f"Exception occurred on {group.name}: {e}")
                pass

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
        with open(f".\\Images\\Images_{group.name}\\Image_{group.name}_{str(filenum)}_{membername}{ext}", "wb") as handle:
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
                writer.write(""
                            f"{findMember(group, item[0]).name} posted\n\t"
                            f"{item[1]} images"
                            f"\n\t{round(item[1]/total*100, 2)}%\n"
                            "")
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
                textlist = message.text.split(" ")
                longeststring = textlist[0]
                for index in textlist:
                    if len(index) > len(longeststring):
                        longeststring = index
                urllist.append(longeststring)
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

def downVids(groupname):
    group = findGroup(groupname)
    with open(f".\\URLs\\URLs_{group.name}.txt", "r") as reader:
        lines = reader.readlines()

    numvid = 1
    for line in lines:
        try:
            urllib.request.urlretrieve(line.strip(), f".\\Videos\\{group.name}\\{numvid}.mp4")
            numvid += 1
        except Exception as e:
            print(f"Exception occurred: {e}")
