# GroupMe Scripts

These scripts played a large role in teaching me the ins and outs of Python sheerly based on how much time I spent making them (probably sitting around 200 hours logged at this point). I've had GroupMe since 2014 and am in over 135 groups. Some of these groups have over 75,000 (yes, seventy-five thousand) messages, some have under 100. Some have over 100 members, some have under 10. Some have 3,000+ images, some have none. The list goes on and on.

I've always wanted a way to collect that data, mostly to back it up so if GroupMe ever burned down, I'd still have a way to look back on the memories from those group messages that I share with friends and family. After finding Groupy, though, I found out that I could do so much more... and so began the GroupMe Scripts!

I tried to make readable comments at the beginning of every method/function in the scripts to give an understanding of what each of them did. Please let me know if I should expand on any of them!

Here is a brief summary and some examples of the initial setup and how to run each script:

### Setup

Setup is actually fairly easy (at least when I did it).

Groupy is a downloadable package with instructions found here: https://pypi.org/project/GroupyAPI/.

Another good API can be found at: https://groupy.readthedocs.io/en/master/pages/api.html (yes I realize they're technically the same API, but they explain the package in different ways)

The GroupMe Developer page has instructions on how to get your GroupMe token: https://dev.groupme.com/

Make a `creds.py` file in the same directory as the GroupMe scripts, create a variable called `token` and paste your token as a string

#### Example:

`creds.py`
```
# This is your unique token found through dev.groupme.com
token = "123myreallylongtokenstring"

# Filling exceptionlist is optional, but at least declare it
exceptionlist = ["names", "that", "get", "special", "consideration", "in", "some", "methods"]

# Keeps you from having to enter long lists of static groups
bulklist = ["Favorite Group", "Family Group", "Friend Group"]

# Groups you don't want to assess in certain functions
skipgrouplist = ["Soccer Group", "Old Group"]

# Only used in findNames() right now, but allows you to use a name you know
refgroup = "Soccer Group"
```


### ./GroupMeBot

This was the first script I made. Its purpose is to interact directly with any group on the controller's behalf. It can run any analysis on any given GroupMe and post directly into the GroupMe whatever results it finds. It can also "listen" to messages realtime from any user in the group and decide whether or not to run commands from that user based on their privileges in the group.

I ran into issues with this one when a network exception came up. I believe my sessions were timing out and couldn't figure out how to restart them. Apparently this block of code wasn't executing in my try/catch block:

`except requests.exceptions.HTTPError as net:`

I also found out that it crashes when you try to run it in multiple groups simultaneously. I don't think that's something I can fix. It's just the way GroupMe built their infrastructure.

#### Example:

Console:

`python3 ./GroupMeBot.py monBot groupname`

Member post in groupname:

`!numPosts:membername:`

Console:
```
membername executed numPosts
Ran command
```

GroupMeBot's post (on your behalf) in groupname:

`BOT: membername has posted X time(s)`

### ./GroupMeData

Script used to run any command/option within the other `./GroupMe` files. Run `python3 ./GroupMeData.py help` to list available commands and needed inputs.

Constantly under development, I'm always looking for new information to find.

#### Example:

Console:

`python3 ./GroupMeData.py numLikesGiven groupname`
```
Looking for groupname
Found groupname
Filling memberdict...
Filling messagelist...
Filling likes...
Sorting memberdict...
Writing results...
```

File:

`PercentageLikes.txt`
```
Percentage of likes given of messages not posted by member in groupname...
membername1 liked XX.XX% of X messages
membername2 liked XX.XX% of X messages
membername3 liked XX.XX% of X messages
...
```

### ./GroupMeAnalysis

Contains functions that deal with analyzing groups for length of messages, average number of messages, etc. The logic per function is probably the most complex compared to the others.

### ./GroupMeBackups

Deals with backing up group messages either one at a time or in bulk.

### ./GroupMeFinders

Handles searching for keywords/phrases, but also contains the two most important functions: `findGroup(groupname)` and `findMember(group, member)` which are used in nearly every other function. These functions are imported to each of the other scripts.

### ./GroupMeGallery

Used to download the gallery and any `v.groupme.com` URLs (video) in the group

### ./GroupMeLikes

Handles any analysis related to number of likes within groups
