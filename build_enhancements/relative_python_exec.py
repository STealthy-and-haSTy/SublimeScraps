import sublime
import sublime_plugin

import os

from Default.exec import ExecCommand

# Related reading:
#     https://forum.sublimetext.com/t/how-can-i-create-a-new-build-system-to-run-python-from-project-root/47461/2
#
# This is an example of a custom build target that can execute Pythion code
# as a module by calculating the module name of the file based on the root of
# the project. Given a folder named myProject/folder1/my_file.py, then
# you could excecute it as "python -m folder1.my_file" with the current
# directory being myProject.
#
# This exposes a new variable named module_name that represents the module name
# of the current file.
#
# To use this, create a sublime-build file with contents similar to the
# following example:
#
# {
#     "target": "relative_python_exec",
#     "cancel": {"kill": true},
#
#     "shell_cmd": "python -um \"\\${module_name}\"",
#     "working_dir": "${folder}",
#
#     "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
#     "selector": "source.python",
#
#     "env": {"PYTHONIOENCODING": "utf-8"},
# }
#

class RelativePythonExecCommand(ExecCommand):
    def run(self, **kwargs):
        # Get the standard list of build variables and construct a
        # relative path to the current file based on the first open
        # folder
        var_list = self.window.extract_variables()
        rel_name = os.path.relpath(var_list["file"], var_list["folder"])

        # Remove the extension and replace path separators with periods
        rel_name = os.path.splitext(rel_name)[0].replace(os.path.sep, '.')

        # Set up a new variable and then expand it in the keyword args
        var_list["module_name"] = rel_name

        # This should only expand variables in shell_cmd, cmd and working_dir
        # if it wants to be fully compatible with exec. Or alternately you
        # can do it this way, which allows you to expand variables in all
        # keys if you wanted to do that.
        kwargs = sublime.expand_variables(kwargs, var_list)

        # Run the build
        super().run(**kwargs)
