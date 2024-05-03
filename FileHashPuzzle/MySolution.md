### My Thought Process

I broke down my thought process into three steps: 1) Retreive all 1000+ directories from the web server and put them locally on my machine. I did this through Powershell. 2) Iterate through each folder and append the text from each .sha1 file into one `mergefile.txt`. Also did this through Powershell. 3) Iterate through that file with Python and compare each line to the SHA1 hash of 000, 0000, and 00000. If one of them matches, increase my counter by one.

The submission was the number of bot accounts there were, which I successfully found on the first try!

#### `GenFileStructure.py`

After finishing the competition, I thought back to this problem and wanted to reverse-engineer it myself, so I created `GenFileStructure.py`, which creates 1,000 folders, each with its own .sha1 file, and at the end it creates `SecretNum.txt` and writes how many bots it created.

#### `CountBots.py`

This is a "prettier" version of the Python I used to crack the hashes. This one includes the CLI command that I used to merge the files, which I had done seperately in the competition. It also has a safeguard and a Linux/Windows prompt, which I obviously would've left out in the competition. Consider this the "answer sheet" that I created, although there are definitely other ways it could've been done.

#### `CleanUp.py`

Not needed, but just a short way to delete the structure `GenFileStructure.py` created. Especially useful in Linux since you may not have a GUI to work with.