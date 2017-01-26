import sublime
import sublime_plugin
import re

# Related reading;
#     http://stackoverflow.com/questions/40519960/sublime-3-selecting-text-without-line-numbers-from-find-all-results

# I consider this a great example of being able to extend Sublime to allow you
# to work the way you want to. In this case, someone wanted to be able to copy
# entire lines out of the Find in Files results without capturing the line
# numbers that tell you where in the file the result came from.

# In use, you might use a key binding such as the following. This uses the
# context mechanism to re-use the same key that is normally used for a copy
# operation to be this command only while inside of find results, so that
# everything is more intuitive.
#
# {"keys": ["ctrl+c"], "command": "find_results_copy", "context":
#     [
#         { "key": "selector",
#           "operator": "equal",
#           "operand": "text.find-in-files",
#           "match_all": true
#         },
#     ]
# }

class FindResultsCopyCommand(sublime_plugin.ApplicationCommand):
    """
    Provide a version of the standard copy command which can copy data out of
    a Find in Files result buffer without capturing the line numbers that appear
    in the output.
    """
    def run(self):
        sublime.active_window ().run_command ("copy")
        sublime.set_clipboard (re.sub (r"^\s*[0-9]+.", "",
            sublime.get_clipboard (), flags=re.MULTILINE))