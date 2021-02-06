# Goal: Import Google Contacts CSV and format to use in MessageParser.py
# Deliverable(s): CSV w/ name and number
# Required Criteria: SMS Backup and Restore format CSV - first last, +12223334444

# The path variable points to the downloaded Google Contacts CSV
from creds import path
import pandas as pd

# Create DataFrame from Google Contacts CSV using name and number columns
contactframe = pd.read_csv(path, usecols=["Name", "Phone 1 - Value"])

# Characters to remove from imported numbers
badcharlist = [" ", "(", ")", "+", "-"]

# Fill lines list w/ number column
lines = []
for cell in contactframe["Phone 1 - Value"]:
    lines.append(str(cell))

# Remove unwanted characters from lines
for badchar in badcharlist:
    for line in lines:
        if badchar in line:
            lines[lines.index(line)] = line.replace(badchar, "")

# Format w/ + or +1 where needed
for line in lines:
    if len(line) == 10:
        lines[lines.index(line)] = "+1" + line
    else:
        lines[lines.index(line)] = "+" + line

# Create a new column w/ modified lines list
contactframe["Number"] = lines

# Delete old column
del contactframe["Phone 1 - Value"]

# Write contactframe to CSV
contactframe.to_csv(r".\contacts_sanitized.csv", index=False)
