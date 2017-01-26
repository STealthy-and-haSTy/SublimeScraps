import sublime, sublime_plugin

# Related reading:
#     http://stackoverflow.com/questions/41768673/let-sublime-choose-among-two-similar-build-systems

# This is very similar to shebanger.py. This uses the same method, only here the
# idea is that the build system holds the possible list of interpreters and the
# first line of the file is formatted to allow the build to select.
#
# This example is for selecting between a 32-bit or 64-bit version of Python,
# but it could easily be modified to select between different versions of
# python, operate for different languages, etc.
#
# In order to use this, you would need a build file that looks something like
# this. Here the important parts are the "target" and the two different
# interpreters to use.
#
# {
#     "target": "python_build",
#
#     "shell_cmd": "python -u \"$file\"",
#     "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
#     "selector": "source.python",
#
#     "python32": "python",
#     "python64": "c:/python27-64/python",
#
#     "env": {"PYTHONIOENCODING": "utf-8"},
#
#     "variants":
#     [
#         {
#             "name": "Syntax Check",
#             "shell_cmd": "python -m py_compile \"${file}\"",
#         }
#     ]
# }

class PythonBuildCommand(sublime_plugin.WindowCommand):
    """
    A take on shebanger.py. Here the build system file explictly specifies what
    to use for the executable for two different versions of python and the
    build system will select the appropriate version based on the first line in
    the file.
    """
    def detect_version(self, filename, python32, python64):
        with open(filename, 'r') as handle:
            line = handle.readline ()
        return python64 if (line.startswith ("#") and "64" in line) else python32

    def execArgs(self, sourceArgs):
        current_file = self.window.active_view ().file_name ()
        args = dict (sourceArgs)

        python32 = args.pop ("python32", "python")
        python64 = args.pop ("python64", "python")
        selected = self.detect_version (current_file, python32, python64)

        if "shell_cmd" in args:
            args["shell_cmd"] = args["shell_cmd"].replace ("python", selected)

        return args

    def run(self, **kwargs):
        self.window.run_command ("exec", self.execArgs (kwargs))
