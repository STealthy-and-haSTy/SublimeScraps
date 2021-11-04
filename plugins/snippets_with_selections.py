import sublime
import sublime_plugin

# Related Reading:
#     https://forum.sublimetext.com/t/parse-two-selected-lines-in-html-tags/56162

# This plugin implementd a version of the insert_snippet command that provides
# access to each individual selection as numbered variables, such as
# SELECTION_1, SELECTION_2, and so on. This allows an expansion to include
# multuple selections in the replacement.

class InsertSnippetWithSelectionsCommand(sublime_plugin.TextCommand):
    """
    Since the normal "insert_snippet" command would insert contents in all
    selections, this version "joins" all of the current selections into a
    single selection first.
    """
    def run(self, edit, **kwargs):
        sel = self.view.sel()
        for idx in range(len(sel)):
            kwargs["SELECTION_%d" % (idx + 1)] = self.view.substr(sel[idx])

        self.view.sel().add(sublime.Region(sel[0].begin(), sel[-1].end()))
        self.view.run_command("insert_snippet", kwargs)

