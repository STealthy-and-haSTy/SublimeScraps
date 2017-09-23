import sublime
import sublime_plugin

# Related reading:
#     https://forum.sublimetext.com/t/command-to-move-by-several-lines/28508
#     https://stackoverflow.com/questions/46369685/sublime-how-can-i-jump-n-lines-with-the-keyboard-arrows/

# A couple of users were interested in making the built in move command for
# moving the cursor around be able to take the same action a number of times
# instead of just once.

# This creates a drop in replacement for the standard move command named
# move_amount that takes the same arguments as move does, plus an extra argument
# named amount for specifying how many times to take the action which defaults
# to 1.

# With this in place you can modify or duplicate existing motion key binds and
# replace the command to get multiple motions easily.
class MoveAmountCommand(sublime_plugin.TextCommand):
    def run(self, edit, amount=1, **kwargs):
        for _ in range(amount):
            self.view.run_command("move", args=kwargs)
