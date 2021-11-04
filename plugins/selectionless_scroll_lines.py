import sublime
import sublime_plugin

# This implements a selectionless_scroll_lines command that is a drop in
# replacement for the scroll_lines command that is in the Sublime core; it
# does the same thing but scrolls the view without changing the location of
# the cursors as the built in command does.
#
# The following key bindings show how to use it (they overwrite the built in
# key bindings on the built in command, blocking them from being used via the
# keyboard).

# { "keys": ["ctrl+up"], "command": "selectionless_scroll_lines", "args": {"amount": 1.0 } },
# { "keys": ["ctrl+down"], "command": "selectionless_scroll_lines", "args": {"amount": -1.0 } },

class SelectionlessScrollLinesCommand(sublime_plugin.TextCommand):
    """
    Scroll the view into the file up or down by the amount provided, leaving
    the cursors in their current location.
    """
    def run(self, edit, amount=1.0):
        height = self.view.line_height()
        x,y = self.view.viewport_position()
        self.view.set_viewport_position((x, y + (height * -amount)))
