import sublime
import sublime_plugin
import textwrap
from Default.comment import build_comment_data, ToggleCommentCommand

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
    
    Known limitations:
    - Wrapping contiguous text containing multiple indentation
      levels will have terrible results.
    - Wrapping line comments and anything else at the same time
      will cause the entire selection to become line commented.
    """
    def run(self, edit, width=0):
        # use the narrowest ruler from the view if no width specified, or default to 72 if no rulers are enabled
        width = width or next(iter(self.view.settings().get('rulers', [])), 72)
        # determine the indentation style used in the view
        use_spaces = self.view.settings().get('translate_tabs_to_spaces', False)
        tab_size = self.view.settings().get('tab_size', 4)
        one_level = ' ' * tab_size if use_spaces else '\t'
        
        # make sure the entire line is selected for each selection region
        # - `remove_line_comment` needs the region to be at the start of the line
        # - `dedent` needs it in order to see what indentation all lines have in common
        self.view.run_command('expand_selection', { 'to': 'line' })
        
        new_sel = list()
        sel_comment_data = list()
        
        # loop through the selections in reverse order so that the selection positions don't move when the selected text changes size
        for sel in reversed(self.view.sel()):
            # if the selection contains any single line comments, toggle the comments off
            # so the comment tokens won't get wrapped into the middle of the line - we'll reapply them later
            comment_data = build_comment_data(self.view, sel.begin())
            sel_comment_data.append(comment_data if ToggleCommentCommand.remove_line_comment(None, self.view, edit, comment_data, sel) else None)
        
        # loop through the selections in reverse order so that the selection positions don't move when the selected text changes size
        for sel, comment_data in zip(reversed(self.view.sel()), sel_comment_data):
            # determine how much indentation is at the first selected line
            indentation_level = self.view.indentation_level(sel.begin())
            indentation = one_level * indentation_level
            if comment_data: # if line comments were removed earlier
                line_comments, block_comments = comment_data
                # apply the line comment token as part of the indentation so the text wrapper will re-comment the text for us
                if any(line_comments): # if there is at least one line comment token defined
                    line_comment = line_comments[0] # if there are multiple such line comment tokens we will use the first one
                    if line_comment[1]: # if the line comment token has DISABLE_INDENT set
                        indentation = line_comment[0] + indentation # apply the indentation after the line comment token
                    else:
                        indentation += line_comment[0] # apply the indentation before the line comment token
            
            # create a text wrapper that will keep the existing indentation level
            wrapper = textwrap.TextWrapper(
                drop_whitespace=True,
                width=width - (0 if use_spaces else (tab_size - 1) * indentation_level), # if hard tab characters are used, then we need to pretend the max width is smaller, because here Python counts a tab as a single char. Easier to just not use tabs, people!
                initial_indent=indentation,
                subsequent_indent=indentation,
                expand_tabs=False,
                replace_whitespace=True,
            )
            # unindent the selected text, before then reformatting said text to fill the available (column) space
            text = wrapper.fill(textwrap.dedent(self.view.substr(sel)))
            # replace the selected text with the re-wrapped text
            self.view.replace(edit, sel, text + '\n')
            # resize the selection to match the new wrapped text size
            new_sel.append(sublime.Region(sel.begin(), sel.begin() + len(text)))
        self.view.sel().clear()
        self.view.sel().add_all(new_sel)
