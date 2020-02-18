#!/usr/bin/env bash

#
# This is meant to be invoked from the task bar or a launcher in order to start
# Sublime; any arguments passed to the script are passed to Sublime when it's
# launched.
#
# A check is done prior to the launch to see if Sublime is currently running or
# not. If it's not, then a check is done to see if there are any defunct
# projects in the session that can be cleaned up.
#
# Once the check (if any) is complete, Sublime is launched.
#
# Additionally, if Sublime was already running, -n is added to the list of
# arguments so that running the script while Sublime is already running creates
# a new window.
#
# Regardless, Sublime is started and passed all of the arguments the script
# received.

#
# Check to see if Sublime is running or not.
#
if ! pgrep -x sublime_text > /dev/null
then
    #
    # Sublime is not running, so run a check to clean the session and then
    # start Sublime with the arguments we were given.
    #
    sublime_session_clean.py -p text --workspaces --files --folders
    sublime_text $*
else
    #
    # Sublime is currently running. In that case execute with the arguments
    # that we were given, but also include -n so that a new window is created.
    #
    sublime_text -n $*
fi

