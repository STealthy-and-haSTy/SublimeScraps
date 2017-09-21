import sublime
import sublime_plugin
import textwrap

# related reading: https://stackoverflow.com/a/46315431/4473405


class WrapTextCommand(sublime_plugin.TextCommand):
    """
    Reflow the selected text to wrap after the specified width.
    This is handy for Python docstrings - sometimes you need to
    edit existing ones, and find that you no longer meet those
    pesky flake8 line length limits, and have multiple lines of
    text to re-line up nicely. (This command also helps when
    increasing the max line length!)
    
    If no width is specified, it will infer the desired width
    from the "rulers" setting on the view. If there are no rulers,
    a default of 72 is used.
    """
    def run(self, edit, width=0):
        new_sel = list()
        # use the narrowest ruler from the view if no width specified, or default to 72 if no rulers are enabled
        width = width or next(iter(self.view.settings().get('rulers', [])), 72)
        # determine the indentation style used in the view
        use_spaces = self.view.settings().get('translate_tabs_to_spaces', False)
        tab_size = self.view.settings().get('tab_size', 4)
        one_level = ' ' * tab_size if use_spaces else '\t'
        # loop through the selections in reverse order so that the selection positions don't move when the selected text changes size
        for sel in reversed(self.view.sel()):
            # make sure the leading indentation is selected, for `dedent` to work properly
            sel = sel.cover(self.view.line(sel.begin()))
            # determine how much indentation is at the first selected line
            indentation_level = self.view.indentation_level(sel.begin())
            indentation = one_level * indentation_level
            # create a wrapper that will keep that indentation
            wrapper = textwrap.TextWrapper(
                drop_whitespace=True,
                width=width - (0 if use_spaces else (tab_size - 1) * indentation_level), # if tabs are used, then we need to pretend the max width is smaller, because here Python counts a tab as a single char
                initial_indent=indentation,
                subsequent_indent=indentation,
                expand_tabs=False,
                replace_whitespace=True,
            )
            # unindent the selected text before then reformatting the text to fill the available (column) space
            text = wrapper.fill(textwrap.dedent(self.view.substr(sel)))
            # replace the selected text with the rewrapped text
            self.view.replace(edit, sel, text)
            # resize the selection to match the new wrapped text size
            new_sel.append(sublime.Region(sel.begin(), sel.begin() + len(text)))
        self.view.sel().clear()
        self.view.sel().add_all(new_sel)
