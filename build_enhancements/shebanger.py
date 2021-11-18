import sublime, sublime_plugin

from Default.exec import ExecCommand


# Related reading:
#     http://stackoverflow.com/questions/39606221/how-to-create-sublime-text-3-build-system-which-reads-shebang

# Normally in a Sublime build system you need to specify the program to run to
# execute the build directly. This is an example of how you could modify a build
# system so that it gets the name of the executable to use to build the current
# file from the current file itself.
#
# In order to use this, you would need a build file that looks something like
# the following example. This build is python specific but it doesn't need to
# be.
#
# {
#     // WindowCommand to execute for this build
#     "target": "shebanger",
#     "cancel": { "kill": true },
#
#     // Default program for when there is no shebang
#     "interpreter_default": "python",
#
#     // Default arguments for when there is no shebang or it has no args
#     "interpreter_args": ["-u"],
#
#     "file_regex": "^[ ]*File \"(...*?)\", line([0-9]*)",
#     "selector": "source.python",
#
#     "env": {"PYTHONIOENCODING": "utf-8"},
#
#     "variants":
#     [
#         {
#             "name": "Syntax Check",
#             "interpreter_args": ["-m py_compile"],
#         }
#     ]
# }

class ShebangerCommand(ExecCommand):
    """
    Command to be used as the "target" option in a build system. Based on a
    customized build system, this will modify the version of python used to
    the one listed in the shebang line at the start of the script (if any).
    """
    def parse_shebang(self, filename):
        with open(filename, 'r') as handle:
            shebang = handle.readline().strip().split(' ', 1)
        if shebang[0].startswith("#!"):
            return (shebang[0][2:],
                    shebang[1].split(' ') if len(shebang) > 1 else [])
        return None, None

    def run(self, **kwargs):
        current_file = self.window.active_view().file_name() or ''

        # Capture the default program and arguments from the build; used in
        # case the current file doesn't have a shebang.
        def_prog = kwargs.pop("interpreter_default", "python")
        def_args = kwargs.pop("interpreter_args", ["-u"])

        # Parse the file to get the program and arguments.
        prog, prog_args = self.parse_shebang(current_file)

        kwargs["shell_cmd"] = "{} {} \"{}\"".format(
            prog or def_prog, " ".join(prog_args or def_args), current_file)
        super().run(**kwargs)
