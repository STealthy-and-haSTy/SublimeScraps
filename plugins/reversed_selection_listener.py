import sublime
import sublime_plugin

# Related reading:
#   https://discord.com/channels/280102180189634562/280102180189634562/958470369767997500
#
# This plugin provides a custom key binding context named reversed_selection
# which can be used to create key bindings that trigger only when the selection
# is "normal" (cursor on the right) or reversed (cursor on the left).
#
# An example of this in use is the following key binding, which will echo an
# empty dictionary to the console if the key is pressed and all selections are
# reversed.
#
# { "keys": ["ctrl+alt+c"], "command": "echo",
#   "context": [
#     { "key": "reversed_selection", "operator": "equal", "operand": true, "match_all": true, },
#    ]
# },

class ReverseSelectionListener(sublime_plugin.EventListener):
    """
    This event listener listens for a key context named reversed_selection and
    will return True or False depending on whether the selection is selected in
    a reverse manner or not. match_all is also supported, to allow the context
    to work across multiple cursors.
    """
    def on_query_context(self, view, key, operator, operand, match_all):
        if key != "reversed_selection":
            return None

        lhs = operand
        if match_all:
            rhs = all([r.a > r.b for r in view.sel()])
        else:
            rhs = view.sel()[0].a > view.sel()[0].b

        return True if operator == sublime.OP_EQUAL and rhs == lhs else False
