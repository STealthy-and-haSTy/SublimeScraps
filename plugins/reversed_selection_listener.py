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
        # If this is not the key that we understand, defer to another listener.
        if key != "reversed_selection":
            return None

        # If the operator is not equal, flip the state of the operand to make
        # it match what OP_EQUAL would do.
        if operator == sublime.OP_NOT_EQUAL:
            operand = not operand

        # Test each selection for being either forward (operand == true) or
        # backwards (operand == false), since that controls what we're testing
        # for. The array must always contain True where the requested condition
        # matches.
        sels = ([r.a > r.b for r in view.sel()] if operand
                       else [r.a < r.b for r in view.sel()])

        # Either all values must be True, or just one, depending on the state
        # of the given match_all argument.
        criteria = all(sels) if match_all else any(sels)

        # Criteria is now True when the condition matches the request and False
        # when it does not. Our return is whether the actual result matches the
        # desired outcome.
        return criteria
