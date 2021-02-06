# GOAL: Create a script that can be run through Task Scheduler that backs up files from a provided source to a provided destintation
# CRITERIA: Must be able to copy entire directories
# DELIVERABLE: Script to give to Task Scheduler to execute on any given frequency
# AFTER ACTION REPORT: Much easier to create than I initially thought. See readme.md for additional functionality that could be added

import shutil, os, sys
from tkinter.filedialog import askdirectory, askopenfilename
from datetime import datetime

# Create/Overwrite path file with desired source and destination backup folder paths
def setPaths():
    # Open GUI to find path to desired source/destination folders
    sourpath = askdirectory(title="Select Source Folder")
    destpath = askdirectory(title="Select Destination Folder")

    try:
        print("Creating/Modifying path file...")
        # Create or overwrite the path.py folder with paths found above
        with open("path.py", "w") as writer:
            writer.write(f'sourpath = "{sourpath}"\n'
                            f'destpath = "{destpath}"')

        # Print confirmation of paths written to path.py
        print(f"Set source path to: {sourpath}")
        print(f"Set destination path to: {destpath}")
    except:
        print("Error creating/modifying path file. Quitting...")
        exit()

    task = "TaskSchedulerStarter.bat"
    # Check to see if the file already exists. Skip if so
    if not os.path.exists(task):
        # Prompt through GUI for the exact filepath for python.exe
        pythonpath = askopenfilename(title="Select Python.exe")
        # Store the current working directory plus the script's name
        currentpath = f"{os.getcwd()}\\AutomatedBackup.py"

        with open(task, "w") as writer:
            # Write the path to python.exe and this script as strings with run parameter to the new batch file
            writer.write(f'"{pythonpath}" "{currentpath}" run')

        # Print confirmation of paths written to batch file
        print(f"Set Python path to: {pythonpath}")
        print(f"Set script path to: {currentpath}")
    else:
        print("Task Scheduler Starter already created...")

# Run backup procedure
def run():
    # This will fail if the set parameter hasn't been run yet
    try:
        from path import sourpath, destpath
    except:
        print("Unable to import path file. Run set parameter...")
        exit()

    # Backup the source folder to a new folder "Backup_MonthDayYear_HourMinute" in destination path
    timestamp = datetime.now().strftime("%m%d%y_%H%M")
    destpath = f"{destpath}/Backup_{timestamp}"

    # Attempt to copy folder. Haven't stress tested, so I don't know what errors could come up
    try:
        print("Attempting backup...")
        shutil.copytree(sourpath, destpath)
        print("Backup Finished")
    except:
        print("Error in copying files. Quitting...")
        exit()

# Parameters available when running script
if sys.argv[1] == "set":
    setPaths()
elif sys.argv[1] == "run":
    run()
