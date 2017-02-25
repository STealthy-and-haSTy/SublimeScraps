import sublime
import sublime_plugin

# The sublime plugin API includes a method for showing a quick panel, which
# allows you to select from a list of items while doing some optional filtering
# if desired using the same fuzzy matching as you can in the command palette.
#
# This file shows an example of using a quick panel to select an item from a
# (potentially) hierarchical list, allowing for seamlessly traversing the
# hierarchy of items in both directions.
#
# The command here takes a list of dictionaries that describe the items to be
# selected. Each dictionary must contain a "caption" key to provide the text
# that is to be displayed in the list, and may also optionally contain a
# "children" key which, if present is a list of similar dictionaries for the
# items below this item in the hierarchy.
#
# The "caption" key may have a value that is a single string or a list of
# strings. In the latter case, the quick list will contain multiple lines for
# each entry.
#
# The command takes an optional argument of "prior_text", which defaults to ".."
# if not given and which represents the text displayed to allow the user to go
# back up the list of selected items.

# It's important to note that if you use a "caption" key in your list items
# which contains a list of strings (i.e. a multi-line entry), you must specify a
# similar list for "prior_text" as well or Sublime will throw an error. In
# practice you could fix this situation programmaticly but this is just an
# example.
#
# When an item with children is selected from the list, the list will
# automatically open to show those child nodes, along with an option to go back
# up the hierarchy.
#
# In use your code would do something more useful than print the item that was
# selected, such as running a command or some such.
#
# An example of this command in action can be achieved using the following key
# binding (change the key in the binding to something appropriate for your
# situation).
#
# {
#     "keys": ["ctrl+alt+shift+t"],
#     "command": "nested_quick_panel",
#     "args": {
#         "items": [
#             { "caption": "Level 1, Item 1" },
#             { "caption": "Level 1, Item 2" },
#             { "caption": "Level 1, Item 3",
#               "children": [
#                     { "caption": "Level 2, Item 1" },
#                     { "caption": "Level 2, Item 2",
#                        "children": [
#                             {"caption": "Level 3, Item 1"}
#                         ]
#                     }
#                 ]
#             }
#         ]
#     }
# }

class NestedQuickPanelCommand(sublime_plugin.WindowCommand):
    """
    This is an example of using a quick_panel to navigate through a list of
    entries, allowing for some entries to contain sub lists.

    The run method expects a list of dictionaries which each have a "caption"
    key to determine what shows in the list and an optional "children" key
    which, if it exists, has a value that is an array of dictionaries.
    """
    def select_item(self, items, prior_text, stack, index):
        if index >= 0:
            # When stack is not empty, first item takes us back
            if index == 0 and len(stack) > 0:
                items = stack.pop()
                return self.display_panel(items, stack)

            # Compensate for the "prior_text" entry on a non-empty stack
            if len(stack) > 0:
                index -= 1

            entry = items[index]
            children = entry.get("children", None)

            if children is not None:
                stack.append(items)
                return self.display_panel(children, prior_text, stack)

            print("Selected item %d (%s)" % (index, entry))

    def display_panel(self, items, prior_text, stack):
        captions = [item["caption"] for item in items]
        if len(stack) > 0:
            captions.insert(0, prior_text)

        self.window.show_quick_panel(
            captions,
            on_select=lambda index: self.select_item(items, prior_text, stack, index))

    def run(self, items, prior_text=".."):
        self.display_panel(items, prior_text, [])
