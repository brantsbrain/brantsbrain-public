elif sys.argv[1] == "pullURL":
    print("Running pullURL()")
    # group name
    pullURL(sys.argv[2])

elif sys.argv[1] == "pullGallery":
    print("Running pullGallery()")
    # group name
    pullGallery(sys.argv[2])

elif sys.argv[1] == "downImages":
    print("Running downImages()")
    # group name
    downImages(sys.argv[2])

elif sys.argv[1] == "percentImagePost":
    print("Running percentImagePost()")
    # group name
    percentImagePost(sys.argv[2])


elif sys.argv[1] == "pullAllGalleries":
    print("Running pullAllGalleries()")
    # nothing
    pullAllGalleries()

elif sys.argv[1] == "downAllGalleries":
    print("Running downAllGalleries()")
    # nothing
    downAllGalleries()



elif sys.argv[1] == "pullGroup":
    print("Running pullGroup")
    # groupname
    pullGroup(sys.argv[2])

elif sys.argv[1] == "printPandas":
    print("Running printPandas")
    # groupname
    printPandas(sys.argv[2])

elif sys.argv[1] == "printAllMess":
    print("Running printAllMess")
    # groupname
    printAllMess(sys.argv[2])

elif sys.argv[1] == "imageURLs":
    print("Running imageURLs")
    # groupname
    imageURLs(sys.argv[2])

elif sys.argv[1] == "lastPost":
    print("Running lastPost")
    # groupname
    lastPost(sys.argv[2])



elif sys.argv[1] == "messInMonth":
    print("Running messInMonth")
    # groupname
    messInMonth(sys.argv[2])


elif sys.argv[1] == "scopedSharedGroups":
    print("Running scopedSharedGroups")
    # source group name
    scopedSharedGroups(sys.argv[2])

elif sys.argv[1] == "backupIDs":
    print("Running backupIDs...")
    # none
    backupIDs()

elif sys.argv[1] == "origMems":
    print("Running origMems...")
    # groupname
    origMems(sys.argv[2])

elif sys.argv[1] == "findMessages":
    print("Running findMessages...")
    # groupname, membername
    findMessages(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "usersLeft":
    print("Running usersLeft...")
    # groupname, date (MM/DD/YYYY)
    usersLeft(sys.argv[2], sys.argv[3])

else:
    print("Command doesn't exist")
