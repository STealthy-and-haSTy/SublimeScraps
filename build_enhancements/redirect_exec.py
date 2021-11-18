import sublime
import sublime_plugin

import os
import tempfile

from Default.exec import ExecCommand

# Related Reading:
#     https://stackoverflow.com/questions/68083252/run-a-python-snippet-with-every-run-on-sublime-text

# This is an example of a build system custom target, in this case one that
# will generate a temporary file based on the contents of the current file.
# This plugin requires Sublime Text 4; the version of the ExecCommand class
# subclassed here is laid out differently in ST3. To use this plugin there,
# some changes would need to be made as outlined in the stack overflow
# post above.
#
# This could be useful for things like executing only selected code or only
# some parts of a larger file, or as in this example to augment a file with
# extra boilerplate code that you want there while it's executing without it
# being permanent.
#
# In use, the build will generate a temporary file that contains the boiler
# plate code below and the contents of the current file. The name of the
# temporary file is stored in the $temp_file variable in the build.
#
# An example build might be:

# {
#     "target": "python_with_redirect_exec",
#     "cancel": {"kill": true},
#
#     "cmd": ["python3", "-u", "\\$temp_file"],
#     "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
#     "selector": "source.python",
#
#     "working_dir": "${file_path}",
#
#     "env": {"PYTHONIOENCODING": "utf-8"},
#
#     "windows": {
#         "cmd": ["py", "-u", "\\$temp_file"],
#     },
# }


_stub = """
import sys
sys.stdin, sys.stdout = open('input', 'r'), open('output', 'w')

"""


class PythonWithRedirectExecCommand(ExecCommand):
    def run(self, **kwargs):
        view = self.window.active_view()
        if view.file_name() is None or not os.path.exists(view.file_name()):
            return self.window.status_message("Cannot build; no file associated with the current view")

        self.tmp_file = self.get_temp_file(view)

        variables = {"temp_file": self.tmp_file}
        kwargs = sublime.expand_variables(kwargs, variables)

        super().run(**kwargs)

    def get_temp_file(self, view):
        handle, name = tempfile.mkstemp(text=True, suffix=".py")
        with os.fdopen(handle, mode="wt", encoding="utf-8") as handle:
            handle.write(_stub)
            with open(view.file_name()) as source:
                handle.write(source.read())

        return name

    def on_finished(self, proc):
        super().on_finished(proc)

        # If the current build didn't finish or it was manually killed, leave.
        if proc != self.proc or proc.killed:
            return

        try:
            # If the build suceeded, delete the temporary file; we will leave
            # it alone if the build fails so that it's possible to navigate
            # to it.
            exit_code = proc.exit_code()
            if exit_code == 0 or exit_code is None:
                os.remove(self.tmp_file)
        finally:
            self.tmp_file = None
