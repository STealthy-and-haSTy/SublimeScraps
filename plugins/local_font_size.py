import sublime
import sublime_plugin


# Related reading;
#     https://forum.sublimetext.com/t/setting-different-font-sizes-for-different-tabs-files/15685?
#
# This plugin implements versions of the commands that increase, decrease and
# reset the font size in Sublime, but here they apply only to the current file.
# Using this you could have different font sizes in different tabs as desired.
#
# To use these commands, set up key bindings similar to the following:
#
# { "keys": ["alt+ctrl+="], "command": "increase_local_font_size" },
# { "keys": ["alt+ctrl+-"], "command": "decrease_local_font_size" },
# { "keys": ["alt+ctrl+0"], "command": "reset_local_font_size" },
#
# The toggle_setting_ex.py plugin also available in this repository provides
# another way to do a similar action, in that case swapping between a set of
# known font sizes.


class IncreaseLocalFontSizeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        current = self.view.settings().get("font_size", 10)

        if current >= 36:
            current += 4
        elif current >= 24:
            current += 2
        else:
            current += 1

        if current > 128:
            current = 128

        self.view.settings().set("font_size", current)


class DecreaseLocalFontSizeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        current = self.view.settings().get("font_size", 10)

        if current >= 40:
            current -= 4
        elif current >= 26:
            current -= 2
        else:
            current -= 1

        if current < 8:
            current = 8

        self.view.settings().set("font_size", current)


class ResetLocalFontSizeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.settings().erase("font_size")
