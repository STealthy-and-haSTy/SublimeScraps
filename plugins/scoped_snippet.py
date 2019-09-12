import sublime
import sublime_plugin

# A snippet file can contain a scope to constrain when it will expand via the
# tab trigger and appear in the command palette, but the insert_snippet command
# will always insert the snippet regardless of scope. When bound to a key you
# can use a context to also constrain the snippet, but this isn't possible in
# the command palette or a menu item.
#
# This plugin implements a wrapper on that command for enabling this in those
# locations. It lets you specify a scope to match (and whether it should match
# all cursors or not) and will only enable itself in the appropriate scope.

class InsertScopedSnippetCommand(sublime_plugin.TextCommand):
    """
    Drop in replacement for the insert_snippet command that will only insert
    the snippet when the scope at the cursor location matches the scope
    provided (if any). match_all controls whether the scope must match at all
    cursor locations or just some of them.
    """
    def run(self, edit, scope=None, match_all=True, **kwargs):
        self.view.run_command("insert_snippet", kwargs)

    def is_enabled(self, scope=None, match_all=True, **kwargs):
        if scope is None:
            return True

        match = [self.view.match_selector(s.b, scope) for s in self.view.sel()]
        return all(match) if match_all else any(match)
