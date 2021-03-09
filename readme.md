# brantsbrain/brantsbrain-public Projects

Welcome to my public repository. It has a bunch of my individual projects, some big and some small. I am FAR from an expert in Python, but I'd like to say I can figure out most problems after ample time at the keyboard! I tried to lay out which projects I thought were easy, medium, and hard to give new scripters an idea of where to start reading.

For those that don't know, the `./` notation is a Linux thing and just denotes that the specified directory is in your current directory. Nothing too fancy!

The `./GroupMe` project was particularly fun in my opinion and I definitely recommend checking it out regardless of your skill level.

If you'd like visual walkthroughs, check out my [Brant's Brain](https://www.youtube.com/channel/UC3QJF0KmLRIlfztOt06xXBQ) YouTube channel! It's small but growing.

Hope you enjoy one or both!

### ./AutomatedBackups

Difficulty - Easy/Medium

Script to schedule weekly backups of source folder(s) to destination folder(s). The basics of the project were very easy: I had to find a way to copy/paste a source folder to a destination folder. The project got harder as I tried to streamline the process so the user didn't have to do as much.

### ./AutomatedWeather

Difficulty - Hard

Used to gather historic weather data from Weather Underground. Developed as proof to a friend that a repetitive, manual job could be automated.

### ./BabyVotes

Difficulty - Easy

Heavily commented and a great introduction to Selenium. Used to enter info and click buttons on a regular schedule to contribute votes to an engine.

### ./CompareImages

Difficulty - N/A

The majority of this was not written by me. Its source is referenced in the script, and was modified by me to compare two images' pixel layout.

### ./FileHashPuzzle

Difficulty - Easy/Medium depending on hashlib experience

The project was inspired by a puzzle I came across at a cyber competition. Check out the `readme.md` within it for more info.

I've had experience with the hashlib library through `./PassCrack/HashCracker.py`, so I knew what I was getting into when I took on this one. If you don't have experience with the hashlib library, check out `./PassCrack/HashlibBasics.py` to see how it works.

I built out `CountBots.py` in ~15 minutes during the competition. Afterwards I built `GenFileStructure.py` and `CleanUp.py` which each took 10 minutes or so.

### ./GroupMe

Difficulty - Hard

See `readme.md` within folder

### ./MessageParser

Difficulty - Medium

Takes a XML file from *SMS Backup and Restore* on Google Play and runs analytics such as keyword search, message length search, or bulk backups.

### ./NBAStatFinder

Difficulty - Medium

Another case in showing a friend that a manual process could be automated. The only difficult part about this was finding an effective way to extract data from HTML cells. This is a good way to step up from easy tasks to medium tasks. Heavily commented to explain thought process.

### ./PassCrack

Difficulty - Hard

Contains `DictionaryBuilder.py` and `HashCracker.py`. The former builds a dictionary of passwords based off an initial set of relative phrases. The latter is used to crack any given dictionary after being supplied a rainbow table (hash list) and dictionary table

### ./SanitizeContacts

Difficulty - Easy

I needed a way to format the contacts I downloaded from my Google account so that MessageParser could interpret them correctly. Good introduction to the Pandas module

### ./StockTrader

Difficulty - Hard

Proof of concept for an automated trading program through Python and Robinhood. Requires a list of stock tickers and Pre-Market Highs (PMHs) for each ticker.

### ./Super Smash

Difficulty - Easy (`SimpleSmashRandomizer.py`), Medium (`SmashTourn.py`)

Meant for Super Smash Bros. Ultimate, `SimpleSmashRandomizer.py` randomly selects a given number of characters for players to use in a match. `SmashTourn.py` creates a tournament environment with any number of players, tracks which character each player has played, removes each character from that player's list, and marks which characters each player won with and against who those were.
