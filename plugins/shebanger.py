import sublime, sublime_plugin

# Related reading:
#     http://stackoverflow.com/questions/39606221/how-to-create-sublime-text-3-build-system-which-reads-shebang


class ShebangerCommand(sublime_plugin.WindowCommand):
    """
    Command to be used as the "target" option in a build system. Based on a
    customized build system, this will modify the version of python used to
    the one listed in the shebang line at the start of the script (if any).
    """
    def parseShebang (self, filename):
        with open(filename, 'r') as handle:
            shebang = handle.readline ().strip ().split (' ', 1)[0]
        if shebang.startswith ("#!"):
            return shebang[2:]
        return None

    def createExecDict(self, sourceDict):
        current_file = self.window.active_view ().file_name()
        args = dict (sourceDict)

        interpreter = args.pop ("interpreter_default", "python")
        exec_args = args.pop ("interpreter_args", ["-u"])
        shebang = self.parseShebang (current_file)

        args["shell_cmd"] = "{} {} \"{}\"".format (shebang or interpreter,
                                                   " ".join (exec_args),
                                                   current_file)

        return args

    def run(self, **kwargs):
        self.window.run_command ("exec", self.createExecDict (kwargs))
