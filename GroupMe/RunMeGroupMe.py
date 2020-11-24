from GroupMeData import *

if str(sys.argv[1]) == "help":
    print("Available options:\n\n\t"
            "delta - only make backups of changed groupmes\n\t"
            "find - search for a given group name\n\t"
            "names - create GroupNames.txt containing all active groups\n\t"
            "averMessLength - Find individualized stats for a group (takes group name)\n\t"
            "numLikes - Find number of messages per member that got 1+ like (takes group name) \n\t"
            "mostLikedMessages - Return the top five most liked messages (takes group name)\n\t"
            "commonWords - Return most said words per member (takes group name)\n\t"
            "myinfo - Return current user info\n\t"
            "percent - Return sorted list of percentage of posts per member (takes group name)\n\t"
            "groupNum - Return sorted list of total posts per group\n\t"
            "sharedGroups - Return list of shared groups per member\n\t"
            "writeChats - Write DMs to file\n\t"
            "longestMess - Print longest message from specified group (takes group name)\n\t"
            "mostLikedSprints - Write most liked posts surrounded by provided number of messages (takes group name, number of posts to write, number of messages behind and in front, and stagger)\n\t"
            "pullURL - Write GroupMe video URLs to file (takes group name)\n\t"
            "pullGallery - Write gallery URLs to file (takes group name)\n\t"
            "downImages - Download gallery photos from pullGallery() file (takes group name)\n\t"
            "percentImagePost - Write percentage of images posted per member (takes group name)\n\t"
            "numLikesGiven - Show the percentage of posts liked that weren't posted by the member (takes group name)\n\t"
            "")
elif str(sys.argv[1]) == "delta":
    print("Running backupChanged()")
    backupChanged()
elif sys.argv[1] == "writeAll":
    # group name and easyread string value True/False
    writeAllMessages(sys.argv[2], sys.argv[3])
elif sys.argv[1] == "backupAll":
    # provide easyread string value True/False
    backupAll(sys.argv[2])
elif str(sys.argv[1]) == "find":
    print("Running findGroup()")
    findGroup(sys.argv[2])
elif str(sys.argv[1]) == "names":
    print("Running writeGroupNamesToFile()")
    writeGroupNamesToFile()
elif str(sys.argv[1]) == "averMessLength":
    print("Running averMessLength()")
    averMessLength(sys.argv[2])
elif str(sys.argv[1]) == "numLikes":
    print("Running numlikes()")
    numLikes(sys.argv[2])
elif str(sys.argv[1]) == "mostLikedMessages":
    print("Running mostLikedMessages()")
    mostLikedMessages(sys.argv[2])
elif str(sys.argv[1]) == "commonWords":
    print("Running commonWords()")
    commonWords(sys.argv[2])
elif str(sys.argv[1]) == "myinfo":
    print("Running myinfo()")
    printMyInfo()
elif str(sys.argv[1]) == "percent":
    print("Running allMemberPercentPosts()")
    allMemberPercentPosts(sys.argv[2])
elif str(sys.argv[1]) == "groupNum":
    print("Running totalPostsPerGroup()")
    totalPostsPerGroup()
elif str(sys.argv[1]) == "sharedGroups":
    print("Running sharedGroups()")
    sharedGroups()
elif (str(sys.argv[1])) == "writeChats":
    writeChats()
elif (str(sys.argv[1])) == "longestMess":
    longestMess(str(sys.argv[2]))
elif sys.argv[1] == "mostLikedSprints":
    mostLikedSprints(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
elif sys.argv[1] == "pullURL":
    pullURL(sys.argv[2])
elif sys.argv[1] == "pullGallery":
    pullGallery(sys.argv[2])
elif sys.argv[1] == "downImages":
    downImages(sys.argv[2])
elif sys.argv[1] == "percentImagePost":
    percentImagePost(sys.argv[2])
elif sys.argv[1] == "numLikesGiven":
    numLikesGiven(sys.argv[2])
elif sys.argv[1] == "stealthLikeOthers":
    stealthLikeOthers(sys.argv[2], sys.argv[3])
else:
    print("Command doesn't exist")
