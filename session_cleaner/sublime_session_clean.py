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

import argparse
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


def load_session(file_name):
    """
    Load and parse the Sublime session file provided, returning back a tuple
    containing the overall session file and the recent workspaces. The tuple
    contains None if there are errors loading or parsing the session file.
    """
    try:
        with open(file_name, encoding="utf-8") as file:
            session = json.load(file)
            return (session, session["workspaces"]["recent_workspaces"])

    except FileNotFoundError:
        logging.exception("Unable to locate session file")

    except ValueError:
        logging.exception("Session file could not be parsed; invalid JSON?")

    except KeyError:
        logging.exception("No workspaces key found in session file")

    return (None, None)


def save_session(file_name, session):
    """
    Save the session dictionary back to disk in the appropriate folder using
    a temporary name. The name of the file is returned if the new session is
    successfully saved.
    """
    file_name = file_name + ".tmp"
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(session, file,
                      indent="\t",
                      ensure_ascii=False,
                      sort_keys=True,
                      separators=(',', ': '))
            return file_name

    except TypeError:
        logging.exception("Session file contains non-basic data")

    except OSError:
        logging.exception("Error saving new session file")

    return None


def workspace_exists(file_name):
    """
    Given a file name that represents a Sublime project or workspace, return a
    determination as to whether that project is still valid or not.
    """
    if sys.platform.startswith("win") and not file_name.startswith("//"):
        # On Windows, Sublime stores local paths as '/drive/path/file/', which
        # Python doesn't recognize as valid, so we need to rewrite them. UNC
        # paths work OK (presuming the network is up to it).
        file_name = "{drive}:{path}".format(
            drive=file_name[1],
            path=file_name[2:])

    return os.path.isfile(file_name)


def clean_session(data_dir, dry_run):
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
    session, workspaces = load_session(session_file)
    if session is not None:
        present, missing = [], []
        for file in workspaces:
            status_list = present if workspace_exists(file) else missing
            status_list.append(file)

        if len(present) != len(workspaces):
            logging.info("Expunging defunct workspaces:")
            for file in missing:
                logging.info("  %s", file)
            logging.info("Expunged %d workspace(s)", len(missing))

            if dry_run:
                return

            workspaces[:] = present

            tmp_file = save_session(session_file, session)
            if tmp_file is not None:
                try:
                    os.rename(session_file, bkp_file)
                    os.rename(tmp_file, session_file)

                    logging.info("New session file saved")

                except OSError:
                    logging.exception("Error replacing session file")

        else:
            logging.info("No missing projects found")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-dir",
                        help="Specify the Sublime Data directory to use",
                        default=sublime_data_dir())
    parser.add_argument("--dry-run",
                        help="Run clean but don't write the new session file",
                        action="store_true")

    args = parser.parse_args()

    clean_session(args.data_dir, args.dry_run)
