#!/usr/bin/env python3
"""
Load the Session.sublime_session file from either the Sublime Text or Sublime
Merge data directory and perform a cleanup operation to remove all of the
recent workspaces, folders/git repositories, and files that are in the list of
recently accessed items if they no longer exist on disk. The items cleaned up
are controlled by command line arguments.

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

            if program == "text":
                items = session["workspaces"]["recent_workspaces"]
                folders = session["folder_history"]
                files = [w["file_history"] for w in session["windows"] ]
                files.append(session["settings"]["new_window_settings"]["file_history"])
            else:
                items = session["recent"]
                folders = None
                files = None

            return (session, items, folders, files)

    except FileNotFoundError:
        logging.exception("Unable to locate session file")

    except ValueError:
        logging.exception("Session file could not be parsed; invalid JSON?")

    except KeyError:
        logging.exception("Session file could not be parsed; invalid format?")

    return (None, None, None, None)


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

    Some code invokes this with a program of "merge" when it knows that it
    wants to check for folders and not files, as a mild hack.
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


def clean_items(checked_items, program, item_name):
    """
    Given a list of items to check (workspace files, folders, git repositories,
    files, etc), modify the list such that any items that no longer exist are
    removed from the list on return. The list is modified in place.

    The check done is based on the program doing the check and the item itself.
    """
    if checked_items is None:
        print("No items; doing nothing")
        return False

    present, missing = [], []
    for item in checked_items:
        status_list = present if item_exists(item, program) else missing
        status_list.append(item)

    if len(present) != len(checked_items):
        logging.info("Cleaning up %s:" % item_name)
        for item in missing:
            logging.info("  %s", item_path(item, program))
        logging.info("Cleaned %d item(s)\n", len(missing))

        checked_items[:] = present
        return True

    return False


def clean_session(args):
    """
    Load the session file from the data directory for the specified program and
    perform the requested clean up operations to remove items that are marked
    as recent but which no longer exist on disk, writing the session back.

    This attempts to keep a backup of the existing session file and creates a
    temporary session first in case things go pear shaped.
    """
    session_file = os.path.join(args.data_dir, "Local", "Session.sublime_session")
    tmp_file = session_file + ".tmp"
    bkp_file = session_file + datetime.now().strftime(".%Y%m%d_%H%M%S")

    logging.info("Using Data Directory: %s", args.data_dir)
    if args.dry_run:
        logging.info("--- PERFORMING DRY RUN: No Actions will be taken! ---")

    session, check_items, check_folders, check_files = load_session(session_file, args.program)
    if session is not None:
        check1 = check2 = check3 = False

        if args.workspaces:
            item_type = "recent %s" % ("workspaces" if args.program == "text" else "repositories")
            check1 = clean_items(check_items, args.program, item_type)

        if args.folders and check_folders:
            # Force the program to be merge because merge handles folders for us
            # transparently, and it doesn't support the notion of recent folders
            # anyway.
            check2 = clean_items(check_folders, "merge", "recent folders")

        if args.files and check_files:
            for file_list in check_files:
                check3 = clean_items(file_list, args.program, "recent files") or check3

        if any((check1, check2, check3)):
            if args.dry_run:
                logging.info("--- PERFORMING DRY RUN: Session WILL NOT be modified ---")
                return

            tmp_file = save_session(session_file, session)
            if tmp_file is not None:
                try:
                    os.rename(session_file, bkp_file)
                    os.rename(tmp_file, session_file)

                    logging.info("New session file saved")
                    logging.info("Previous session backed up to: DATA_DIR%s%s" % (
                        os.path.sep,
                        os.path.relpath(bkp_file, args.data_dir)))

                except OSError:
                    logging.exception("Error replacing session file")

        else:
            logging.info("Nothing found to clean up")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)


    parser = argparse.ArgumentParser(description="Clean Sublime Text/Merge session files",
                                     epilog="At least one cleanup action must be selected",
                                     prefix_chars="-+")
    parser.add_argument("--program", "-p",
                        help="Specify the program to clean [Default: text]",
                        choices=["text", "merge"],
                        default="text")
    parser.add_argument("--data-dir", "-d",
                        help="Specify the Sublime Data directory to use")

    parser.add_argument("--dry-run",
                        help="Run clean but don't write the new session file",
                        action="store_true")

    actions = parser.add_argument_group("Available Cleanup Actions")

    actions.add_argument("--workspaces", "-w",
                        help="Clean up recently used workspaces, projects and repositories",
                        action="store_true")

    actions.add_argument("--files", "-f",
                        help="Clean up recently used files",
                        action="store_true")

    actions.add_argument("--folders", "-o",
                        help="Clean up recently used folders [Default: False]",
                        action="store_true")

    args = parser.parse_args()
    if not any([args.workspaces, args.files, args.folders]):
        parser.error("You must specify at least one cleanup option")

    # Need to set the default data_dir last so it can pick up the program.
    args.data_dir = args.data_dir or sublime_data_dir(args.program)

    clean_session(args)
