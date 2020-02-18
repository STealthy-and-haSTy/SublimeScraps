Sublime Session Cleaner
-----------------------

As you work with Projects in Sublime Text or repositories in Sublime Merge, the
list of items that you've worked with in the past is stored inside of the
Sublime session file, allowing you to easily and quickly switch between them.
Additionally, Sublime Text also tracks recently used files and folders to make
working with them again in the future easier.

One issue with this mechanism is that if a project or repository no longer
exists (or a file or folder has been removed), there is no straight forward way
to remove it from the list of recent items.

This directory contains a script for Python 3 that will load up the Sublime
session file for either Sublime Text or Sublime Merge and remove from the list
of recent items all of the entries for things that no longer exist.


### Usage

In order to use this script, you must have Python 3 installed on your computer,
since this is an external script and not a Sublime plugin. Additionally, make
sure that Sublime (Text or Merge) isn't running while you run the script, since
the session file is persisted to disk on exit, which will make Sublime restore
its in-memory version of the session.

You can use the `--program` command line argument to specify whether you want
to clean the recent items for Sublime Text or Sublime Merge, with the default
being Sublime Text.

If you're **not** running a Portable version of Sublime, you can just run the
script directly in the manner that you would normally execute a Python script
on your platform. The script will determine what platform you're on and use
that information to locate the Sublime session file.

If you **are** using a Portable version of Sublime, then you need to invoke the
script with the `--data-dir` argument to tell it where the Data directory is,
so that the Sublime session file can be found. This can be a fully qualified
path or a path relative to the current working directory.

When you run the script, you must specify the items that you would like to have
cleaned out of the session file by using the following command line arguments.
Note that Sublime Merge only supports the first argument, but providing the
others is harmless and will do nothing.

  * `--workspaces` to clean up the list of project/workspace files (Sublime
    Text) or git repositories (Sublime Merge) that no longer exist

  * `--files` to clean up the list of recently accessed files that no longer
    exist. (Note: If you had multiple windows open when you quit Sublime, this
    action will trigger once for each window since they all carry their own
    history).

  * `--files` to clean up the list of recently opened folders that no longer
    exist.

The script works by loading up the session, finding the list of recent items,
and then checking each one to see if it still exists or not. Any items that no
longer exist will be written to the console and removed from the loaded session
information.

If any missing items are found, the new session information is written out to
disk after first making a backup of the existing session file (the name of the
created backup file is displayed when it is created). You can specify the
`--dry-run` parameter to the script to have it tell you what it would do
without actually doing it.

Something to note is that testing for the existence of a file or directory on a
network share or external disk that is not currently connected or mounted
results in a determination that the path does not exist (technically accurate
but somewhat unhelpful).

As such, if you tend to work with items stored in those locations, you may want
to use `--dry-run` to verify that existing but currently unavailable items are
not going to be removed.

If you don't heed that advice, you can always get your previous session back
from the session backups.

Lastly, no cleanup is done of session backups, so you may need to go into your
Sublime Data directory and clean up the backups from time to time.


### Bonus Script

The folder also contains a shell script that I use to kick off this script on
my Linux machine as a demonstration of how to use the session cleaning script
automatically to clean up Sublime Text projects.

This should work on MacOS as well (assuming the command can be found on the
`PATH`), but a Windows batch file that does this is left as an exercise to the
Windows reader. A similar item could be constructed for Sublime Merge as well
using a similar design.

Although I manually invoke `subl` on the command line to start Sublime most of
the time, I also have a task bar icon set up to launch it from my Linux Window
Manager as well.

For the task bar icon, this script is executed instead of directly invoking
`subl`. The script checks to see if Sublime is already running or not, and if
it's not it runs the session cleanup script prior to starting Sublime. When
Sublime **is** running, this creates a new window; remove the `-n` argument if
you do not want that sort of behaviour.
