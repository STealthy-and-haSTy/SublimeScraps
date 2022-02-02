import sublime
import sublime_plugin

# This implements a command named "clear_console" that will clear the contents
# of the Sublime Text console. This will only work in Sublime Text 4.
#
# You can create a key binding on this such as the following (the context makes
# it only apply while the console has the focus):
#
# { "keys": ["super+t"], "command": "clear_console",
#   "context": [
#       { "key": "panel", "operand": "console" },
#       { "key": "panel_has_focus"  }
#   ]
# },
#
# Alternately, you can create a file named "Widget Context.sublime-menu" in
# your User package to add a context menu item that you can use in the console
# body as well:
#
# [
#     { "caption": "-" },
#     { "command": "clear_console" },
# ]
#


class ClearConsoleCommand(sublime_plugin.ApplicationCommand):
    """
    Clear out the Sublime console by temporarily setting the scroll back length
    to a single line and outputting a line, causing the history to be dropped.
    """
    def run(self):
        s = sublime.load_settings('Preferences.sublime-settings')
        scrollback = s.get('console_max_history_lines')
        s.set('console_max_history_lines', 1)
        print("")
        s.set('console_max_history_lines', scrollback)
