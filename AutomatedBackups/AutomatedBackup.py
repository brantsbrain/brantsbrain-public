# GOAL: Create a script that can be run through Task Scheduler that backs up files from a provided source to a provided destintation
# CRITERIA: Must be able to copy entire directories
# DELIVERABLE: Script to give to Task Scheduler to execute on any given frequency
# AFTER ACTION REPORT: Much easier to create than I initially thought. See readme.md for additional functionality that could be added

import shutil, os, sys
from tkinter.filedialog import askdirectory, askopenfilename
from datetime import datetime

# Create/Overwrite path file with desired source and destination backup folder paths
def setPaths():
    # Declare variables
    pyexists = False
    filename = "AutomatedBackup.py"

    # If the file already exists, then we can import the existing arrays
    try:
        from path import sourpaths, destpaths
    # If not, we'll create them along the way
    except:
        pass

    # Print welcome message
    print("\nWelcome!\n\n"
            "If this is the first time you're running Automated Backup, you MUST modify source AND destination folders when prompted.\n\n"
            "During source and destination folder selection, in order to END folder selection, you MUST select the folder containing\n"
            "this file. I recommend running this file for this first time in a safe folder like Documents where it won't accidentally be deleted.\n\n"
            "Pay attention to the folder selection window title to know if you're selecting a source or destination.\n\n"
            "You may rerun this file with the set parameter as many times as you like afterwards and give the N parameter to source/destination if desired.\n\n"
            "During the first run, you will be prompted to find the 'python.exe' file. This is oftentimes found in C:\\Users\\*username*\\AppData\\Local\\Programs\\Python\\... but you may need to search online if that isn't the case for you.\n\n"
            "I hope this script serves you well!\n\n"
            "- Brant\n\n")


    modsour = input("Would you like to modify source folder(s)? (Y/N): ")
    if modsour.upper() == "Y":
        sourpaths = []
        # Select source folder(s)
        print("Select as many source folders as you'd like, which will be copied to all destination folders selected later.")
        print("When done selecting folders, select the folder containing this file.")
        pause1 = input("Press enter when ready to continue...")
        while not pyexists:
            sourpath = askdirectory(title="Select Source Folder")
            if os.path.exists(f"{sourpath}\\{filename}"):
                pyexists = True
            else:
                sourpaths.append(sourpath)
        print(f"Stored source path(s): {sourpaths}")
    else:
        print(f"Continuing with source path(s): {sourpaths}")

    # Reset pyexists for use in next while loop
    pyexists = False

    moddest = input("\nWould you like to modify destination folder(s)? (Y/N): ")
    if moddest.upper() == "Y":
        destpaths = []
        # Select destination folder(s)
        print("Select as many folders as you'd like. All source folders will be copied to all these folders.")
        print("When done selecting folders, select the folder containing this file.")
        pause2 = input("Press enter when ready to continue...")
        while not pyexists:
            destpath = askdirectory(title="Select Destination Folder")
            if os.path.exists(f"{destpath}\\{filename}"):
                pyexists = True
            else:
                destpaths.append(destpath)
        print(f"Stored destination path(s): {destpaths}")
    else:
        print(f"Continuing with destination path(s): {destpaths}")

    print()
    try:
        print("Creating/Modifying path file...")
        # Create or overwrite the path.py folder with paths found above
        with open("path.py", "w") as writer:
            writer.write(f'sourpaths = {sourpaths}\n'
                            f'destpaths = {destpaths}')

        # Print confirmation of paths written to path.py
        print(f"Set source path(s) to: {sourpaths}")
        print(f"Set destination path(s) to: {destpaths}")
    except:
        print("Error creating/modifying path file. Quitting...")
        exit()

    task = "TaskSchedulerStarter.bat"
    # Check to see if the file already exists. Skip if so
    if not os.path.exists(task):
        # Prompt through GUI for the exact filepath for python.exe
        pythonpath = askopenfilename(title="Select Python.exe")
        # Store the current working directory plus the script's name
        currentpath = f"{os.getcwd()}\\{filename}"

        with open(task, "w") as writer:
            # Write the path to python.exe and this script as strings with run parameter to the new batch file
            writer.write(f'"{pythonpath}" "{currentpath}" run')

        # Print confirmation of paths written to batch file
        print(f"Set Python path to: {pythonpath}")
        print(f"Set script path to: {currentpath}")

        # Create Task Scheduler Task
        os.system(f'SchTasks /Create /SC WEEKLY /TN "Python Automated Backups" /TR "{os.getcwd()}\\{task}" /ST 09:00')
    else:
        print("Task Scheduler Starter and Task already created...")

# Run backup procedure
def run():
    # This will fail if the set parameter hasn't been run yet
    try:
        from path import sourpaths, destpaths
    except:
        print("Unable to import path file. Run set parameter...")
        exit()

    # Backup the source folder to a new folder "Backup_MonthDayYear_HourMinute" in destination path
    timestamp = datetime.now().strftime("%m%d%y_%H%M")

    # Iterate through source/destination folders from paths
    for sourpath in sourpaths:
        for destpath in destpaths:
            destpath = f"{destpath}/Backup_{timestamp}"

            # Attempt to copy folder. Haven't stress tested, so I don't know what errors could come up
            try:
                if not os.path.exists(destpath):
                    shutil.copytree(sourpath, destpath)
                    print(f"{sourpath} to {destpath} backup finished")
                else:
                    print(f"{sourpath} to {destpath} already backed up")
            except Exception as e:
                print(f"Error in copying files: {e} \nQuitting...")
                exit()

# Parameters available when running script
if sys.argv[1] == "set":
    setPaths()
elif sys.argv[1] == "run":
    run()
