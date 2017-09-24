import sublime
import sublime_plugin
import textwrap
from Default.comment import build_comment_data, ToggleCommentCommand, advance_to_first_non_white_space_on_line

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
            # do it on a paragraph by paragraph basis so we don't lose blank line gaps
            text = ''
            for paragraph in textwrap.dedent(self.view.substr(sel)).split('\n\n'):
                if text != '':
                    text += '\n\n'
                text += wrapper.fill(paragraph)
            
            # replace the selected text with the re-wrapped text
            self.view.replace(edit, sel, text + '\n')
            # resize the selection to match the new wrapped text size
            new_sel.append(sublime.Region(sel.begin(), sel.begin() + len(text)))
        self.view.sel().clear()
        self.view.sel().add_all(new_sel)


def find_region_matching_selector(view, within_region, selector):
    is_match = lambda pt: view.match_selector(pos, selector)
    pos = within_region.begin()
    while pos < within_region.end() and not is_match(pos):
        pos += 1
    start_pos = pos
    while pos < within_region.end() and is_match(pos):
        pos += 1
    return sublime.Region(start_pos, pos)


class ContinueCommentOnNextLineCommand(sublime_plugin.TextCommand):
    """
    This is handy when you are in a comment, and want to spill over
    into a new line manually. For a single line comment, this means
    that the comment token would be inserted on the next line, for
    a block comment, what one might want could depend on the syntax
    and personal preference - for example, a space followed by an
    asterisk, or nothing at all. (Here we will let the caller decide,
    to keep things simple. Then the user can create a keybinding with
    different arguments for different situations.)
    
    We can't rely on the meta info for the syntax to tell us what the
    line comment token is (as at Build 3144, the C# syntax definition
    scopes `///` as a documentation block comment, but it is really a
    line comment, and it is not included in the meta info), so we
    instead find the punctuation scope at the beginning of the line to
    find the line comment token.
    """
    def run(self, edit, insert_what=None):
        if insert_what is None:
            # find text with the `punctuation` scope on the line, only searching up to the caret position
            pos = self.view.sel()[0].begin()
            line_begin = self.view.line(pos).begin()
            region = find_region_matching_selector(self.view, sublime.Region(line_begin, pos), 'punctuation')
            insert_what = self.view.substr(region)
        # the insert command will take care of keeping the indentation after the \n the same as the current line
        if insert_what:
            insert_what += ' ' # don't insert a space when pressing `enter` before the start of a line comment
        self.view.run_command('insert', { 'characters': '\n' + insert_what })


def unique_regions(regions):
    # NOTE: using `set(` directly doesn't work due to Region not being a hashable type...
    return set(map(lambda region: (region.begin(), region.end()), regions))


class JoinLineBelowCommand(sublime_plugin.TextCommand):
    """
    Join the line below to the current line - no matter where the caret
    is. This will remove the `\n` character at EOL, and all leading
    whitespace at the beginning of the next line (i.e. indentation).
    
    Also, if the `\n` on the current line is scoped as a comment line,
    then look for more comment line punctuation on the beginning of the
    next line, and remove that too. This makes it easy to join comment
    lines together. If a space precedes the end of the current line,
    also remove leading whitespace after the comment token.
    """
    def run(self, edit):
        # get a unique list of lines where the caret(s) are
        caret_lines = unique_regions([self.view.line(sel) for sel in self.view.sel()])
        # iterate through them in reverse order, so that the selection positions don't move when the gaps between the text change size
        for current_line_begin, current_line_end in reversed(list(caret_lines)):
            next_line = self.view.line(current_line_end + 1)
            # find where the leading whitespace on the next line ends
            whitespace_ends = min(next_line.end(), advance_to_first_non_white_space_on_line(self.view, next_line.begin()))
            # if the current line is a comment
            if self.view.match_selector(current_line_end, 'comment'):
                # find where the comment punctuation ends
                if self.view.match_selector(whitespace_ends, 'punctuation.definition.comment - punctuation.definition.comment.end'):
                    whitespace_ends = find_region_matching_selector(self.view, sublime.Region(whitespace_ends, next_line.end()), 'punctuation').end()
                    # if a space preceeds the end of the current line
                    if self.view.substr(max(current_line_begin, current_line_end - 1)) == ' ':
                        # also remove leading whitespace after the comment token
                        whitespace_ends = min(next_line.end(), advance_to_first_non_white_space_on_line(self.view, whitespace_ends))
            # remove the \n and any leading whitespace on the next line
            self.view.replace(edit, sublime.Region(current_line_end, whitespace_ends), '')

# Example keybindings (duplicate `enter` to `keypad_enter` if desired)
# { "keys": ["alt+q"], "command": "wrap_text" },
# { "keys": ["enter"], "command": "continue_comment_on_next_line",
#     "args": {
#         "insert_what": "*",
#     },
#     "context": [
#         { "key": "selector", "operator": "equal", "operand": "comment.block - comment.block.documentation", "match_all": true },
#         { "key": "auto_complete_visible", "operator": "equal", "operand": false },
#         { "key": "preceding_text", "operator": "not_regex_contains", "operand": "/\\*", "match_all": true },
#     ],
# },
# { "keys": ["enter"], "command": "continue_comment_on_next_line",
#     "args": {
#         "insert_what": " *",
#     },
#     "context": [
#         { "key": "selector", "operator": "equal", "operand": "comment.block - comment.block.documentation", "match_all": true },
#         { "key": "auto_complete_visible", "operator": "equal", "operand": false },
#         { "key": "preceding_text", "operator": "regex_contains", "operand": "/\\*", "match_all": true },
#     ],
# },
# { "keys": ["enter"], "command": "continue_comment_on_next_line",
#     "context": [
#         { "key": "selector", "operator": "equal", "operand": "comment.block.documentation.cs", "match_all": true },
#         { "key": "auto_complete_visible", "operator": "equal", "operand": false },
#     ],
# },
# { "keys": ["enter"], "command": "continue_comment_on_next_line",
#     "context": [
#         { "key": "selector", "operator": "equal", "operand": "comment.line", "match_all": true },
#         { "key": "auto_complete_visible", "operator": "equal", "operand": false },
#     ],
# },
# { "keys": ["delete"], "command": "join_line_below",
#     "context": [
#         { "key": "following_text", "operator": "regex_match", "operand": "$", "match_all": true },
#         { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
#     ],
# },
