import sublime
import sublime_plugin

# Related Reading:
#     https://forum.sublimetext.com/t/find-for-a-macro/57387/
#
# This example command allows you to jump the cursor to the next or previous
# location of a given pattern of text, which can be either a regex or not and
# case sensitive or not based on command arguments.
#
# A use case for this is implementing a specific Find operation in a macro in
# a repeatable way.


class PatternNavigateCommand(sublime_plugin.TextCommand):
    """
    Jump the selection in the file to the next or previous location of the
    given textual pattern based on the current cursor location. The search
    direction is controlled by the forward argument, and will wrap around the
    ends of the buffer.
    """
    def run(self, edit, pattern, literal=True, ignorecase=False, forward=True):
        # Convert the incoming arguments to the appropriate search flags.
        flags = ((sublime.LITERAL if literal else 0) |
                 (sublime.IGNORECASE if ignorecase else 0))

        # Find the locations where this pattern occurs; leave if none
        regions = self.view.find_all(pattern, flags)
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

