# Import necessary methods from Finders
from GroupMeFinders import findGroup, findMember, convertCreatedAt
# from GroupMePresenter import client, groups, grouplist

# Get modules/packages
import sys, csv, os, json
from creds import token, exceptionlist, bulklist
from datetime import datetime, timezone
import pandas as pd

# Instantiate variables to be used throughout
from groupy.client import Client
client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()
chats = client.chats.list_all()
grouplist = list(groups.autopage())

# Backup member names
def backupMems(groupname):
    group = findGroup(groupname)
    memberlist = []
    path = f"./Groups/{group.name}/"

    if not os.path.exists(path):
        os.makedirs(path)

    for member in group.members:
        memberlist.append(member.name)

    memberlist.sort()

    with open(f"{path}members.txt", "w") as writer:
        for index in memberlist:
            writer.write(f"{index}\n")

# Write group IDs w/ name
def backupIDs():
    idlist = []
    for group in grouplist:
        idlist.append([group.id, group.name])
    frame = pd.DataFrame(idlist, columns = ["ID", "Name"])
    frame.to_csv("group_ids.csv", index = False)

# Backup new groups
def backupNewGroups():
    if os.path.exists("group_ids.csv"):
        iddf = pd.read_csv("group_ids.csv")
    else:
        iddf = pd.DataFrame(columns=["ID","Name"])
    idlist = []

    for group in grouplist:
        stripped = group.name.strip()

        try:
            if not iddf["ID"].astype(str).str.contains(str(group.id)).any():
                print(f"Backing up {stripped}")
                writeAllMessages(stripped, "easy")
                writeAllMessages(stripped, "backup")
                writeAllMessages(stripped, "data")
                idlist.append([group.id, group.name])
        except Exception as e:
            print(f"Exception: {e}")

    for index in idlist:
        iddf = iddf.append({"ID" : index[0], "Name" : index[1]}, ignore_index=True)

    iddf.to_csv("group_ids.csv", index=False)

# Only update groups whose newest message is different than its latest backup's
def deltaMessages(easyread):
    for group in grouplist:
        print(f"Finding newest messages from {group.name} group and backup file...")
        lastmessage = group.messages.list()[0]

        if easyread == "easy":
            path = f".\\EasyRead\\{group.name}_Messages.txt"
            lastmessagetext = f"{convertCreatedAt(lastmessage)} - {lastmessage.name} - {lastmessage.text}"
        elif easyread == "backup":
            path = f".\\BackupCSVs\\{group.name}_Messages.csv"
            lastmessagetext = f"{convertCreatedAt(lastmessage)}`{lastmessage.name}`{lastmessage.user_id}`{lastmessage.text}"
        else:
            path = f".\\DataBackups\\{group.name}_Messages.txt"
            # lastmessagetext =

        print("Finding last line of backup file...")
        oldlen = 0
        with open(path, "r") as reader:
            for line in reader:
                oldlen += 1
            lastline = line

        print("Comparing last lines...")
        if lastline != lastmessagetext:
            print("Newest messages are different. Updating...")
            newlen = writeAllMessages(group.name, easyread)
            print(f"Added {newlen - oldlen} lines")
        else:
            print("Last lines match. No updates needed...")

# Write DMs to file
def writeChats():
    counter = 0
    with open("DirectMessages.txt", "w") as writer:
        print("Writing to ./DirectMessages.txt...")
        for chat in chats:
            chatlist = list(chat.messages.list().autopage())
            num = len(chatlist) - 1
            writer.write(f"---------- {chat.other_user['name']} - {num + 1} ----------\n")
            while num >= 0:
                message = chatlist[num]
                try:
                    writer.write(f"{convertCreatedAt(message)} - {message.name} - {message.text}\n")
                except:
                    try:
                        writer.write(f"{convertCreatedAt(message)} - {message.name} - ")
                        for character in message.text:
                            writer.write(character)
                        writer.write("\n")
                    except:
                        writer.write("\n")
                        pass
                num -= 1
            writer.write("\n")

# Write all group message data from all groups to files
def backupAll(format):
    failedNames = []
    counter = 0
    groupnum = 1

    for group in grouplist:
        try:
            print(f"Group {groupnum}/{len(grouplist)}")
            writeAllMessages(group.name, format)
        except Exception as e:
            print(f"Error occurred in {group.name} : {e}")
            failedNames.append(group.name)
            counter += 1
            pass
        groupnum += 1
    print(f"Failed {counter} groups: {failedNames}")

# Write all messages in a given group to file either through a .csv or .txt based on easyread boolean
# Will need to create folder(s) manually before running function
def writeAllMessages(groupname, format):
    counter = 0
    group = findGroup(groupname)

    dfpath = f"./Groups/{group.name}"

    if format == "easy":
        print("Writing to EasyRead")
        sep = " - "
        extension = ".txt"
        folder = "EasyRead"
    elif format == "backup":
        print("Writing to BackupCSVs")
        # Made sep an accent character because message.text will rarely have it, making it more reliable
        sep = "`"
        extension = ".csv"
        folder = "BackupCSVs"
        messdf = pd.DataFrame()
        timelist = []
        namelist = []
        textlist = []
    else:
        print("Writing as data file...")
        extension = ".txt"
        folder = "DataBackups"

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    path = f".\\{folder}\\{group.name}_Messages{extension}"
    print(f"Writing results to {path}...")
    with open(path, "w") as messagewriter:
        num = len(messagelist) - 1
        # if format == "backup":
            # messagewriter.write("Time`Name`Text\n")
        while num >= 0:
            message = messagelist[num]
            try:
                if format == "easy":
                    messagewriter.write(convertCreatedAt(message) + sep + message.name + sep + message.text + "\n")
                elif format == "backup":
                    textlist.append(message.text)
                    namelist.append(message.name)
                    timelist.append(convertCreatedAt(message))
                    # messagewriter.write(datetime.strptime(convertCreatedAt(message), "%Y-%m-%d %H:%M:%S ") + sep + message.name + sep + message.user_id + sep + message.text + "\n")
                else:
                    messagewriter.write(str(message.data) + "\n")
            except Exception as e:
                counter += 1
                pass
            num -= 1
        if format == "backup":
            messdf["Time"] = timelist
            pd.to_datetime(messdf["Time"])
            messdf["Name"] = namelist
            messdf["Text"] = textlist
            messdf.to_csv(f"{dfpath}/{group.name}_backup.csv", index=False)

    print(f"{counter} errors occurred in writing messages\n")

    return len(messagelist)

# Write all your group names to a file
def writeGroupNamesToFile():
    counter = 0
    failed = 0
    with open("GroupNames.txt", "w") as groupnamewriter:
        for group in grouplist:
            try:
                groupnamewriter.write(group.name + "\n")
                counter += 1
            except:
                print("Couldn't write " + group.name)
                failed += 1
                pass
    print(f"Wrote {counter} out of {counter + failed} groups")
    return grouplist
