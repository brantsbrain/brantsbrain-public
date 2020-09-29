# Takes XML from SMS Backup and Restore
import xml.etree.ElementTree as ET
import sys
from datetime import date, datetime
from creds import bulklist, me

tree = ET.parse("sms-20200913004252.xml")
root = tree.getroot()

# Easier to manage class over a dictionary
class Contact:
    def __init__(self, name):
        self.name = name
        self.messages = []
        self.occurences = 0

# Convert and print date
def printDate():
    intdate = int("1452393970205")/1000
    print(str(intdate))
    newdate = datetime.fromtimestamp(intdate)
    print(newdate.strftime("%Y/%m/%d"))

# Find all messages from a certain date
def searchDate(contactname, passeddate):
    contact = ""
    contactdict = {}
    messagelist = []

    if contactname == "bulk":
        for index in bulklist:
            contactdict[index] = Contact(index)

        for child in root.iter("sms"):
            if child.get("contact_name") in contactdict.keys():
                messagedate = datetime.fromtimestamp(int(child.get("date"))/1000).strftime("%Y/%m/%d")
                if messagedate == passeddate:
                    if child.get("type") == "2":
                        contact = me
                    else:
                        contact = child.get("contact_name")
                    contactdict[child.get("contact_name")].messages.append(child.get("readable_date") + " - " + contact + " - " + child.get("body"))
                    contactdict[child.get("contact_name")].occurences += 1

        for x,y in contactdict.items():
            with open(".\\SearchDate\\searchDate_" + x + ".txt", "w") as writer:
                writer.write("\n---------- " + date.today().strftime("%m/%d/%Y") + " - " + str(y.occurences) + " Matching Messages ----------\n")
                for message in y.messages:
                    try:
                        writer.write(message + "\n")
                    except:
                        writer.write("ERROR OCCURRED")
                        pass
    else:
        for child in root.iter("sms"):
            if child.get("contact_name") == contactname:
                messagedate = datetime.fromtimestamp(int(child.get("date"))/1000).strftime("%Y/%m/%d")
                if messagedate == passeddate:
                    if child.get("type") == "2":
                        contact = me
                    else:
                        contact = child.get("contact_name")
                    messagelist.append(child.get("readable_date") + " - " + contact + " - " + child.get("body"))
        with open(".\\SearchDate\\searchDate_" + contactname + ".txt", "w") as writer:
            writer.write("\n---------- " + date.today().strftime("%m/%d/%Y") + " - " + str(y.occurences) + " Matching Messages ----------\n")
            for message in messagelist:
                try:
                    writer.write(message + "\n")
                except:
                    pass

# Search for all messages that meet a character length
def searchLength(contactname, length):
    contact = ""
    contactdict = {}
    messagelist = []

    if contactname == "bulk":
        for index in bulklist:
            contactdict[index] = Contact(index)

        for child in root.iter("sms"):
            if child.get("contact_name") in contactdict.keys():
                if len(child.get("body")) >= int(length):
                    if child.get("type") == "2":
                        contact = me
                    else:
                        contact = child.get("contact_name")
                    contactdict[child.get("contact_name")].messages.append(child.get("readable_date") + " - " + contact + " - " + child.get("body"))
                    contactdict[child.get("contact_name")].occurences += 1

        for x,y in contactdict.items():
            with open(".\\SearchLength\\searchLength_" + x + ".txt", "w") as writer:
                writer.write("\n---------- " + date.today().strftime("%m/%d/%Y") + " - " + str(y.occurences) + " Messages >= " + str(length) + " characters ----------\n")
                for message in y.messages:
                    try:
                        writer.write(message + "\n")
                    except:
                        pass
    else:
        for child in root.iter("sms"):
            if child.get("contact_name") == contactname:
                if child.get("body") >= length:
                    if child.get("type") == "2":
                        contact = me
                    else:
                        contact = child.get("contact_name")
                    messagelist.append(child.get("readable_date") + " - " + contact + " - " + child.get("body"))
        with open(".\\SearchLength\\searchLength_" + contactname + ".txt", "w") as writer:
            writer.write("\n---------- " + date.today().strftime("%m/%d/%Y") + " - " + str(y.occurences) + " Messages >= " + str(length) + " characters ----------\n")
            for message in messagelist:
                try:
                    writer.write(message + "\n")
                except:
                    pass


# Need to find oldest message
def oldestMess():
    olderdate = datetime.today().strftime("%Y/%m/%d")

    for child in root.iter("sms"):
        if datetime.fromtimestamp(int(child.get("date"))/1000).strftime("%Y/%m/%d") < olderdate:
            olderdate = datetime.fromtimestamp(int(child.get("date"))/1000).strftime("%Y/%m/%d")
            olderchild = child

    print("Oldest Message: " + olderchild.get("readable_date") + " - " + olderchild.get("contact_name") + " - " + olderchild.get("body"))

# Search for and write messages that match keyword for contact
def searchKey(contactname, keyword):
    contact = ""
    contactdict = {}
    messagelist = []

    if contactname == "bulk":
        for index in bulklist:
            contactdict[index] = Contact(index)

        for child in root.iter("sms"):
            if child.get("contact_name") in contactdict.keys():
                if keyword.lower() in child.get("body").lower():
                    if child.get("type") == "2":
                        contact = me
                    else:
                        contact = child.get("contact_name")
                    contactdict[child.get("contact_name")].messages.append(child.get("readable_date") + " - " + contact + " - " + child.get("body"))
                    contactdict[child.get("contact_name")].occurences += 1

        for x,y in contactdict.items():
            with open(".\\SearchKeys\\SearchKey_" + x + ".txt", "a") as writer:
                writer.write("\n---------- " + date.today().strftime("%m/%d/%Y") + " Search For '" + keyword + "' ----------\n")
                for message in y.messages:
                    try:
                        writer.write(message + "\n")
                    except:
                        y.occurences -= 1
                        pass
                writer.write("Keyword: " + keyword + " occurred " + str(y.occurences) + " times")
    else:
        for child in root.iter("sms"):
            if child.get("contact_name") == contactname:
                if keyword.lower() in child.get("body").lower():
                    if child.get("type") == "2":
                        contact = me
                    else:
                        contact = child.get("contact_name")
                    messagelist.append(child.get("readable_date") + " - " + contact + " - " + child.get("body"))
        with open(".\\SearchKeys\\searchKey_" + contactname + ".txt", "w") as writer:
            writer.write("\n---------- " + date.today().strftime("%m/%d/%Y") + " Search For '" + keyword + "' ----------\n")
            for message in messagelist:
                try:
                    writer.write(message + "\n")
                except:
                    pass

# Print list of total messages between all contacts
def totalMessages():
    contactlist = gatherContacts()
    messagedictionary = {}

    for contact in contactlist:
        messagedictionary[contact] = 0

    for child in root.iter("sms"):
        messagedictionary[child.get("contact_name")] += 1

    sorted_messagedictionary = sorted(messagedictionary.items(), key=lambda x: x[1], reverse=True)
    with open("TotalMessages.txt", "w") as writer:
        for x,y in sorted_messagedictionary:
            writer.write(x + " - " + str(y) + "\n")

# Gather contact names and return list
def gatherContacts():
    contactlist = []

    for child in root.iter("sms"):
        if child.get("contact_name") not in contactlist:
            contactlist.append(child.get("contact_name"))
    return contactlist

# Targeted write based on contact name
def targetWrite(contactname):
    totalmessages = 0

    with open(".\\AllMessages\\AllMessages_" + contactname + ".txt", "w") as writer:
        for child in root.iter("sms"):
            if contactname == child.get("contact_name"):
                totalmessages += 1
                if child.get("type") == "2":
                    contact = me
                else:
                    contact = contactname
                readable_date = child.get("readable_date")
                body = child.get("body")
                try:
                    writer.write(readable_date + " - " + contact + " - " + body + "\n")
                except:
                    try:
                        writer.write(readable_date + " - " + contact + " - ")
                        for character in body:
                            writer.write(character)
                    except:
                        writer.write("ERROR OCCURED\n")
                        pass

        print("Total Messages: " + str(totalmessages))

# Write plain date, contact, and body of every message
def plainWrite():
    with open("AllMessages.txt", "w") as writer:
        for child in root.iter("sms"):
            if child.get("type") == "2":
                contact = me
            else:
                contact = child.get("contact_name")
            readable_date = child.get("readable_date")
            body = child.get("body")
            try:
                writer.write(readable_date + " - " + contact + " - " + body + "\n")
            except:
                writer.write("ERROR OCCURED\n")
                pass

# Print plain date, contact, and body of every message
def plainPrint():
    for child in root.iter("sms"):
        if child.get("type") == "2":
            contact = me
        else:
            contact = child.get("contact_name")
        readable_date = child.get("readable_date")
        body = child.get("body")

        print(readable_date + " - " + contact + " - " + body)

# Create dictionary w/ key = contact and value = list of messages
def createDictionary():
    messagedictionary = {"" : []}

    for child in root.iter("sms"):
        if messagedictionary[child.get("contact_name")] in messagedictionary.keys():
            messagedictionary[child.get("contact_name")].append(child.get("readable_date") + child.get("contact_name") + child.get("body"))
        else:
            messagedictionary[child.get("contact_name")] = [child.get("readable_date") + child.get("contact_name") + child.get("body")]

# Prompts available at command line
if str(sys.argv[1]) == "prop":
    print(root.findall("sms")[0].items())
elif str(sys.argv[1]) == "plainw":
    plainWrite()
elif str(sys.argv[1]) == "plainp":
    plainPrint()
elif str(sys.argv[1]) == "targetWrite":
    targetWrite(sys.argv[2])
elif str(sys.argv[1]) == "create":
    createDictionary()
elif str(sys.argv[1]) == "totalMess":
    totalMessages()
elif str(sys.argv[1]) == "searchKey":
    # contactname, keyword
    searchKey(sys.argv[2], sys.argv[3])
elif str(sys.argv[1]) == "searchLength":
    searchLength(sys.argv[2], sys.argv[3])
elif str(sys.argv[1]) == "searchDate":
    searchDate(sys.argv[2], sys.argv[3])
elif str(sys.argv[1]) == "printDate":
    printDate()
elif str(sys.argv[1]) == "oldestMess":
    oldestMess()
