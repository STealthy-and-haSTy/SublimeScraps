import sublime
import sublime_plugin

from bisect import bisect_left

# This plugin was created for someone grumpy on the forum who never came back
# to collect the answer, but this could be useful anyway.
#
# This implements an insert_to_column command that will insert whitespace at
# every cursor that exists to move the cursor to the column specified. When
# this is 0, the next closest ruler is used, with column 72 being a fallback
# if there are no rulers that match.
#
# This could be used to add whitespace to the ends of lines, such as to align
# comments or tables.

class InsertToColumnCommand(sublime_plugin.TextCommand):
    """
    Insert spaces at every selection in order to move the cursor
    to the given column, or the next ruler, or column 72.

    Cursors that are already at or past the destination don't
    move.

    This requires all selections to be empty so that we don't
    clobber any selected text.
    """
    def run(self, edit, col=0):
        rulers = sorted(self.view.settings().get('rulers', []))

        for sel in self.view.sel():
            caret = self.view.rowcol(sel.a)[1]
            col = col or self.find_next_ruler(caret, rulers)
            spaces = col - caret
            if spaces > 0:
                self.view.insert(edit, sel.a, spaces * " ")

    def find_next_ruler(self, caret, rulers):
        if rulers:
            pos = bisect_left(rulers, caret)
            if pos == len(rulers) - 1:
                return caret

            return rulers[pos] if rulers[pos] != caret else rulers[pos + 1]

        return 72

    def is_enabled(self, col=0):
        return all(s.empty() for s in self.view.sel())


