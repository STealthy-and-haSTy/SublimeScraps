import sublime, sublime_plugin

# Related reading:
#     http://stackoverflow.com/questions/41768673/let-sublime-choose-among-two-similar-build-systems


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
