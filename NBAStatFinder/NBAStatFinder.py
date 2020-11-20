# Goal: Create an automated stats collector for a given NBA team and season from basketball-reference.com
# Deliverables: Player CSVs w/ individual game stats for that season contained in a team folder

########## IMPORTS ##########
# Try to import required packages/modules
try:
    # These packages help create folders and write to files
    import os, sys, csv
    # This helps us get the year
    from datetime import datetime
    # This helps us pull in the HTML we need from the team's website
    from urllib.request import urlopen
    # This formats the HTML in a way we can analyze it
    from bs4 import BeautifulSoup
# If there was a problem importing one of the above packages, print and quit
except ImportError as e:
    print(f"Wasn't able to import one or more needed packages. Try running 'pip install x' where x is the missing package. Here's the error: {e}")
    exit()
# If there was any other issue up until this point, the program most likely won't run, so print and quit
except Exception as e:
    print(f"Fatal error occurred: {e}")
    exit()

########## METHOD ##########
# Use makeCSV() to create a file per player and write individual stats
def makeCSV(url, player, season, foldername):
    # Gather player information from the URL passed
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.findAll("table", {"id":"pgl_basic"})[0]
    rows = table.findAll("tr")

    # Write each cell as a line in the CSV
    with open(f".\\{foldername}\\{player}_{season}.csv", "wt+", newline="") as opener:
        writer = csv.writer(opener)
        print(f"Working on {player}...")
        for row in rows:
            csv_row = []
            for cell in row.findAll(["td", "th"]):
                csv_row.append(cell.get_text())
            writer.writerow(csv_row)

########## MAIN ##########
# Give welcome message and instructions
print("\n"
        "Welcome to NBAStatFinder. Stats are collected from www.basketball-reference.com and are written to the same folder this file is in.\n\n"
        "You are currently being prompted for a team abbrevation. Every NBA team has a three letter abbreviation available. If you enter nothing, the program will assume you would like stats for the 76ers.\n\n"
        "Next you will enter a year. Enter the second year of the season. For example, if you want the 2012-13 season, enter 2013. If you don't enter a season, the program will assume you want the most current season.\n\n"
        "To end the program at any time, press Ctrl+C\n\n"
        "\tHappy stats collecting!\n\n"
        "\t- Brant\n\n")

# Input team abbreviation and season
team = input("Enter team abbreviation [PHI]: ")
season = input(f"Enter season [{datetime.today().year}]: ")
print()

# Assuming PHI if team string is empty
if team == "":
    team = "PHI"
print(f"Will gather stats for {team}")

# Assuming current year if season string is empty
if season == "":
    season = str(datetime.today().year)
print(f"Will gather stats from {int(season) - 1}-{season[2:]}")

# Build the team's season URL
teamsite = f"https://www.basketball-reference.com/teams/{team}/{season}.html"

# Try to find the site. If invalid, print and quit
try:
    html = urlopen(teamsite)
    print(f"Found the {team} {int(season) - 1}-{season[2:]} season\'s website")
except Exception as e:
    print(f"The team {team} and/or the season {season} is incorrect, because the program couldn't find the right webpage. Here's the error: {e}")
    exit()

# Create folder if not already created
foldername = f"{team}_{season}_Stats"
try:
    os.makedirs(foldername)
    print(f"Created {foldername} folder")
except:
    print(f"{foldername} folder already exists")

# Build the table of player names and prep URL
soup = BeautifulSoup(html, "html.parser")
table = soup.findAll("table", {"id":"roster"})[0]
rows = table.findAll("tr")
beginurl = "https://www.basketball-reference.com/"

# Write player stats
for row in rows:
    for a in row.findAll("a"):
        # Need this if statement because we'd get college names included otherwise
        if "players" in a["href"]:
            try:
                # Pass the full player URL, the player name, the season, and the folder to write to
                makeCSV(beginurl + a["href"][:-5] + f"/gamelog/{season}", a.text, season, foldername)
            except Exception as e:
                print(f"Encountered an error with {a.text}: {e}")

print("Program Finished\n")
