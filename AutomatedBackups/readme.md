# Automated Backups

To give credit where credit's due, Apple does an incredible job of making a user-friendly interface for backing up the system's files. They call it Time Machine.

While there are many similar solutions for Windows, all the ones I've found are either paid or too janky to trust/use. Since I've been diving into Python so much, I figured why not make my own janky version so I can at least troubleshoot it and know what's going on, right?

I'm not trying to backup an entire hard drive like Time Machine does, although I guess it's technically possible with this. The point of this is to backup files/folders you regularly access and are important to you to another location. That can be a USB or another hard drive altogether.

You might be thinking, "Why would I go through the pain of making this when there's Google Drive or Dropbox or OneDrive?" 1) This took me 20 minutes to make. A beginner could make it in an hour tops. 2) I personally don't like storing sensitive information (PII, taxes, passwords, etc.) in those cloud storage environments. But then again, I'm a cybersecurity major so I'm paranoid like that.

### Instructions

#### 1. `AutomatedBackup.py [set, run]`

  The brains behind the operation.

  The `set` parameter MUST be executed first or the `run` parameter won't work because it won't have anything to backup. When you execute `set`, the script prompts you to browse to a source (the folder you want to backup) and destination (where the backups will be stored). Then it creates a `path.py` file locally and writes those paths to it for future reference. These paths can be changed at any time by running `set` again.

  After writing the paths, it creates a `TaskSchedulerStarter.bat` and prompts you to find the `python.exe` file in your Local AppData directory tree. Give it a google if you're unsure of where to find it.

  The `run` parameter imports the paths from `path.py` and creates a timestamped backup folder within the destination and attempts to copy the source over to it. The current logic does NOT delete old backups, so be careful of drive space as the backups continue.

#### 2. `path.py`

  Created/Modified automatically by running `python AutomatedBackup.py set`. The only two lines in this file are the source and destination paths.

#### 3. `TaskSchedulerStarter.bat`

  Created automatically. This is a Windows batch file that allows Windows Task Scheduler to run the Python script. The batch file needs the path to your current `python.exe` file and the path to `AutomatedBackup.py`. Those are written as strings with the `run` parameter at the end. For example:
  ```
  "C:\Users\YourUsername\AppData\Local\Programs\Python\Python39\python.exe" "C:\Users\YourUsername\Documents\GitHub\bgoings-public\AutomatedBackups\AutomatedBackup.py" run
  ```

#### Task Scheduler

The next step is to create a Task Scheduler task:

1. Open `Task Scheduler > Action > Create Basic Task`
2. Give it an arbitrary name and set a desired frequency for the backup to occur
3. Click Next with "Start a program" selected
4. Select `TaskSchedulerStarter.bat` as the program/script
5. Leave all further settings blank/default and finish

Voila! You're good to go.

### Further Development

- Make a way to delete, overwrite, or use a more differential/incremental method on old backups like corporate environments do
- Automate creating the Task Scheduler task
- Allow for multiple source folders and/or multiple destination folders
