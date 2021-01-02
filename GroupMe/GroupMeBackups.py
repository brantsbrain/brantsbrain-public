# Import necessary methods from Finders
from GroupMeFinders import findGroup, findMember, convertCreatedAt

# Get modules/packages
import sys, csv
from creds import token, exceptionlist, bulklist
from groupy.client import Client
from datetime import datetime, timezone

# Instantiate variables to be used throughout
client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()
chats = client.chats.list_all()

# Detailed backup with message attributes
def detailedBackup(groupname):
    group = findGroup(groupname)

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    print("Writing lines...")
    with open(f".\\DetailedBackup\DetailedBackup_{group.name}.txt", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter='`', quotechar='"')
        writer.writerow(["created_at", "user_id", "name", "text", "favorited_by"])
        for message in messagelist:
            try:
                writer.writerow([message.created_at, message.user_id, message.name, message.text, message.favorited_by])
            except:
                pass

# Only update groups whose newest message is different than its latest backup's
def deltaMessages(easyread):
    for group in groups.autopage():
        print(f"Finding newest messages from {group.name} group and backup file...")
        lastmessage = group.messages.list()[0]

        if easyread == "True":
            path = f".\\EasyRead\\{group.name}_Messages.txt"
            lastmessagetext = f"{convertCreatedAt(lastmessage)} - {lastmessage.name} - {lastmessage.text}"
        else:
            path = f".\\BackupCSVs\\{group.name}_Messages.csv"
            lastmessagetext = f"{convertCreatedAt(lastmessage)}`{lastmessage.name}`{lastmessage.user_id}`{lastmessage.text}"

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
def backupAll(easyread):
    grouplist = list(groups.autopage())
    failedNames = []
    counter = 0
    groupnum = 1

    for group in grouplist:
        try:
            print(f"Group {groupnum}/{len(grouplist)}")
            writeAllMessages(group.name, easyread)
        except Exception as e:
            print(f"Error occurred in {group.name} : {e}")
            failedNames.append(group.name)
            counter += 1
            pass
        groupnum += 1
    print(f"Failed {counter} groups: {failedNames}")

# Write all messages in a given group to file either through a .csv or .txt based on easyread boolean
# Will need to create folder(s) manually before running function
def writeAllMessages(groupname, easyread):
    counter = 0
    group = findGroup(groupname)

    if easyread == "True":
        print("Writing to EasyRead")
        sep = " - "
        extension = ".txt"
        folder = "EasyRead"
    else:
        print("Writing to BackupCSVs")
        # Made sep an accent character because message.text will rarely have it, making it more reliable
        sep = "`"
        extension = ".csv"
        folder = "BackupCSVs"

    print("Filling messagelist...")
    messagelist = list(group.messages.list().autopage())

    path = f".\\{folder}\\{group.name}_Messages{extension}"
    print(f"Writing results to {path}...")
    with open(path, "w") as messagewriter:
        num = len(messagelist) - 1
        while num >= 0:
            message = messagelist[num]
            try:
                if easyread == "True":
                    messagewriter.write(convertCreatedAt(message) + sep + message.name + sep + message.text + "\n")
                else:
                    messagewriter.write(convertCreatedAt(message) + sep + message.name + sep + message.user_id + sep + message.text + "\n")
            except Exception as e:
                counter += 1
                pass
            num -= 1

    print(f"{counter} errors occurred in writing messages\n")

    return len(messagelist)

# Write all your group names to a file
def writeGroupNamesToFile():
    counter = 0
    failed = 0
    grouplist = []
    with open("GroupNames.txt", "w") as groupnamewriter:
        for group in groups.autopage():
            try:
                grouplist.append(group.name)
                groupnamewriter.write(group.name + "\n")
                counter += 1
            except:
                print("Couldn't write " + group.name)
                failed += 1
                pass
    print(f"Wrote {counter} out of {counter + failed} groups")
    return grouplist
