import sublime
import sublime_plugin

import os

from Default.exec import ExecCommand

# This is an example of a custom build target for executing a build using a
# Makefile, but for use in situations in which there could be any number of
# possible Makefiles, such as if there were multiple projects, etc.
#
# In use, the plugin provides a command that allows you to select a Makefile to
# use during the build by selecting it from the context menu in the side bar.
# The menu entry has a checkbox in it that will show as checked for the
# Makefile that will be used in the next build.
#
# When the build executes, it will have two extra variables that will expand
# out, 'selected_makefile' and 'selected_makefile_path' which specify the full
# path to the selected makefile and the location in which it's stored
# respectively.
#
# To use this plugin, you must create a file named "Side Bar.sublime-menu" in
# your User package with the following content; if you already have such a file
# then just add this entry. You can also change the caption text to be anything
# you like.
#
# [
#     { "caption": "Build with this Makefile",
#       "checkbox": true,
#       "command": "select_makefile",
#       "args": {"files": []},
#     },
# ]
#
# In use, your build system would use the two new variables to set up how the
# build should execute. An example of that based on the Makefile.sublime-build
# file that ships with Sublime is the following. It executes make telling it
# what Makefile to use, and also uses the Makefile location to set the working
# directory as appropriate.
#
# {
#     "target": "makefile_build",
#     "cancel": {"kill": true},
#
#     "shell_cmd": "make -f \\${selected_makefile}",
#     "working_dir": "\\${selected_makefile_path}",
#     "file_regex": "^(..[^:\n]*):([0-9]+):?([0-9]+)?:? (.*)$",
#
#     "selector": "source.makefile",
#     "syntax": "Packages/Makefile/Make Output.sublime-syntax",
#     "keyfiles": ["Makefile", "makefile"],
#
#     "variants":
#     [
#         {
#             "name": "Clean",
#             "shell_cmd": "make clean"
#         }
#     ]
# }


def _get_project_settings(window):
    """
    Get the project specific settinsg data for the provided window; this will
    work for any window since all windows carry project data.
    """
    project_data = window.project_data()
    return project_data.get('settings', {})


def _set_project_settings(window, settings):
    """
    Given a settings object, update the project data in the given window. If
    this is a window that contains an explicit project, the sublime-project
    file will be updated.
    """
    project_data = window.project_data() or {}
    project_data['settings'] = settings

    window.set_project_data(project_data)


class SelectMakefileCommand(sublime_plugin.WindowCommand):
    """
    This can be executed from the side bar context menu by right clicking on
    a Makefile and choosing the item. The selected Makefile is stored into the
    project specific settings for this window, so that it will persist.
    """
    def run(self, files=[]):
        settings = _get_project_settings(self.window)
        settings.update({
            'selected_makefile': files[0],
            'selected_makefile_path': os.path.dirname(files[0])
        })

        _set_project_settings(self.window, settings)

    def is_enabled(self, files=[]):
        # Only enabled for files named Makefile regardless of case; this could
        # be augmented to search within a list of possible names as well.
        return len(files) == 1 and os.path.basename(files[0]).upper() == 'MAKEFILE'

    def is_checked(self, files=[]):
        settings = _get_project_settings(self.window)
        return len(files) == 1 and files[0] == settings.get('selected_makefile', '')


class MakefileBuildCommand(ExecCommand):
    """
    Enhanced version of the internal exec command that can expand out variables
    that specify the selected Makefile and its location.
    """
    def run(self, **kwargs):
        kill = kwargs.get('kill', False)
        if kill:
            return super().run(kill=True)

        settings = _get_project_settings(self.window)
        variables = {
            'selected_makefile': settings.get('selected_makefile', ''),
            'selected_makefile_path': settings.get('selected_makefile_path', '')
        }

        if variables['selected_makefile'] == '':
            return sublime.error_message('No Makefile has been selected for this project')

        kwargs = sublime.expand_variables(kwargs, variables)
        super().run(**kwargs)
