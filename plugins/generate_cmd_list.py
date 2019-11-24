import sublime
import sublime_plugin

# Related reading:
#     https://stackoverflow.com/questions/48656430/how-to-list-all-commands-in-sublime-text-3/
#
# This plugin is a variation on the version referenced in the Stack Overflow
# answer above, and creates an output view in the current window that contains
# information on all commands currently known to Sublime (except commands in
# the core, which are not exposed for runtime introspection).
#
# The output splits the commands first by the package that they're defined in
# and then by their type. Each command is shown with arguments accepted,
# default values for arguments, and a description of the command if it is
# available.
#
# This information is gained via introspection and so it is potentially
# incomplete and subject to the whims of the developer that generated the
# command to a large degree.
#
# Something to note is that this won't pick up commands in the Sublime core
# as they're not implemented by direct plugin code and are thus not exposed via
# the mechanism that this plugin uses.
#
# It should also be noted that not all commands defined by packages are meant
# to be used by the user directly in any meaningful capacity, but this plugin
# has no way of differentiating those from "normal" commands

import inspect
import textwrap
import re
import sys


from sublime_plugin import application_command_classes
from sublime_plugin import window_command_classes
from sublime_plugin import text_command_classes


cmd_types = {
    "app": {
        "name": "ApplicationCommand",
        "commands": application_command_classes
    },
    "wnd": {
        "name": "WindowCommand",
        "commands": window_command_classes
    },
    "txt": {
        "name": "TextCommand",
        "commands": text_command_classes
    }
}


def trim_docstring(docstring):
    """
    This is taken from PEP257, and was slightly modified to work with Python 3
    (and renamed), but is otherwise included verbatim.

        https://www.python.org/dev/peps/pep-0257/
    """
    if not docstring:
        return ''

    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)



class GenerateCommandListCommand(sublime_plugin.WindowCommand):
    """
    Generate a list of all commands, their arguments and their doc strings to a
    buffer. The list of commands is displayed ordered under the package that
    defined them.
    """
    arg_re = re.compile(r"^\(self(?:, )?(?:edit, |edit)?(.*)\)$")

    def run(self):
        cmd_dict = {}
        for cmd_type, cmd_info in cmd_types.items():
            self.get_commands(cmd_type, cmd_info["commands"], cmd_dict)

        pkg_list = sorted(cmd_dict.keys())

        # Don't include the sublime_plugin module since it only contains the
        # stub classes for commands.
        if "sublime_plugin" in pkg_list:
            pkg_list.remove("sublime_plugin")

        # Default should always be first (and always exist).
        pkg_list.remove("Default")
        pkg_list.insert(0, "Default")

        # User should always be last (if it exists).
        if "User" in pkg_list:
            pkg_list.remove("User")
            pkg_list.append("User")

        self.view = self.window.new_file()
        self.view.set_scratch(True)
        self.view.set_name("Command List")

        for pkg in pkg_list:
            self.dump_package(pkg, cmd_dict[pkg])

        self.view.set_read_only(True)

    def dump_package(self, pkg_name, pkg_cmd_list):
        """
        Output the commands from a particular package to the output view,
        skipping any categories that don't contain any commands. The indent in
        the output is controlled by the tab size set in view.
        """
        indent_size = self.view.settings().get("tab_size", 4)
        indent = " "*indent_size

        self.append("{pkg}\n{sep}\n".format(
            pkg=pkg_name,
            sep=len(pkg_name)*"="))

        for cmd_type in sorted(cmd_types.keys()):
            cmd_type_name = cmd_types[cmd_type]["name"]
            cmd_list = pkg_cmd_list[cmd_type]

            if cmd_list:
                self.append("{indent}{typename}\n{indent}{sep}\n".format(
                    typename=cmd_type_name,
                    sep="-"*len(cmd_type_name),
                    indent=indent))

                for pkg_info in cmd_list:
                    self.append("{indent}{pkg}.{mod}.{cmd} {args}\n{doc}\n".format(
                        pkg=pkg_name,
                        mod=pkg_info.get("mod"),
                        cmd=pkg_info.get("name"),
                        args=pkg_info.get("args"),
                        doc=textwrap.indent(pkg_info.get("docs"), indent*3),
                        indent=indent*2))

        self.append()

    def append(self, line=""):
        """
        Append the text provided to the current output view in this window,
        followed by a newline character.
        """
        self.view.run_command("append", {"characters": line + "\n"})

    def get_commands(self, cmd_type, commands, cmd_dict_out):
        """
        Given a list of commands of a particular type, decode each command in
        the list into a dictionary that describes it and store it into the
        output dictionary keyed by the package that defined it.

        The output dictionary gains keys for each package, where the values are
        dictionaries which contain keys that describe the commands of each of
        the supported typed.
        """
        for command in commands:
            decoded = self.decode_cmd(command, cmd_type)
            pkg = decoded["pkg"]
            if pkg not in cmd_dict_out:
                cmd_dict_out[pkg] = {
                    "app": [],
                    "wnd": [],
                    "txt": []
                }

            cmd_dict_out[pkg][cmd_type].append(decoded)

    def decode_cmd(self, command, cmd_type):
        """
        Given a class that implements a command of the provided type, return
        back a dictionary that contains the properties of the command for later
        display.
        """
        return {
            "type": cmd_type,
            "pkg": command.__module__.split(".")[0],
            "mod": ".".join(command.__module__.split(".")[1:]),
            "name": self.get_name(command),
            "args": self.get_args(command),
            "docs": self.get_docs(command)
        }

    def get_args(self, cmd_class):
        """
        Return a string that represents the arguments to the run method of the
        Sublime command class provided, edited to remove the internal python
        arguments that are not needed to invoke the command from Sublime.
        """
        args = str(inspect.signature(cmd_class.run))
        return self.arg_re.sub(r"{ \1 }", args)

    def get_docs(self, cmd_class):
        """
        Return a formatted doc string for the command class provided, filling
        in a default for any command that does not have one defined on its own.
        """
        docstr = cmd_class.__doc__ or "No command description available"
        return textwrap.dedent(trim_docstring(docstr))

    def get_name(self, cmd_class):
        """
        Return the internal Sublime command name as Sublime would infer it from
        the name of the implementing class. This is taken from the name()
        method of the underlying Command class in sublime_plugin.py.
        """
        clsname = cmd_class.__name__
        name = clsname[0].lower()
        last_upper = False
        for c in clsname[1:]:
            if c.isupper() and not last_upper:
                name += '_'
                name += c.lower()
            else:
                name += c
            last_upper = c.isupper()
        if name.endswith("_command"):
            name = name[0:-8]
        return name
