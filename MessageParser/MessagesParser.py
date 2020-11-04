##############################################################################
# Takes XML from SMS Backup and Restore on Google Play (and App Store?)
#
# Create a creds.py file in the current directory
# Add a bulklist list with strings of favorite/interesting contacts
# Add a me string with your name
# Add a path string with the absolute path to the backed up .xml
#
# readable_date, contact_name, type, and body are all elements in the .xml
# type == 2 is a message from you
# type == 1 is a message from them
##############################################################################

import xml.etree.ElementTree as ET
import sys, re, string
from datetime import date, datetime
from creds import bulklist, me, path

tree = ET.parse(path)

if path == None or path == "":
    # Need a GUI select file line
    print("No filepath")
    exit()

root = tree.getroot()

# Easier to manage class over a dictionary
class Contact:
    def __init__(self, name):
        self.name = name
        self.messages = []
        self.occurences = 0
        self.mostcharsfromthem = 0
        self.childfromthem = None
        self.mostcharsfromme = 0
        self.childfromme = None

# List messages that have all uppercase words in them
def allUpper(contactname, type):
    childlist = []
    ignoreupperlist = ["I", "U", "A"]
    if type == "all":
        for child in root.iter("sms"):
            if contactname == child.get("contact_name"):
                allupper = True
                body = child.get("body").translate(str.maketrans("", "", string.punctuation))
                wordlist = body.split(" ")
                pattern = re.compile("^[A-Z]+$")
                punctuation = re.compile("\!\.")
                for word in wordlist:
                    word = word.translate(str.maketrans("", "", string.punctuation))
                    if not pattern.match(word) or word in ignoreupperlist:
                        allupper = False
                if allupper:
                    childlist.append(child)

    with open(".\\AllUpper\\AllUpper_" + contactname + ".txt", "w") as writer:
        for child in childlist:
            if child.get("type") == "2":
                contact = "Brant Goings"
            else:
                contact = contactname

            try:
                writer.write(child.get("readable_date") + " - " + contact + " - " + child.get("body") + "\n")
            except Exception as e:
                print("Exception occurred: " + str(e))
                pass

# Find longest message out of all messages
def longestMess():
    charlength = 0

    for child in root.iter("sms"):
        if len(child.get("body")) >= charlength and child.get("type") != "2":
            charlength = len(child.get("body"))
            readable_date = child.get("readable_date")
            name = child.get("contact_name")
            longestmess = child.get("body")

    print("Longest Message: " + str(charlength) + " characters")
    print(readable_date + " - " + name + " - " + longestmess)

# Longest message to and from per contact
def longestPerCon(contactname):
    namedict = {}
    if contactname == "bulk":
        for name in bulklist:
            namedict[name] = Contact(name)
        for child in root.iter("sms"):
            if child.get("contact_name") in namedict.keys():
                if len(child.get("body")) >= namedict[child.get("contact_name")].mostcharsfromthem and child.get("type") == "1":
                    namedict[child.get("contact_name")].mostcharsfromthem = len(child.get("body"))
                    namedict[child.get("contact_name")].childfromthem = child
                elif len(child.get("body")) >= namedict[child.get("contact_name")].mostcharsfromme and child.get("type") == "2":
                    namedict[child.get("contact_name")].mostcharsfromme = len(child.get("body"))
                    namedict[child.get("contact_name")].childfromme = child
        for x,y in namedict.items():
            with open(".\\LongestMessages\\LongestMessage_" + x + ".txt", "w") as writer:
                try:
                    writer.write("Longest message from " + x + ":\n" + y.childfromthem.get("readable_date") + " - " + y.childfromthem.get("body") + "\n\nCharacters: " + str(y.mostcharsfromthem) + "\n\n")
                except Exception as e:
                    position = 0
                    writer.write("Longest message from " + x + ":\n" + y.childfromthem.get("readable_date") + " - ")
                    while position <= len(y.childfromthem.get("body")):
                        try:
                            writer.write(y.childfromthem.get("body")[position])
                            position += 1
                        except:
                            position += 1
                    writer.write("\n\nCharacters: " + str(y.mostcharsfromthem) + "\n\n")

                try:
                    writer.write("Longest message to " + x + ":\n" + y.childfromme.get("readable_date") + " - " + y.childfromme.get("body") + "\n\nCharacters: " + str(y.mostcharsfromme) + "\n\n")
                except:
                    position = 0
                    writer.write("Longest message to " + x + ":\n" + y.childfromme.get("readable_date") + " - ")
                    while position <= len(y.childfromme.get("body")):
                        try:
                            writer.write(y.childfromme.get("body")[position])
                            position += 1
                        except:
                            position += 1
                    writer.write("\n\nCharacters: " + str(y.mostcharsfromme) + "\n")

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
                writer.write("\n---------- " + passeddate + " - " + str(y.occurences) + " Matching Messages ----------\n")
                for message in y.messages:
                    try:
                        writer.write(message + "\n")
                    except:
                        try:
                            writer.write(child.get("readable_date") + " - " + contact + " - ")
                            for character in child.get("body"):
                                writer.write(character)
                        except:
                            writer.write(" --- ERROR OCCURED\n")
                            pass
    else:
        occurences = 0
        for child in root.iter("sms"):
            if child.get("contact_name") == contactname:
                messagedate = datetime.fromtimestamp(int(child.get("date"))/1000).strftime("%Y/%m/%d")
                if messagedate == passeddate:
                    occurences += 1
                    if child.get("type") == "2":
                        contact = me
                    else:
                        contact = child.get("contact_name")
                    messagelist.append(child.get("readable_date") + " - " + contact + " - " + child.get("body"))

        with open(".\\SearchDate\\searchDate_" + contactname + ".txt", "w") as writer:
            writer.write("\n---------- " + passeddate + " - " + str(occurences) + " Matching Messages ----------\n")
            for message in messagelist:
                try:
                    writer.write(message + "\n")
                except:
                    try:
                        writer.write(child.get("readable_date") + " - " + contact + " - ")
                        for character in child.get("body"):
                            writer.write(character)
                    except:
                        writer.write(" --- ERROR OCCURED\n")
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
                        writer.write(message + "\n\n")
                    except:
                        try:
                            writer.write(child.get("readable_date") + " - " + contact + " - ")
                            for character in child.get("body"):
                                writer.write(character)
                        except:
                            writer.write(" --- ERROR OCCURED\n")
                            pass
    else:
        occurences = 0
        for child in root.iter("sms"):
            if child.get("contact_name") == contactname:
                if len(child.get("body")) >= int(length):
                    occurences += 1
                    if child.get("type") == "2":
                        contact = me
                    else:
                        contact = child.get("contact_name")
                    messagelist.append(child.get("readable_date") + " - " + contact + " - " + child.get("body"))

        with open(".\\SearchLength\\searchLength_" + contactname + ".txt", "w") as writer:
            writer.write("\n---------- " + date.today().strftime("%m/%d/%Y") + " - " + str(occurences) + " Messages >= " + str(length) + " characters ----------\n")
            for message in messagelist:
                try:
                    writer.write(message + "\n\n")
                except:
                    try:
                        writer.write(child.get("readable_date") + " - " + contact + " - ")
                        for character in child.get("body"):
                            writer.write(character)
                    except:
                        writer.write(" --- ERROR OCCURED\n")
                        pass

# Find oldest message
def oldestMess():
    olderdate = datetime.today().strftime("%Y/%m/%d")

    for child in root.iter("sms"):
        if datetime.fromtimestamp(int(child.get("date"))/1000).strftime("%Y/%m/%d") < olderdate:
            olderdate = datetime.fromtimestamp(int(child.get("date"))/1000).strftime("%Y/%m/%d")
            olderchild = child

    print("Oldest Message: " + olderchild.get("readable_date") + " - " + olderchild.get("contact_name") + " - " + olderchild.get("body"))

# Find newest message
def newestMess():
    newerdate = "2000/01/01"

    for child in root.iter("sms"):
        if datetime.fromtimestamp(int(child.get("date"))/1000).strftime("%Y/%m/%d") > newerdate:
            newerdate = datetime.fromtimestamp(int(child.get("date"))/1000).strftime("%Y/%m/%d")
            newerchild = child

    print("Newest Message: " + newerchild.get("readable_date") + " - " + newerchild.get("contact_name") + " - " + newerchild.get("body"))

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
                        try:
                            writer.write(child.get("readable_date") + " - " + contact + " - ")
                            for character in child.get("body"):
                                writer.write(character)
                        except:
                            writer.write(" --- ERROR OCCURED\n")
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
                    try:
                        writer.write(readable_date + " - " + contact + " - ")
                        for character in child.get("body"):
                            writer.write(character)
                    except:
                        writer.write(" --- ERROR OCCURED\n")
                        pass

# Write list of total messages between all contacts
def totalMessages():
    contactlist = gatherContacts()
    messagedictionary = {}

    for contact in contactlist:
        messagedictionary[contact] = 0

    for child in root.iter("sms"):
        messagedictionary[child.get("contact_name")] += 1

    sorted_messagedictionary = sorted(messagedictionary.items(), key=lambda x: x[1], reverse=True)
    with open("TotalMessages.txt", "w") as writer:
        writer.write("Total Conversations: " + str(len(messagedictionary)) + "\n")
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
                        writer.write("\n")
                    except:
                        writer.write(" --- ERROR OCCURED\n")
                        pass
        writer.write("\nTotal Messages: " + str(totalmessages))

# Write all messages for all contacts
def writeAll():
    contactlist = gatherContacts()
    failedlist = []
    for contact in contactlist:
        try:
            print("Writing", contact, "...")
            targetWrite(contact)
        except:
            failedlist.append(contact)
            pass
    print("Error writing:", failedlist)

# PROMPTS AVAILABLE AT COMMAND LINE
# Print properties/elements available for analysis
if str(sys.argv[1]) == "prop":
    print(root.findall("sms")[0].items())
# Write bulklist or a specific contact name to file
elif str(sys.argv[1]) == "targetWrite":
    # bulk/contactname
    targetWrite(sys.argv[2])
# Write total number of messages
elif str(sys.argv[1]) == "totalMess":
    totalMessages()
# Search for a keyword in bulklist or contact
elif str(sys.argv[1]) == "searchKey":
    # bulk/contactname, keyword
    searchKey(sys.argv[2], sys.argv[3])
# Write all messages that meet a provided character length
elif str(sys.argv[1]) == "searchLength":
    # bulk/contactname, string value for length
    searchLength(sys.argv[2], sys.argv[3])
# Search for messages sent/received on a specific date
elif str(sys.argv[1]) == "searchDate":
    # bulk/contactname, date in YYYY/MM/DD string format
    searchDate(sys.argv[2], sys.argv[3])
# Print oldest message
elif str(sys.argv[1]) == "oldestMess":
    oldestMess()
# Print newest message
elif str(sys.argv[1]) == "newestMess":
    newestMess()
# Write all messages to files
elif str(sys.argv[1]) == "writeAll":
    writeAll()
# Find longest message
elif str(sys.argv[1]) == "longestMess":
    longestMess()
# Write longest messages to/from per contact
elif str(sys.argv[1]) == "longestPerCon":
    # bulk/(no contact as of now)
    longestPerCon(sys.argv[2])
elif str(sys.argv[1]) == "allUpper":
    allUpper(sys.argv[2], sys.argv[3])
