import sublime
import sublime_plugin

# Related reading:
#     https://stackoverflow.com/questions/46167234/sublimetext-3-dynamically-enable-disable-invisible-white-space-option/

# This implements an extended version of the internal toggle_setting command.
# Where that command can toggle a boolean setting between True and False, this
# version can toggle any setting between any values, even two or more.
#
# This was originally written as an example for someone that wanted to toggle
# the display of visible white space on and off. The version here is extended
# and made more generic by allowing not only the list of options to toggle
# between, but also the setting to use.
#
# The command takes an argument that specifies the setting to toggle as well as
# a list of the values to toggle between, which can be two or more values that
# are valid for the setting in question.
#
# When the setting is not already set for the current view, or the current
# setting is not in the list of options given, the first item in the list is
# used as the setting. Otherwise, the value of the setting is set to the next
# item in the list.

# Examples:
#
# // Toggle between all white space display options
# {
#    "keys": ["super+s"], "command": "toggle_setting_ext",
#    "args": {
#       "setting": "draw_white_space"
#       "options": ["all", "selection", "none"]
#    }
# },
#
#
# // Swap between two sets of rulers for the current view
# {
#    "keys": ["super+s"], "command": "toggle_setting_ext",
#    "args": {
#       "setting": "rulers"
#       "options": [[80, 110], [40, 55]]
#    }
# },
#
# // Standard: Toggle word wrap on or off
# {
#    "keys": ["super+s"], "command": "toggle_setting_ext",
#    "args": {
#       "setting": "word_wrap"
#       "options": [True, False]
#    }
# },

class ToggleSettingExt(sublime_plugin.TextCommand):
    """
    An extended version of the toggle_setting internal command. Along with a
    setting, provide a list of options to toggle between, which can contain
    more than two items if the setting can have more than two values.
    (e.g. the draw_white_space option)
    """
    def run(self, edit, setting, options):
        try:
            current = self.view.settings().get(setting)
            index = -1 if current is None else options.index(current)
        except:
            return self.view.settings().set(setting, options[0])

        index = (index + 1) % len(options)
        self.view.settings().set(setting, options[index])