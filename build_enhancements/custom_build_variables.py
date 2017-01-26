import sublime, sublime_plugin

# Related reading:
#     http://stackoverflow.com/questions/40193019/set-project-dependent-build-system-variables

# This is yet another example of how to customize Sublime build systems to do
# what you want them to do. In this example, we provide the ability to specify
# our own custom build variables for cases when the ones built into Sublime are
# not enough.

# For this to work, you need to specify that the "target" is this command,
# specify the command to execute as "command" instead of "cmd", and of course
# provide the settings that you want to expand (such as in your project or from
# a plugin).
#
# An example might be:
#
# {
#     "target": "my_custom_build",
#     "command": ["build.sh", "${proj_var_1}"],
#
#     "working_dir": "${project_path:${folder}}",
#     "shell": false
# }

# Something to watch out for here is that when Sublime executes the build, it
# does an expansion of variables that it supports internally before it passes
# the results to the custom command. During this process, any custom variables
# that we have added will get replaced with empty text because they are not
# recognized.
#
# This only happens for fields that Sublime knows are part of a build file. That
# is why you need to specify "command" instead of "cmd" in the build.

# List of variable names we want to support
custom_var_list = ["proj_var_1"]

class MyCustomBuildCommand(sublime_plugin.WindowCommand):
    """
    Provide custom build variables to a build system, such as a value that needs
    to be specific to a current project.

    This example only allows for variables in the "cmd" field, but could be
    easily extended.
    """
    def createExecDict(self, sourceDict):
        global custom_var_list

        # Get the project specific settings
        project_data = self.window.project_data ()
        project_settings = (project_data or {}).get ("settings", {})

        # Get the view specific settings
        view_settings = self.window.active_view ().settings ()

        # Variables to expand; start with defaults, then add ours.
        variables = self.window.extract_variables ()
        for custom_var in custom_var_list:
            variables[custom_var] = view_settings.get (custom_var,
                project_settings.get (custom_var, ""))

        # Create arguments to return by expanding variables in the
        # arguments given.
        args = sublime.expand_variables (sourceDict, variables)

        # Rename the command parameter to what exec expects.
        args["cmd"] = args.pop ("command", [])

        return args

    def run(self, **kwargs):
        self.window.run_command ("exec", self.createExecDict (kwargs))