import sublime
import sublime_plugin
import time

# Related Reading:
#     https://forum.sublimetext.com/t/automatically-updated-timestamp/7156
#
# This is a simple plugin for people that like to have a last edited timestamp
# directly inside their files. It implements a command that will find such a
# timestamp based on a header and then update it with the current time. The
# header to look for and the date format are user customizable.
#
# The event listener will apply the command on every save, making this seamless
# as an operation. If you would rather do this manually, remove or comment out
# the event handler class and you can bind the command to a key instead.
#
# This example binding uses the chain command built into Sublime Text 4 to
# execute first this command, then the save command.

# { "keys": ["super+t"], "command": "chain",
#    "args": {
#       "commands": [
#          {"command": "update_last_edited_date"},
#          {"command": "save"},
#       ]
#    }
# },

class UpdateLastEditedDateCommand(sublime_plugin.TextCommand):
    """
    Check the current file for the first line that contains the provided
    header, and if found update it to include the current date and time
    as formatted by the given date format.
    """
    def run(self, edit, header="Last Edited: ", format="%d %b %Y %I:%M%p"):
        span = self.view.find(f'{header}.*$', 0)
        if span is not None:
            self.view.replace(edit, span, f"{header}{time.strftime(format)}")


class UpdateLastSavedEvent(sublime_plugin.EventListener):
    """
    Update the last edited time in a file every time it's saved.
    """
    def on_pre_save(self, view):
        view.run_command('update_last_edited_date')

