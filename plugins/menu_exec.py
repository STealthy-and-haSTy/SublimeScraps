import sublime
import sublime_plugin

from Default.exec import ExecCommand

# Related reading/viewing;
#     https://stackoverflow.com/questions/56934013/sublimetext-run-the-exec-with-current-file-as-arg-tab-context-menu
#     https://youtu.be/WxiMlhOX_Ng

# This plugin is a combination of an exec variant written for a stack overflow
# answer and one from my YouTube video on common custom build targets.
#
# The internal exec command can execute external programs, but unless it is
# invoked via the build command as a part of a build system, variables like
# $file and the like are not expanded. This makes key bindings or menu entries
# that want to execute specific tasks in context harder or impossible to do.
#
# In addition the exec command uses the global show_panel_on_build setting to
# open the build output, which may also not be desirable if you're executing
# ad-hoc programs.
#
# This variant of the command expands variables the same way as they would be
# expanded in a build system, and also supports a custom argument named
# show_panel that controls if the output panel should be displayed or not. A
# value of None honors the show_panel_on_build setting; set it to True or False
# to explicitly show or not show the panel.

class MenuExecCommand(ExecCommand):
    """
    A simple wrapper around the internal exec command that expands all of the
    normal build variables prior to the build, while also being able to
    temporarily suppress the build output panel if desired.
    """
    def run(self, show_panel=None, **kwargs):
        variables = self.window.extract_variables()

        for key in ("cmd", "shell_cmd", "working_dir"):
            if key in kwargs:
                kwargs[key] =  sublime.expand_variables(kwargs[key], variables)

        settings = sublime.load_settings("Preferences.sublime-settings")
        pref_var = settings.get("show_panel_on_build")

        show_panel = pref_var if show_panel is None else show_panel

        if show_panel != pref_var:
            settings.set("show_panel_on_build", show_panel)

        super().run(**kwargs)

        if show_panel != pref_var:
            settings.set("show_panel_on_build", pref_var)
