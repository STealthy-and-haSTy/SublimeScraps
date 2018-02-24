Sublime Session Cleaner
-----------------------

As you work with Projects in Sublime, the list of projects that you've worked
with in the past is stored inside of the Sublime session file, allowing you to
easily switch between projects.

One issue with this mechanism is that if a project no longer exists, there is
no straight forward way to remove it from the list of projects in the project
switcher.

This directory contains a script for Python 3 that will load up the Sublime
session file and remove from the list of recent workspaces all of the entries
for projects that no longer exist.


### Usage

In order to use this script, you must have Python 3 installed on your computer,
since this is an external script and not a Sublime plugin. Additionally, make
sure that Sublime isn't running while you run the script, since the session
file is persisted to disk on exit, which will make Sublime restore its
in-memory version of the session.

If you're not running a Portable version of Sublime, you can just run the
script directly in the manner that you would normally execute a Python script
on your platform. The script will determine what platform you're on and use
that information to locate the Sublime session file.

If you are using a Portable version of Sublime, then you need to invoke the
script with the `--data-dir` argument to tell it where the Data directory is,
so that the Sublime session file can be found. This can be a fully qualified
path or a path relative to the current working directory.

The script works by loading up the session, finding the list of recent
workspaces, and then checking each one to see if it still exists or not. Any
files that no longer exist will be written to the console and removed from the
loaded session information.

If any missing session files are found, the new session information is written
out to disk after first making a backup of the existing session file. You can
specify the `--dry-run` parameter to the script to have it tell you what it
would do without actually doing it.

Something to note is that testing for the existence of a file on a network
share or external disk that is not currently connected or mounted results in a
determination that the file does not exist (technically accurate but somewhat
unhelpful).

As such, if you tend to use projects stored in those locations, you may want to
use `--dry-run` to verify that existing but currently unavailable workspaces are
not going to be removed.

If you don't heed that advice, you can always get your previous session back
from the session backups.

Lastly, no cleanup is done of session backups, so you may need to go into your
Sublime Data directory and clean up the backups from time to time.


### Bonus Script

The folder also contains a shell script that I use to kick off this script on
my Linux machine as a demonstration of how to use the session cleaning script
automatically. This should work on MacOS as well, but a Windows batch file that
does this is left as an exercise to the Windows reader.

Although I manually invoke `subl` on the command line to start Sublime most of
the time, I also have a task bar icon set up to launch it from my Linux Window
Manager as well.

For the task bar icon, this script is executed instead of directly invoking
`subl`. The script checks to see if Sublime is already running or not, and if
it's not it runs the session cleanup script prior to starting Sublime.

This keeps things more or less automatically cleaned up, so long as I happen to
quit Sublime for some reason.
