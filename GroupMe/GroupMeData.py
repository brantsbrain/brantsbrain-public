# Import all methods
from GroupMeLikes import *
from GroupMeGallery import *
from GroupMeAnalysis import *
from GroupMeBackups import *
from GroupMeFinders import *
# from GroupMeOffline import *

# Get modules/packages
import sys

# Interpret CLI input
if sys.argv[1] == "help":
    print("Available options:\n")

    print("GroupMeAnalysis:\n\t"
            "boardMessages - Find total messages posted by users in ./creds.py bulklist variable across all shared groups\n\t"
            "Takes nothing\n\n\t"

            "longestMess - Finds the longest message(s) sent in a group\n\t"
            "Takes group name\n\n\t"

            "sharedGroups - Write number of shared groups per member to file\n\t"
            "Takes nothing\n\n\t"

            "totalPostsPerGroup - Writes ordered list of total number of posts per group to file\n\t"
            "Takes nothing\n\n\t"

            "allMemberPercentPosts - Writes percentage of total posts per user to file\n\t"
            "Takes group name\n\n\t"

            "commonWords - Writes most common words in group to file. Ignores entries in ./creds.py exceptionlist\n\t"
            "Takes group name, length of word (string)\n\n\t"

            "averMessLength - Write average length of message, total messages, and percentage of group's posts per member to file\n\t"
            "Takes group name\n\n\t"

            "averMessPerMonth"
            "")

    print("GroupMeBackups:\n\t"
            "deltaMessages - Backup changed messages across all groups\n\t"
            "Takes easyread True/False"

            "writeChats - Write DMs to file\n\t"
            "Takes nothing\n\n\t"

            "backupAll - Write all group messages from all groups to files\n\t"
            "Takes easyread True/False\n\n\t"

            "writeGroupNamesToFile - Write all group names to file\n\t"
            "Takes nothing\n\n\t"

            "writeAllMessages - Writes all messages from a given group to file\n\t"
            "Takes group name, True/False (True = EasyRead, False = CSV formatted)\n\n\t"

            "detailedBackup - Write all messages along with message attributes\n\t"
            "Takes group name\n\n\t"
            "")

    print("GroupMeLikes:\n\t"
            "messLikes - Find message(s) from text and return number of likes received\n\t"
            "Takes group name, text\n\n\t"

            "stealthLikeOthers - Quickly like/unlike messages then undo changes\n\t"
            "Takes group name, like/unlike\n\n\t"

            "mostLikedMessages - Write a list of the most liked messages to file\n\t"
            "Takes group name, number of messages to write\n\n\t"

            "numLikes - Write list of people that got 1+ likes to file\n\t"
            "Takes group name\n\n\t"

            "numLikesGiven - Write percentage of likes per member given to messages not from that member to file\n\t"
            "Takes group name\n\n\t"

            "mostLikedSprints - Write number of messages with surrounding spread and stagger that got the most likes\n\t"
            "Takes group name, number of top liked messages, number of surrounding messages, and stagger\n\n\t"
            "")

    print("GroupMeGallery:\n\t"
            "pullGallery - Write GroupMe gallery URLs to CSV\n\t"
            "Takes group name\n\n\t"

            "downImages - Downloads images from stored CSV\n\t"
            "Takes group name\n\n\t"

            "percentImagePost - Writes percentage of total images posted per member to file\n\t"
            "Takes group name\n\n\t"

            "pullURL - Writes GroupMe URLs to file\n\t"
            "Takes group name\n\n\t"

            "downVids - Read URLs from video txt and download to folder\n\t"
            "Takes group name\n\n\t"

            "pullAllGalleries - Pull all galleries\n\t"
            "Takes nothing\n\n\t"
            "")

    print("GroupMeFinders:\n\t"
            "searchForKeyword - Search group for keyword/phrase\n\t"
            "Takes group name (any/csv groups/group), member name (any/csv members/member), keyword/phrase (csv)\n\n\t"

            "searchKeywordSprints - Search group for keyword/phrase and capture surrounding spread and stagger\n\t"
            "Takes group name, keyword/phrase, spread (string), stagger (string)\n\n\t"

            "printMyInfo - Print current user attributes\n\t"
            "Takes nothing\n\n\t"

            "findGroup - Search for group name\n\t"
            "Takes group name\n\n\t"

            "getAttributes - Print attributes of group and message objects\n\t"
            "Takes nothing\n\n\t"
            "")

elif sys.argv[1] == "writeAllMessages":
    print("Running writeAllMessages()")
    # group name, easyread string value True/False
    writeAllMessages(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "backupAll":
    print("Running backupAll()")
    # easyread string value True/False
    backupAll(sys.argv[2])

elif sys.argv[1] == "findGroup":
    print("Running findGroup()")
    # group name
    findGroup(sys.argv[2])

elif sys.argv[1] == "writeGroupNamesToFile":
    print("Running writeGroupNamesToFile()")
    # None
    writeGroupNamesToFile()

elif sys.argv[1] == "averMessLength":
    print("Running averMessLength()")
    # group name
    averMessLength(sys.argv[2])

elif sys.argv[1] == "numLikes":
    print("Running numlikes()")
    # group name
    numLikes(sys.argv[2])

elif sys.argv[1] == "mostLikedMessages":
    print("Running mostLikedMessages()")
    # group name, number of messages
    mostLikedMessages(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "commonWords":
    print("Running commonWords()")
    # group name, length of word
    commonWords(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "allMemberPercentPosts":
    print("Running allMemberPercentPosts()")
    # group name
    allMemberPercentPosts(sys.argv[2])

elif sys.argv[1] == "totalPostsPerGroup":
    print("Running totalPostsPerGroup()")
    # None
    totalPostsPerGroup()

elif sys.argv[1] == "sharedGroups":
    print("Running sharedGroups()")
    # None
    sharedGroups()

elif sys.argv[1] == "writeChats":
    print("Running writeChats()")
    # None
    writeChats()

elif sys.argv[1] == "longestMess":
    print("Running longestMess")
    # group name
    longestMess(sys.argv[2])

elif sys.argv[1] == "mostLikedSprints":
    print("Running mostLikedSprints()")
    # group name, number of sprints to write, spread, stagger
    mostLikedSprints(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

elif sys.argv[1] == "percentImagePost":
    print("Running percentImagePost()")
    # group name
    percentImagePost(sys.argv[2])

elif sys.argv[1] == "numLikesGiven":
    print("Running numLikesGiven()")
    # group name
    numLikesGiven(sys.argv[2])

elif sys.argv[1] == "stealthLikeOthers":
    print("Running stealthLikeOthers()")
    # group name, like/unlike
    stealthLikeOthers(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "messLikes":
    print("Running messLikes()")
    # group name, text
    messLikes(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "boardMessages":
    print("Running boardMessages()")
    # None
    boardMessages()

elif sys.argv[1] == "searchKeywordSprints":
    print("Running searchKeywordSprints")
    # group name, keyword/phrase, spread, stagger
    searchKeywordSprints(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

elif sys.argv[1] == "searchForKeyword":
    print("Running searchForKeyword")
    # group name (any/csv group/group), member name (any/csv member/member), keyword csv
    searchForKeyword(sys.argv[2], sys.argv[3], sys.argv[4])

elif sys.argv[1] == "numLikedMessages":
    print("Running numLikedMessages")
    # group name, nummessages
    mostLikedMessages(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "deltaMessages":
    print("Running deltaMessages()")
    # easyread True/False
    deltaMessages(sys.argv[2])

elif sys.argv[1] == "findNames":
    print("Running findNames()")
    # group name, True for reference group
    findNames(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "getAttributes":
    print("Running getAttributes()")
    getAttributes()

elif sys.argv[1] == "averMessPerMonth":
    print("Running averMessPerMonth")
    # group name
    averMessPerMonth(sys.argv[2])

elif sys.argv[1] == "storedFindKeyword":
    print("Running storedFindKeyword")
    # group name, keyword
    storedFindKeyword(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "printRecentMess":
    print("Running printRecentMess")
    # groupname, recentmess num
    printRecentMess(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "dateUserAdded":
    print("Running dateUserAdded")
    # groupname
    dateUserAdded(sys.argv[2])

elif sys.argv[1] == "memberStats":
    print("Running memberStats")
    # groupname, membername
    memberStats(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "peersShareGroups":
    print("Running peersShareGroups")
    # name1, name2
    peersShareGroups(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "totalGroups":
    print("Running totalGroups")
    # nothing
    totalGroups()

elif sys.argv[1] == "printAllMess":
    print("Running printAllMess")
    # groupname
    printAllMess(sys.argv[2])

elif sys.argv[1] == "lastPost":
    print("Running lastPost")
    # groupname
    lastPost(sys.argv[2])

elif sys.argv[1] == "downProfilePics":
    print("Running downProfilePics")
    # groupname
    downProfilePics(sys.argv[2])

elif sys.argv[1] == "mutedChat":
    print("Running mutedChat")
    # groupname
    mutedChat(sys.argv[2])

elif sys.argv[1] == "messInMonth":
    print("Running messInMonth")
    # groupname
    messInMonth(sys.argv[2])

elif sys.argv[1] == "likeStats":
    print("Running likeStats")
    # groupname
    likeStats(sys.argv[2])

elif sys.argv[1] == "printMessOfType":
    print("Running printMessOfType")
    # groupname
    printMessOfType(sys.argv[2])

elif sys.argv[1] == "likeStreak":
    print("Running likeStreak")
    # groupname
    likeStreak(sys.argv[2])

elif sys.argv[1] == "backupNewGroups":
    print("Running backupNewGroups")
    # none
    backupNewGroups()

elif sys.argv[1] == "scopedSharedGroups":
    print("Running scopedSharedGroups")
    # source group name
    scopedSharedGroups(sys.argv[2])

elif sys.argv[1] == "groupBirthdays":
    print("Running groupBirthdays")
    # none
    groupBirthdays()

elif sys.argv[1] == "backupIDs":
    print("Running backupIDs...")
    # none
    backupIDs()

elif sys.argv[1] == "origMems":
    print("Running origMems...")
    # groupname
    origMems(sys.argv[2])

elif sys.argv[1] == "consecPosts":
    print("Running consecPosts...")
    # groupname
    consecPosts(sys.argv[2])

elif sys.argv[1] == "liker":
    print("Running liker...")
    # groupname, number of likes or all
    liker(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "findMessages":
    print("Running findMessages...")
    # groupname, membername
    findMessages(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "usersLeft":
    print("Running usersLeft...")
    # groupname, date (MM/DD/YYYY)
    usersLeft(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "backupMems":
    print("Running backupMems...")
    # groupname
    backupMems(sys.argv[2])

elif sys.argv[1] == "noLikes":
    print("Running noLikes...")
    # groupname
    noLikes(sys.argv[2])

elif sys.argv[1] == "fullDownVids":
    fullDownVids(sys.argv[2])

elif sys.argv[1] == "eventsAttended":
    eventsAttended(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "dateJoined":
    dateJoined(sys.argv[2])

elif sys.argv[1] == "aveLikesReceived":
    print("Running aveLikesReceived...")
    aveLikesReceived(sys.argv[2])

elif sys.argv[1] == "responseTime":
    print("Running responseTime...")
    responseTime(sys.argv[2])

elif sys.argv[1] == "lastInteraction":
    print("Running lastInteraction...")
    lastInteraction(sys.argv[2])

elif sys.argv[1] == "groupOwners":
    print("Running groupOwners...")
    groupOwners()

elif sys.argv[1] == "downPics":
    print("Running downPics...")
    downPics(sys.argv[2])

elif sys.argv[1] == "likesGivenOverTime":
    print("Running likesGivenOverTime...")
    likesGivenOverTime(sys.argv[2], sys.argv[3])

else:
    print("Command doesn't exist")
