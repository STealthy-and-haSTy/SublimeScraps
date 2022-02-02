import sublime
import sublime_plugin

# This is a simple example of implementing a custom key binding context using
# an event listener listening for on_query_context.
#
# In this example we provide a custom key context named last_line which is a
# boolean context that can tell you if one or all of the selections have
# their cursor positioned in the last line of the file.
#
# This example key binding shows how to use this; the echo command will only
# display output in the console if the cursor is in the last line of the file.
#
#    { "keys": ["ctrl+shift+h"], "command": "echo",
#      "args": {"message": "This is the last line of the file"},
#      "context": [
#        { "key": "last_line", "operator": "equal", "operand": true },
#      ],
#    },


class EndOfFileContextListener(sublime_plugin.EventListener):
    """
    Check if one or all selections have their cursor positioned in the last
    line of the file.
    """
    def on_query_context(self, view, key, operator, operand, match_all):
        # If this isn't the key context we know about, pass through to let
        # Sublime ask another context.
        if key != "last_line":
            return None

        # Get a region that represents the last line in the view, and the
        # character offset that represents the end of the file.
        last_line = view.line(len(view))

        # Check to see which of the selections is contained in the last line.
        #
        # NOTE: the whole selection must appear inside the last line for this
        # to match; a selection that is only partially in the last line is
        # not contained in the last line.
        sels = (last_line.contains(s) for s in view.sel())

        # Depending on match_all, indicate if one or all selections are on
        # the last line
        lhs = all(sels) if match_all else any(sels)

        # Return if they're equal or not
        return lhs == operand if operator == sublime.OP_EQUAL else lhs != operand
