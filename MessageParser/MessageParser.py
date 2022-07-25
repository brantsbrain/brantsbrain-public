##############################################################################
# Takes XML from SMS Backup and Restore on Google Play (and App Store?)
#
# Create a creds.py file in the current directory
# Add a bulklist list with strings of favorite/interesting contacts
# Add a me string with your name
# Add a mynum string with your +12223334444 number
# Add a path string with the absolute path to the backed up .xml
# Assign contactdict pandas dataframe from CSV export of SanitizeContacts.py
#
# readable_date, contact_name, type, and body are all elements in the .xml
# type == 2 is a message from you
# type == 1 is a message from them
##############################################################################

"""
TODO:
- How many conversations did I start?
"""

import sys, re, string, base64
import xml.etree.ElementTree as ET
from datetime import date, datetime
from creds import bulklist, me, mynum, path, contactframe

# Create dictionary w/ data from contactframe
contactdict = {}
for num in range(len(contactframe)):
    contactdict[contactframe.iloc[num]["Number"]] = {"name" : contactframe.iloc[num]["Name"]}
contactdict[mynum]["name"] = me

if path == None or path == "":
    # Need a GUI select file line
    print("No filepath")
    exit()

tree = ET.parse(path)
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

# Print number of image types
def printMMSImageTypes():
    imagedict = {}

    for mms in root.iter("mms"):
        for parts in mms.iter("parts"):
            for part in parts.iter("part"):
                if part.get("seq") == "0":
                    if part.get("ct") not in imagedict.keys():
                        imagedict[part.get("ct")] = 1
                    else:
                        imagedict[part.get("ct")] += 1

    for key, val in imagedict.items():
        print(f"{key} - {val}")

# Print MMS that match contact names and length
def printGroupMMSLength(contactname, length):
    namelist = contactname.split(",")
    minlen = int(length)
    currentgroup = ""
    numerrors = 0

    with open(f".\\GroupMMS\\GroupMMSLength_{contactname}.txt", "w") as writer:
        writer.write(f"Writing messages that meet a minimum length of {minlen} characters\n\n")
        for mms in root.iter("mms"):
            printtext = True
            for name in namelist:
                if name not in mms.get("contact_name"):
                    printtext = False

            if printtext:
                if currentgroup != mms.get("contact_name"):
                    wrotegroupname = False
                    currentgroup = mms.get("contact_name")

                found = False
                for addrs in mms.iter("addrs"):
                    for addr in addrs.iter("addr"):
                        if found:
                            pass
                        else:
                            sendernum = addr.get("address")
                            if not sendernum.startswith("1") and len(sendernum) == 10:
                                sendernum = "1" + sendernum
                            if not sendernum.startswith("+"):
                                sendernum = "+" + sendernum

                            try:
                                sendername = contactdict[sendernum]["name"]
                            except Exception as e:
                                print(f"Exception occurred: {e}")
                                numerrors += 1
                            found = True

                for parts in mms.iter("parts"):
                    for part in parts.iter("part"):
                        if part.get("seq") == "0":
                            if len(part.get("text")) >= minlen:
                                if not wrotegroupname:
                                    writer.write(f"\nCurrent Group: {mms.get('contact_name')}\n")
                                    wrotegroupname = True
                                try:
                                    writer.write(f"{mms.get('readable_date')} - {sendername} - {part.get('text')}\n\n")
                                except:
                                    pass
        print(f"Number of errors: {numerrors}")

# Print MMS that contain contact names
def printGroupMMS(contactname):
    namelist = contactname.split(",")
    currentgroup = ""

    with open(f".\\GroupMMS\\GroupMMS_{contactname}.txt", "w") as writer:
        for mms in root.iter("mms"):
            printtext = True
            for name in namelist:
                if name not in mms.get("contact_name"):
                    printtext = False

            if printtext:
                if currentgroup != mms.get("contact_name"):
                    writer.write(f"\nCurrent Group: {mms.get('contact_name')}\n")
                    currentgroup = mms.get("contact_name")

                found = False
                for addrs in mms.iter("addrs"):
                    for addr in addrs.iter("addr"):
                        if found:
                            pass
                        else:
                            sendernum = addr.get("address")
                            if not sendernum.startswith("1") and len(sendernum) == 10:
                                sendernum = "1" + sendernum
                            if not sendernum.startswith("+"):
                                sendernum = "+" + sendernum

                            try:
                                sendername = contactdict[sendernum]["name"]
                            except:
                                pass
                            found = True

                for parts in mms.iter("parts"):
                    for part in parts.iter("part"):
                        if part.get("seq") == "0":
                            try:
                                writer.write(f"{mms.get('readable_date')} - {sendername} - {part.get('text')}\n")
                            except:
                                pass

# Convert Base64 data from MMS messages and save to folder
def convBase64():
    count = 0
    # Add dictionary for tracking group message contacts
    for mms in root.iter("mms"):
        found = False
        for addrs in mms.iter("addrs"):
            for addr in addrs.iter("addr"):
                if found:
                    pass
                else:
                    sendernum = addr.get("address")
                    if not sendernum.startswith("1") and len(sendernum) == 10:
                        sendernum = "1" + sendernum
                    if not sendernum.startswith("+"):
                        sendernum = "+" + sendernum

                    try:
                        sendername = contactdict[sendernum]["name"]
                    except:
                        pass
                    found = True

        for parts in mms.iter("parts"):
            for part in parts.iter("part"):
                if part.get("seq") == "0" and part.get("data"):
                    b64 = part.get("data")
                    bytes = b64.encode("utf-8")

                    if "jpg" in part.get("ct"):
                        ext = ".jpg"
                    elif "jpeg" in part.get("ct"):
                        ext = ".jpeg"
                    elif "png" in part.get("ct"):
                        ext = ".png"
                    elif "gif" in part.get("ct"):
                        ext = ".gif"
                    else:
                        ext = ".txt"

                    with open(f".\\Images\\{sendername}_{count}{ext}", "wb") as writer:
                        try:
                            messbytes = base64.decodebytes(bytes)
                            writer.write(messbytes)
                            count += 1
                        except:
                            pass

# Write MMS messages
def writeMMS():
    with open(".\\MMS\\MMS_Messages.txt", "w") as writer:
        for mms in root.iter("mms"):
            for part in mms.iter("parts"):
                for part in part.iter("part"):
                    if part.get("seq") == "0":
                        try:
                            writer.write(f"{mms.get('readable_date')} - {mms.get('contact_name')} - {part.get('text')}\n")
                        except:
                            pass

# Count the number of MMS groups shared w/ individual contacts
def indivMMSShares():
    contactdict = {}

    for mms in root.iter("mms"):
        namelist = mms.get("contact_name").split(", ")

        for name in namelist:
            if name in contactdict.keys():
                contactdict[name] += 1
            else:
                contactdict[name] = 1

    sorted_contactdict = sorted(contactdict.items(), key=lambda x: x[1], reverse=True)

    print("Shared groups w/ contacts")
    for key, val in sorted_contactdict:
        print(f"{key} - {val}")

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

    if contactname == "all":
        keywordlist = []
        for child in root.iter("sms"):
            if keyword.lower() in child.get("body").lower():
                if child.get("type") == "2":
                    contact = me
                else:
                    contact = child.get("contact_name")
                keywordlist.append(f"{child.get('readable_date')} - {contact} - {child.get('body')}")
        with open(".\\SearchKeys\\SearchKey_All.txt", "w") as writer:
            writer.write("\n---------- " + date.today().strftime("%m/%d/%Y") + " Search For '" + keyword + "' ----------\n")
            for index in keywordlist:
                writer.write(index + "\n")

    elif contactname == "bulk":
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
if sys.argv[1] == "prop":
    print(root.findall("sms")[0].items())
# Write bulklist or a specific contact name to file
elif sys.argv[1] == "targetWrite":
    # bulk/contactname
    targetWrite(sys.argv[2])
# Write total number of messages
elif str(sys.argv[1]) == "totalMessages":
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
elif sys.argv[1] == "writeMMS":
    writeMMS()
elif sys.argv[1] == "indivMMSShares":
    indivMMSShares()
elif sys.argv[1] == "convBase64":
    convBase64()
elif sys.argv[1] == "printGroupMMS":
    printGroupMMS(sys.argv[2])
elif sys.argv[1] == "printGroupMMSLength":
    printGroupMMSLength(sys.argv[2], sys.argv[3])
elif sys.argv[1] == "printMMSImageTypes":
    printMMSImageTypes()
else:
    print("Command doesn't exist")
