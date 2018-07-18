import sublime
import sublime_plugin

# This plugin provides a command that you can use to toggle the state of the
# three internal Sublime logging commands on and off. It takes as an argument
# the type of logging to toggle, which can be one of "log_commands",
# "log_input" or "log_result_regex".
#
# Note that the plugin assumes that you're only using these commands to change
# the state of the logging; since there is no API for getting the current state
# for the log toggles, the command here can't detect if you've changed the
# state of the logging via some external mechanism.
#
# This could be used in a key binding as well as in a sublime-commands or
# sublime-menu file.
#
# In a sublime-menu, the command will display as checked when logging for that
# type of log is enabled if  you include the "checkbox" attribute to the menu
# entry. The command also has a default description which displays what command
# it will execute when it's selected.
#
# As an example, you can add the following to a file named Context.sublime-menu
# in your User package to include the commands in the context menu.
#
# [
    # { "caption": "-", "id": "end" },
    # {
    #     "command": "toggle_sublime_logging",
    #     "checkbox": true,
    #     "caption": "Log Commands",
    #     "args": {"log_type": "log_commands"},
    # },
    # {
    #     "command": "toggle_sublime_logging",
    #     "checkbox": true,
    #     "caption": "Log Input",
    #     "args": {"log_type": "log_input"},
    # },
    # {
    #     "command": "toggle_sublime_logging",
    #     "checkbox": true,
    #     "caption": "Log Result Regex",
    #     "args": {"log_type": "log_result_regex"},
    # },
    # {
    #     "command": "toggle_sublime_logging",
    #     "checkbox": true,
    #     "caption": "Log Build Systems",
    #     "args": {"log_type": "log_build_systens"},
    # }
# ]


_log_state = {
    "log_commands": False,
    "log_input": False,
    "log_result_regex": False,
    "log_build_systems": False
}


class ToggleSublimeLoggingCommand(sublime_plugin.ApplicationCommand):
    """
    Toggle the state of Sublime's internal logging to the console based on the
    log_type parameter, which should be one of the three sublime module API
    endpoints, "log_command", "log_input" or "log_result_regex".
    """
    def run(self, log_type):
        _log_state[log_type] = not _log_state[log_type]
        getattr(sublime, log_type)(_log_state[log_type])

    def description(self, log_type):
        return "sublime.{0}({1})".format(log_type, not _log_state[log_type])

    def is_checked(self, log_type):
        return _log_state[log_type]
