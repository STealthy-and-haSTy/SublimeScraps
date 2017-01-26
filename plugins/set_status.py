import sublime, sublime_plugin

# Related reading:
#     http://stackoverflow.com/questions/39373728/how-to-change-the-sublime-text-3-statusbar-message-in-a-command-or-macro-no-plu

# This is a simple command that adds a bit of text to the status line which
# automatically vanishes after a few seconds.
#
# This is dirt simplem but someone wanted to be able to display some status text
# in the middle of a Macro operation, and this is the easiest way to do that
class SetStatusCommand(sublime_plugin.TextCommand):
    """
    Add a temporary status string to the status bar.
    """
    def run(self, edit, value="set_status: use arg 'value' to set text"):
        self.view.window ().status_message (value)