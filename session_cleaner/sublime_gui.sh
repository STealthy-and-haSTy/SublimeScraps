#!/bin/bash

# If sublime is not running, check if we should clean the session
if ! pgrep -x subl > /dev/null
then
    sublime_session_clean.py
fi

# Run with our arguments
subl $*
