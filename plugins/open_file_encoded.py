import sublime
import sublime_plugin

# Related reading;
#     https://stackoverflow.com/questions/56611586/open-file-at-specific-line-number-using-open-file-command
#     https://forum.sublimetext.com/t/open-file-at-specific-line-number-using-open-file-command/41928

# The open_file command from core Sublime can be used in key bindings, menu
# entries the command palette or even from plugins to open files. From the
# command line, Sublime allows you to optionally encode a position to open the
# file at via adding :line or :line:col to the end of the file name.
#
# Unfortunately, the open_file command does not support this, but this drop in
# replacement does. Using it, you can easily open files at exact locations if
# desired.
#
# There is also a similar plugin available in the forum thread linked above
# which adds similar functionality but uses a different mechanism for
# specifying the line and column information.

import sublime
import sublime_plugin


class OpenFileEncodedCommand(sublime_plugin.WindowCommand):
    """
    A simple drop in replacement for the open_file command that allows file
    names with a :row or row:col position encoded at the end for opening files
    at a specific location.
    """
    def run(self, file):
        self.window.open_file(file, sublime.ENCODED_POSITION)
