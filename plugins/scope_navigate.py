import sublime
import sublime_plugin

# Related Reading:
#     https://forum.sublimetext.com/t/keybinding-to-find-a-particular-set-of-characters/49064
#
# This command allows you to easily jump the cursor to the next or previous
# location of a specific "scope" in the file. This is a bit more advanced as a
# navigation method, but would allow you to for example create a key binding
# that always jumps between comments in files, even when switching languages.
#
# Use 'Tools > Developer > Show Scope Name' to determine the scope to use here.


class ScopeNavigateCommand(sublime_plugin.TextCommand):
    """
    Jump the selection in the file to the next or previous location of the
    given scope based on the current cursor location. The search direction is
    controlled by the forward argument, and will wrap around the ends of the
    buffer.
    """
    def run(self, edit, scope, forward=True):
        # Find the locations where this scope occurs; leave if none
        regions = self.view.find_by_selector(scope)
        if not regions:
            return

        # Get a starting point for our search, and where we should jump to if
        # there are no matches in the specified direction.
        point = self.view.sel()[0].b
        fallback = regions[-1] if not forward else regions[0]

        # Remove all selections.
        self.view.sel().clear()

        # Look in the given direction for the first match from the current
        # position; if one is found jump there.
        pick = lambda p: (point < p.a) if forward else (point > p.a)
        for pos in regions if forward else reversed(regions):
            if pick(pos):
                return self.jump(pos.a)

        # No matches in the search direction, so wrap around.
        self.jump(fallback.a)

    def jump(self, point):
        # Add in the given position as a selection and ensure that it's
        # visible.
        self.view.sel().add(sublime.Region(point))
        self.view.show(point, True)

