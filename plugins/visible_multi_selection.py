import sublime
import sublime_plugin

import functools

# Related reading:
#     https://forum.sublimetext.com/t/difference-when-multiple-selection/58087
#
# This simple plugin makes it easier to visualize when there is more than one
# cursor active in the current file (particularly when one or more of them may
# be outside the visible area of the file) by changing the state of the cursor.
#
# In this example the cursor is made wider when there is more than one, but
# this could be customized to use any number of settings.


class GiantCursorEventListener(sublime_plugin.ViewEventListener):
    pending = 0

    def on_selection_modified_async(self):
        self.pending += 1
        sublime.set_timeout_async(functools.partial(self.update_cursor), 500)

    def update_cursor(self):
        self.pending -= 1
        if self.pending != 0:
            return

        s = self.view.settings()

        # Count of selections now and the last time we were triggered. If they
        # are the same, leave.
        now = len(self.view.sel())
        then = s.get('_sel_count', -1)

        if now == then:
            return

        # Remove the setting on 1 selection, otherwise increase it.
        # Save this selection count, then erase or add the setting.
        s.set('_sel_count', now)
        if now == 1:
            s.erase("caret_extra_width")
        else:
            s.set("caret_extra_width", 4)
