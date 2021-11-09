# Import necessary methods from Finders
from GroupMeFinders import findGroup, findMember, convertCreatedAt

# Get modules/packages
import sys, os
from creds import token, exceptionlist, bulklist
from groupy.client import Client
from datetime import datetime, timezone
import pandas as pd

# Instantiate variables to be used throughout
client = Client.from_token(token)
groups = client.groups.list()
myuser = client.user.get_me()
chats = client.chats.list_all()
grouplist = list(groups.autopage())

# Find the longest time gap between messages
def longestGap(groupname):
    group = findGroup(groupname)
    lines = []

    messageframe = pd.import_csv(f".\\Offline\\{group.name}\\messages.csv")
    # with open(f".\\Offline\\{group.name}\\messages.csv", "r") as reader:
    #     lines = reader.readlines()

    # for row in messageframe:
    #     if messageframe["created_at"][row]


# Backup group to standalone folder w/ separate files for object attributes
def pullGroup(groupname):
    group = findGroup(groupname)
    folderpath = f".\\Offline\\{group.name}"
    messagelist = list(group.messages.list().autopage())
    memberdata = []
    messagedata = []

    # Create offline folder if needed
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)

    # Write members.csv
    for member in group.members:
        memberdata.append([member.user_id, member.name])

    memberframe = pd.DataFrame(memberdata, columns = ["user_id", "name"])
    memberframe.to_csv(f"{folderpath}\\members.csv")

    # Write messages.csv
    for message in messagelist:
        messagedata.append([message.created_at, message.name, message.text, message.favorited_by])

    messageframe = pd.DataFrame(messagedata, columns = ["created_at", "name", "text", "favorited_by"])
    messageframe.to_csv(f"{folderpath}\\messages.csv")

# Print details of CSVs written to offline folders
def printPandas(groupname):
    group = findGroup(groupname)
    folderpath = f".\\Offline\\{group.name}"
    memberframe = pd.read_csv(f"{folderpath}\\members.csv", index_col=0)
    messageframe = pd.read_csv(f"{folderpath}\\messages.csv", index_col=0)

    print(memberframe)
    print(messageframe)
