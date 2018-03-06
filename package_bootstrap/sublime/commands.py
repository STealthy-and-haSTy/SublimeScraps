"""
This file is an example of some Sublime specific plugin code that is contained
within the dependency but later exposed via the bootstrapped system package.

In use this could be one or more files with a variety of commands and event
listeners. The examples here do nothing but generate log messages.

Note that this code is contained wholly within the dependency and the
bootstrapped package will reference it from there.
"""


import sublime
import sublime_plugin


### ---------------------------------------------------------------------------


__all__ = [
    "BootstrapTestCommand",
]


### ---------------------------------------------------------------------------


class BootstrapTestCommand(sublime_plugin.TextCommand):
    """
    Display a message to the console to verify that the command has been
    executed. This is here to verify that the bootstrapped package is
    successfully exposing the command.
    """
    def run(self, edit):
        print("I appear to be some sort of example command")


### ---------------------------------------------------------------------------
