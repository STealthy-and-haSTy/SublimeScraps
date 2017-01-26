import sublime
import sublime_plugin
import os

# Related Reading:
#     https://forum.sublimetext.com/t/displaying-project-name-on-the-rite-side-of-the-status-bar/24721

# This just displays the filename portion of the current project file in the
# status bar, which is the same text that appears by default in the window
# caption.

def plugin_loaded ():
    """
    Ensure that all views in all windows show the associated project at startup.
    """
    # Show project in all views of all windows
    for window in sublime.windows ():
        for view in window.views ():
            show_project (view)

def show_project(view):
    """
    If a project file is in use, add the name of it to the start of the status
    bar.
    """
    if view.window() is None:
        return

    project_file = view.window ().project_file_name ()
    if project_file is not None:
        project_name = os.path.splitext (os.path.basename (project_file))[0]
        view.set_status ("00ProjectName", "[" + project_name + "]")

class ProjectInStatusbar(sublime_plugin.EventListener):
    """
    Display the name of the current project in the status bar.
    """
    def on_new(self, view):
        show_project (view)

    def on_load(self, view):
        show_project (view)

    def on_clone(self, view):
        show_project (view)
