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
    "BootstrapTestListener"
]


### ---------------------------------------------------------------------------


class BootstrapTestListener(sublime_plugin.EventListener):
    """
    Display a message in the console every time someone saves a file. Like the
    test command above, this verifies that the bootstrapped package is
    successfully exposing the event listener.
    """
    def on_post_save(self, view):
        print("Something just got saved and you probably don't care")


### ---------------------------------------------------------------------------
