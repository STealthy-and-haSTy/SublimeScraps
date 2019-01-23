#!/bin/env python3
"""
Load the Session.sublime_session file from either the Sublime Text 3 or Sublime
Merge data directory and remove all of the recent workspaces/git repositories
that  refer to items that no longer reside on disk.

If no data directory is provided on the command line, the script will look for
the session file in the data directory location standard for the appropriate
application on the current platform.

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


_data_dirs = {
    "text": {
        "linux": "~/.config/sublime-text-3/",
        "win": "$APPDATA\\Sublime Text 3\\",
        "osx": "~/Library/Application Support/Sublime Text 3/"
    },

    "merge": {
        "linux": "~/.config/sublime-merge/",
        "win": "$APPDATA\\Sublime Merge\\",
        "osx": "~/Library/Application Support/Sublime Merge/"
    }
}


def sublime_data_dir(prog):
    """
    Obtain the path to the Sublime Data directory for the given program in a
    platform independent way. This doesn't work for portable installs however.
    """
    if sys.platform.startswith("linux"):
        return os.path.expanduser(_data_dirs[prog]["linux"])
    elif sys.platform.startswith("win"):
        return os.path.expandvars(_data_dirs[prog]["win"])

    return os.path.expanduser(_data_dirs[prog]["osx"])


def load_session(file_name, program):
    """
    Load and parse the Sublime session file provided, returning back a tuple
    containing the overall session file and the recent items. The tuple
    contains None if there are errors loading or parsing the session file.
    """
    try:
        with open(file_name, encoding="utf-8") as file:
            session = json.load(file)

            items = (session["recent"] if program == "merge"
                else session["workspaces"]["recent_workspaces"])
            return (session, items)

    except FileNotFoundError:
        logging.exception("Unable to locate session file")

    except ValueError:
        logging.exception("Session file could not be parsed; invalid JSON?")

    except KeyError:
        logging.exception("Session file could not be parsed; invalid format?")

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


def item_path(item, program):
    """
    More recent versions of Sublime Merge use a recent list that contains state
    for the repository instead of just a path; this determines, based on an
    item and the program in use, what the path inside it is.
    """
    if program == "merge" and isinstance(item, dict):
        return item.get("path")

    return item


def item_exists(item, program):
    """
    Given a path that represents a workspace or repository item (based on
    program), return a determination as to whether that item is still valid or
    not.
    """
    path = item_path(item, program)

    if sys.platform.startswith("win") and not path.startswith("//"):
        # On Windows, Sublime stores local paths as '/drive/path/file/', which
        # Python doesn't recognize as valid, so we need to rewrite them. UNC
        # paths work OK (presuming the network is up to it).
        path = "{drive}:{path}".format(
            drive=path[1],
            path=path[2:])

    return os.path.isdir(path) if program == "merge" else os.path.isfile(path)


def clean_session(data_dir, program, dry_run):
    """
    Load the session file from the data directory for the specified program and
    remove all of the projects/repositories that no longer exist on disk,
    writing the session back.

    This attempts to keep a backup of the existing session file and creates a
    temporary session first in case things go pear shaped.
    """
    session_file = os.path.join(data_dir, "Local", "Session.sublime_session")
    tmp_file = session_file + ".tmp"
    bkp_file = session_file + datetime.now().strftime(".%Y%m%d_%H%M%S")

    logging.info("Using Data Directory: %s", data_dir)
    session, check_items = load_session(session_file, program)
    if session is not None:
        present, missing = [], []
        for item in check_items:
            status_list = present if item_exists(item, program) else missing
            status_list.append(item)

        if len(present) != len(check_items):
            logging.info("Expunging defunct items:")
            for item in missing:
                logging.info("  %s", item_path(item, program))
            logging.info("Expunged %d item(s)", len(missing))

            if dry_run:
                return

            check_items[:] = present

            tmp_file = save_session(session_file, session)
            if tmp_file is not None:
                try:
                    os.rename(session_file, bkp_file)
                    os.rename(tmp_file, session_file)

                    logging.info("New session file saved")

                except OSError:
                    logging.exception("Error replacing session file")

        else:
            logging.info("No missing items found")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--program",
                        help="Specify the program to clean [Default: text]",
                        choices=["text", "merge"],
                        default="text")
    parser.add_argument("-d", "--data-dir",
                        help="Specify the Sublime Data directory to use")
    parser.add_argument("--dry-run",
                        help="Run clean but don't write the new session file",
                        action="store_true")

    args = parser.parse_args()

    # Need to set the default last so it can pick up the program
    args.data_dir = args.data_dir or sublime_data_dir(args.program)

    clean_session(args.data_dir, args.program, args.dry_run)
