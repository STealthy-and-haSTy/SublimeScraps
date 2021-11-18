import sublime, sublime_plugin

from Default.exec import ExecCommand


# Related reading:
#     http://stackoverflow.com/questions/40193019/set-project-dependent-build-system-variables

# This is yet another example of how to customize Sublime build systems to do
# what you want them to do. In this example, we provide the ability to specify
# our own custom build variables for cases when the ones built into Sublime are
# not enough.

# For this to work, you need to specify that the "target" is this command, and
# of course provide the settings that you want to expand (such as in your
# project or from a plugin).
#
# An example might be:
#
# {
#     "target": "my_custom_build",
#     "cancel": { "kill": true },
#     "cmd": ["build.sh", "\\${proj_var_1}"],
#
#     "working_dir": "${project_path:${folder}}",
#     "shell": false
# }

# Sublime will expand all variables in the build keys for cmd, shell_cmd and
# working_dir before it invokes your custom command target. If you want to
# include custom variables in those, you need to escape them so that Sublime
# will leave them alone.

# List of variable names we want to support; these will come from:
#    1. Your global preferences
#    2. Project specific settings
#    3. Syntax specific settings
#    4. Buffer (file) specific overrides
custom_var_list = ["proj_var_1"]

class MyCustomBuildCommand(ExecCommand):
    """
    Provide custom build variables to a build system, such as a value that needs
    to be specific to a current project.

    This example only allows for variables in the "cmd" field, but could be
    easily extended.
    """
    def run(self, **kwargs):
        # Get the view specific settings
        settings = self.window.active_view().settings()

        # Variables to expand; start with defaults, then add ours.
        variables = {}
        for custom_var in custom_var_list:
            variables[custom_var] = settings.get(custom_var)

        # Expand out our variables in all of the arguments, and then invoke the
        # super method to execute the build.
        kwargs = sublime.expand_variables(kwargs, variables)
        super().run(**kwargs)
