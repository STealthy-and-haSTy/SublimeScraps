#!/bin/env python3
"""
Load the Session.sublime_session file from the Sublime Text 3 data directory
and remove all of the recent workspaces that refer to projects that no longer
reside on disk.

If no command line arguments are provided, the script will look for the session
file in the data directory location standard for the current platform. When a
command line argument is provided, it's assumed to the location of the Data
folder to use, which can be relative to the current directory or an absolute
path.

This creates the new session file (if any) to a temporary file first and then
renames the session into place. During this process the original session file
is stored as a backup in a file with the current date and time appended.

This script shouldn't be run while Sublime is actively running, since the
session information will be written out to disk when Sublime terminates, which
will cause the changes made by this script to be ignored.
"""

from datetime import datetime
import json
import logging
import os
import sys


def sublime_data_dir():
    """
    Obtain the path to the Sublime Text 3 Data directory in a platform
    independent way. This doesn't work for portable installs however.
    """
    if sys.platform.startswith("linux"):
        return os.path.expanduser("~/.config/sublime-text-3/")
    elif sys.platform.startswith("win"):
        return os.path.expandvars("$APPDATA\\Sublime Text 3\\")

    return os.path.expanduser("~/Library/Application Support/Sublime Text 3/")


def clean_session(data_dir):
    """
    Load the session file from the data directory and remove all of the
    projects that no longer exist on disk, writing the session back.

    This attempts to keep a backup of the existing session file and creates a
    temporary session first in case things go pear shaped.
    """
    session_file = os.path.join(data_dir, "Local", "Session.sublime_session")
    tmp_file = session_file + ".tmp"
    bkp_file = session_file + datetime.now().strftime(".%Y%m%d_%H%M%S")

    logging.info("Using Data Directory: %s", data_dir)
    try:
        with open(session_file, encoding="utf-8") as file:
            session = json.load(file)

        workspaces = session["workspaces"]["recent_workspaces"]
        present, missing = [], []
        for file in workspaces:
            status_list = present if os.path.isfile(file) else missing
            status_list.append(file)

        if len(present) == len(workspaces):
            return logging.info("No missing projects found")

        for file in missing:
            logging.info("  %s", file)
        logging.info("Expunged %d workspace(s)", len(missing))

        workspaces[:] = present
        with open(tmp_file, "w", encoding="utf-8") as file:
            json.dump(session, file,
                      indent="\t",
                      ensure_ascii=False,
                      sort_keys=True,
                      separators=(',', ': '))

        os.rename(session_file, bkp_file)
        os.rename(tmp_file, session_file)

        logging.info("New session file saved")

    except FileNotFoundError:
        logging.exception("Unable to locate session file")
    except KeyError:
        logging.exception("Unable to find recent workspace list")
    except OSError:
        logging.exception("Error replacing session information")


def main(argv):
    logging.basicConfig(level=logging.INFO)
    clean_session(argv[1] if len(argv) > 1 else sublime_data_dir())


if __name__ == "__main__":
    main(sys.argv)
