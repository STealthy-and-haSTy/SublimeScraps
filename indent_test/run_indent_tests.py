import os
import re
from difflib import ndiff

import sublime
import sublime_plugin

# As evidenced here, the indent test code is based on code in this imported
# module from the Default package.
from Default.run_syntax_tests import package_relative_path, PACKAGES_FILE_REGEX
from Default.run_syntax_tests import show_panel_on_build, append


### ---------------------------------------------------------------------------


class RunIndentTestsCommand(sublime_plugin.WindowCommand):
    """
    A custom command that can be executed from a build system target for
    testing indent rules. The current file needs to have a known name prefix
    to be considered, and must have a header line that tells the tester what
    syntax it is.

    The test inserts the data unindented into a view and then runs the reindent
    command to indent it, comparing the results to what the input file looked
    like to verify the indent level.
    """
    def run(self, find_all=False, **kwargs):
        if not hasattr(self, 'output_view'):
            # Try not to call get_output_panel until the regexes are assigned
            self.output_view = self.window.create_output_panel('exec')

        settings = self.output_view.settings()
        settings.set('result_file_regex', PACKAGES_FILE_REGEX)
        settings.set('result_base_dir', sublime.packages_path())
        settings.set('word_wrap', True)
        settings.set('line_numbers', False)
        settings.set('gutter', False)
        settings.set('scroll_past_end', False)

        # Call create_output_panel a second time after assigning the above
        # settings, so that it'll be picked up as a result buffer
        self.window.create_output_panel('exec')

        if find_all:
            tests = sublime.find_resources('indentation_test*')
        else:
            # Can't test files that are not in the packages folder.
            pkg_path = package_relative_path(self.window.active_view())
            if not pkg_path:
                return

            # We can only test files that we know are indent tests.
            file_name = os.path.basename(pkg_path)
            if not file_name.startswith("indentation_test"):
                return sublime.error_message(
                    'The current file is not an indentation test')

            # Get the syntax for the current file out of the header.
            syntax = self.syntax_for_file(pkg_path)
            if syntax is None:
                return sublime.error_message(
                    'The indentation test header is missing');

            # At a minimum, we are going to test this file.
            tests = [pkg_path]

            # Find all other files that are using this syntax and add them to
            # the test list. Realistically this should only happen if the
            # current file was a tmPreferences file, but there is currently no
            # good way to get the appropriate syntax from such a file.
            for file in sublime.find_resources('indentation_test*'):
                if file != pkg_path and self.syntax_for_file(file) == syntax:
                    tests.append(file)

        show_panel_on_build(self.window)

        total_lines = 0
        failed_lines = 0

        for test in tests:
            lines, failures = self.run_indent_test(test)
            total_lines += lines
            if len(failures) > 0:
                failed_lines += len(failures)
                for line in failures:
                    append(self.output_view, line + '\n')

        if failed_lines > 0:
            message = 'FAILED: {} of {} lines in {} files failed\n'
            params = (failed_lines, total_lines, len(tests))
        else:
            message = 'Success: {} lines in {} files passed\n'
            params = (total_lines, len(tests))

        append(self.output_view, message.format(*params))
        append(self.output_view, '[Finished]')

    def run_indent_test(self, package_file):
        syntax = self.syntax_for_file(package_file)
        if syntax is None:
            return (0, [])

        input_file = sublime.load_resource(package_file)
        input_lines = input_file.splitlines()

        view = self.window.create_output_panel("indent_test", False)

        view.assign_syntax(syntax)
        view.run_command("select_all")
        view.run_command("left_delete")

        for line in input_lines:
            view.run_command("append", {"characters": line.lstrip() + "\n"})

        view.run_command("select_all")
        view.run_command("reindent")

        output_file = view.substr(sublime.Region(0, view.size()))
        output_lines = output_file.splitlines()

        if input_file == output_file:
            return (len(input_lines), [])

        diff = ndiff(input_file.splitlines(), output_file.splitlines())

        line_num = 0
        errors = []
        for line in diff:
            prefix = line[:2]
            line_num += 1 if prefix in ("  ", "+ ") else 0

            if prefix == "+ ":
                msg = "{}:{}:1: Indent Failure: {}".format(package_file, line_num, line[2:])
                errors.append(msg)

        # self.window.run_command("show_panel", {"panel": "output.indent_test"})
        return (len(input_lines), errors)

    def syntax_for_file(self, package_file):
        first_line = sublime.load_resource(package_file).splitlines()[0]
        match = re.match('^.*INDENT TEST "(.*?)"', first_line)
        if not match:
            return None

        return match.group(1)
