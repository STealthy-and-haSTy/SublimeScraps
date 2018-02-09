import sublime
import sublime_plugin
import textwrap
from Default.comment import advance_to_first_non_white_space_on_line, build_comment_data

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
    def run(self, edit, width=0, keep_selection=False):
        # use the narrowest ruler from the view if no width specified, or default to 72 if no rulers are enabled
        width = width or next(iter(self.view.settings().get('rulers', [])), 72)
        # determine the indentation style used in the view
        use_spaces = self.view.settings().get('translate_tabs_to_spaces', False)
        tab_size = self.view.settings().get('tab_size', 4)
        one_level = ' ' * tab_size if use_spaces else '\t'
        
        # make sure the entire line is selected for each selection region
        # - `remove_line_comment` needs the region to be at the start of the line
        # - `dedent` needs it in order to see what indentation all lines have in common
        # but first, ensure we follow the Principal of Least Surprise by not expanding the selection to lines where only column 0 is selected
        # - related reading: https://forum.sublimetext.com/t/next-line-is-included-when-sorting-a-multi-line-selection/30580
        self.view.run_command('deselect_trailing_newlines')
        if any(sel for sel in self.view.sel() if not sel.empty()):
            self.view.run_command('expand_selection', { 'to': 'line' })
        else:
            self.view.run_command('expand_selection_to_paragraph')
        
        new_sel = list()
        sel_comment_data = list()
        
        # loop through the selections in reverse order so that the selection positions don't move when the selected text changes size
        for sel in reversed(self.view.sel()):
            # if the selection contains any single line comments, toggle the comments off
            # so the comment tokens won't get wrapped into the middle of the line - we'll reapply them later
            # note the selector doesn't just use `comment.line punctuation.definition.comment`, because C# line documentation comments are scoped as `comment.block.documentation.cs punctuation.definition.comment.documentation.cs`
            comment_punctuation = list(find_regions_matching_selector(self.view, sel, 'comment punctuation.definition.comment - punctuation.definition.comment.begin - punctuation.definition.comment.end'))
            sel_comment_data.append(self.view.substr(comment_punctuation[0]) + ' ' if any(comment_punctuation) else None)
            for punctuation in reversed(comment_punctuation):
                # also remove any space after the comment line punctuation, else the `indentation_level` API can return the wrong result...
                if self.view.substr(punctuation.end()) == ' ':
                    punctuation = punctuation.cover(sublime.Region(punctuation.end(), punctuation.end() + len(' ')))
                self.view.erase(edit, punctuation)
        
        # loop through the selections in reverse order so that the selection positions don't move when the selected text changes size
        for sel, line_comment in zip(reversed(self.view.sel()), sel_comment_data):
            # determine how much indentation is at the first selected line
            indentation_level = self.view.indentation_level(sel.begin())
            indentation = one_level * indentation_level
            
            if line_comment: # if line comments were removed earlier
                comment_data = build_comment_data(self.view, sel.begin())
                # find the line comment that corresponds to the comment punctuation used, and check if indentation is disabled for it or not
                disable_indent = next((data[1] for data in comment_data if isinstance(data, tuple) and data[0].strip() == line_comment), False)
                # apply the line comment token as part of the indentation so the text wrapper will re-comment the text for us
                if disable_indent: # if the line comment token has DISABLE_INDENT set
                    indentation = line_comment + indentation # apply the indentation after the line comment token
                else:
                    indentation += line_comment # apply the indentation before the line comment token
            
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
            # resize the selection to match the new wrapped text size - or move it to the end of the wrapped text
            end_pos = sel.begin() + len(text)
            start_pos = sel.begin() if keep_selection else end_pos
            new_sel.append(sublime.Region(start_pos, end_pos))
        self.view.sel().clear()
        self.view.sel().add_all(new_sel)


def find_region_matching_selector(view, within_region, selector):
    is_match = lambda pt: view.match_selector(pos, selector)
    # advance while the selector doesn't match
    pos = within_region.begin()
    while pos < within_region.end() and not is_match(pos):
        pos += 1
    start_pos = pos
    # advance while the selector matches to find the extent the scope
    while pos < within_region.end() and is_match(pos):
        pos += 1
    if start_pos == pos:
        return None
    return sublime.Region(start_pos, pos)

def find_regions_matching_selector(view, within_region, selector):
    while True:
        region = find_region_matching_selector(view, within_region, selector)
        if region:
            yield region
            within_region = sublime.Region(region.end(), within_region.end())
        else:
            return

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
            region = find_region_matching_selector(self.view, sublime.Region(line_begin, pos), 'comment punctuation')
            insert_what = self.view.substr(region)
        # the insert command will take care of keeping the indentation after the \n the same as the current line
        if insert_what:
            insert_what += ' ' # don't insert a space when pressing `enter` before the start of a line comment
        self.view.run_command('insert', { 'characters': '\n' + insert_what })


def unique_regions(regions):
    # NOTE: using `set(` directly doesn't work due to Region not being a hashable type, as Region isn't immutable
    #       - this doesn't return a Region, but a tuple (although we could change it to if desired)
    return set(map(lambda region: (region.begin(), region.end()), regions))


class JoinLineBelowCommand(sublime_plugin.TextCommand):
    """
    Join the line below to the current line - no matter where the caret
    is. This will remove the `\n` character at EOL, and all leading
    whitespace at the beginning of the next line (i.e. indentation).
    
    If a space doesn't preceed the end of the current line, add a space
    before joining the lines together, if the next line isn't empty and
    doesn't consist only of whitespace (as that will get trimmed and we
    would end up with a space after the caret and nothing after it when
    using this command to remove "blank" lines below the current one).
    
    Also, if the `\n` on the current line is scoped as a comment line,
    then look for more comment line punctuation on the beginning of the
    next line, and remove that too along with any whitespace after it.
    This makes it easy to join comment lines together.
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
                    whitespace_ends = find_region_matching_selector(self.view, sublime.Region(whitespace_ends, next_line.end()), 'comment punctuation').end()
                    # also remove leading whitespace after the comment token
                    whitespace_ends = min(next_line.end(), advance_to_first_non_white_space_on_line(self.view, whitespace_ends))
            # if a space preceeds the end of the current line, or the current or next line is empty, don't insert a space before the line being joined, otherwise do
            replace_with = '' if self.view.substr(max(current_line_begin, current_line_end - 1)) in (' ', '\n') or next_line.empty() or whitespace_ends == next_line.end() else ' '
            # remove the \n and any leading whitespace on the next line
            self.view.replace(edit, sublime.Region(current_line_end, whitespace_ends), replace_with)


#  capture when the built in wrap_lines command is executed and rewrite it to execute our much better command instead
class WrapTextListener(sublime_plugin.EventListener):
    def on_text_command(self, view, command_name, args):
        if command_name == 'wrap_lines':
            return ('wrap_text', args)
        return None


class DeselectTrailingNewlines(sublime_plugin.TextCommand):
    """
    For each selection that is non-empty, if the very last character in
    the selection is a `\n`, then remove/subtract it from the selection.
    
    This is useful when wanting to use a command that will expand the
    selections to the entire line, as one might expect that having no
    text on the line selected should result in the line not being
    included when executing such a command, but the selection is
    expanded from column 0 to the next `\n` character at the end of
    that line...
    """
    def run(self, edit):
        subtract = []
        for sel in self.view.sel():
            if not sel.empty():
                # if the selection ends on column 0 (am presuming this is more performant that checking the last character in the selection)
                if self.view.rowcol(sel.end())[1] == 0:
                    # add the `\n` to the list of regions to subtract from the selections
                    subtract.append(sublime.Region(sel.end() - 1, sel.end()))
        # remove the `\n`s (am assuming this is more performant than removing all selections and re-adding regions without the `\n`s)
        for region in subtract:
            self.view.sel().subtract(region)


# Example keybindings (duplicate `enter` to `keypad_enter` if desired)
# { "keys": ["alt+q"], "command": "wrap_text" },
# { "keys": ["enter"], "command": "continue_comment_on_next_line", // when on a block comment line with an asterisk on it already, ST will keep the space before it when pressing <kbd>Enter</kbd>, so we just need to insert another asterisk
#     "args": {
#         "insert_what": "*",
#     },
#     "context": [
#         { "key": "selector", "operator": "equal", "operand": "comment.block - comment.block.documentation - (text - text source)", "match_all": true },
#         { "key": "auto_complete_visible", "operator": "equal", "operand": false },
#         { "key": "preceding_text", "operator": "not_regex_contains", "operand": "/\\*|\\*/$|^$", "match_all": true },
#     ],
# },
# { "keys": ["enter"], "command": "continue_comment_on_next_line", // when on a block comment line without an asterisk on it already - i.e. the opening /* line, we need to insert a space and an asterisk when the user presses <kbd>Enter</kbd>
#     "args": {
#         "insert_what": " *",
#     },
#     "context": [
#         { "key": "selector", "operator": "equal", "operand": "comment.block - comment.block.documentation - (text - text source)", "match_all": true }, // don't trigger for XML, HTML (/ Markdown) or other syntaxes unless in an embedded source scope inside Markdown for example
#         { "key": "auto_complete_visible", "operator": "equal", "operand": false },
#         { "key": "preceding_text", "operator": "regex_contains", "operand": "/\\*", "match_all": true },
#         { "key": "preceding_text", "operator": "not_regex_contains", "operand": "\\*/$|^$", "match_all": true },
#     ],
# },
# { "keys": ["enter"], "command": "continue_comment_on_next_line",
#     "context": [
#         { "key": "selector", "operator": "equal", "operand": "comment.line, comment.block.documentation.cs", "match_all": true },
#         { "key": "auto_complete_visible", "operator": "equal", "operand": false },
#         { "key": "preceding_text", "operator": "not_regex_contains", "operand": "^$", "match_all": true },
#     ],
# },
# { "keys": ["delete"], "command": "join_line_below",
#     "context": [
#         { "key": "following_text", "operator": "regex_match", "operand": "$", "match_all": true },
#         { "key": "preceding_text", "operator": "not_regex_match", "operand": "^", "match_all": true },
#         { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
#         //{ "key": "selector", "operator": "equal", "operand": "comment", "match_all": true },
#     ],
# },
