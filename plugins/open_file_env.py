import sublime
import sublime_plugin

import os

# Related reading
#     https://forum.sublimetext.com/t/can-i-use-env-variable-in-paths-of-sublime-commands/46437

# The internal open_file command can be used to open specifically named files
# (say as part of a key binding or menu entry) and supports the $platform and
# $packages variables, but no others.
#
# This plugin implements a drop-in replacement for the open_file command that
# will not only expand all of the variables usually available in a sublime-
# build file, but all environment variables as well.
#
# The original use case was to share one configuration file across multiple
# machines where the same files exist in different places by using an
# environment variable. It could be used for a variety of tasks, however.

class OpenFileEnvCommand(sublime_plugin.WindowCommand):
    """
    Drop in replacement for the open_file command that expands environment
    variables as well as standard Sublime variables in all command arguments.
    """
    def run(self, **kwargs):
        # Create a set of variables based on the current process environment
        # and the standard Sublime variables
        variables = dict(os.environ)
        variables.update(self.window.extract_variables())

        # Expand all variables and execute the base command with them
        kwargs = sublime.expand_variables(kwargs, variables)
        self.window.run_command("open_file", kwargs)
