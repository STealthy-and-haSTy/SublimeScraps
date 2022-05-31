import sublime
import sublime_plugin

import os

# Related reading:
#     https://stackoverflow.com/q/71255440/814803
#
# This plugin is based on a request made in the above stack overflow question
# for a method by which you can add the path of the current file to the side
# bar.
#
# This plugin will allow for that, and supports versions of Sublime Text all
# the way back to version 2 (which is the version the question asker uses). It
# defines a command that will examine the path of the currently active file and
# then, if it's not already open in the side bar, add it.
#
# To use this in Sublime Text 2, you need to adjust the value of the _subl_path
# variable to point to your Sublime Text 2 executable; for ST3 and above the
# plugin will use the native plugin API instead.
#
# To use the plugin from the context menu, create a file named
# Context.sublime- menu in your User package and give it the following content
# (or add the command to an existing file, if you have one).
#
# [
#     { "caption": "-", "id": "file" },
#     { "command": "add_file_folder_to_side_bar", "caption": "Add Folder to Side Bar",}
# ]
#
# If you prefer a key binding, you can add one such as the following:
#
# { "keys": ["ctrl+alt+a"], "command": "add_file_folder_to_side_bar"},


# This needs to point to the "sublime_text" executable for your platform; if
# you have the location for this in your PATH, this can just be the name of the
# executable; otherwise it needs to be a fully qualified path to the
# executable.
_subl_path = "/home/tmartin/local/sublime_text_2_2221/sublime_text"

def run_subl(path):
    """
    Run the configured Sublime Text executable, asking it to add the path that
    is provided to the side bar of the current window.

    This is only needed for Sublime Text 2; newer versions of Sublime Text have
    an enhanced API that can adjust the project contents directly.
    """
    import subprocess

    # Hide the console window on Windows; otherwise it will flash a window
    # while the task runs.
    startupinfo = None
    if os.name == "nt":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.Popen([_subl_path, "-a", path], startupinfo=startupinfo)


class AddFileFolderToSideBarCommand(sublime_plugin.WindowCommand):
    """
    This command will add the path of the currently focused file in the window
    to the side bar; the command will disable itself if the current file does
    not have a name on disk, or if it's path is already open in the side bar.
    """
    def run(self):
        # Get the path to the current file and add it to the window
        self.add_path(self.get_current_path())

    def is_enabled(self):
        """
        The command should only be enabled if the current file has a filename
        on disk, and the path to that file isn't already in the list of folders
        that are open in this window.
        """
        path = self.get_current_path()
        return path is not None and path not in self.window.folders()

    def get_current_path(self):
        """
        Gather the path of the file that is currently focused in the window;
        will return None if the current file doesn't have a name on disk yet.
        """
        if self.window.active_view().file_name() is not None:
            return os.path.dirname(self.window.active_view().file_name())

        return None

    def add_path(self, path):
        """
        Add the provided path to the side bar of this window; if this is a
        version of Sublime Text 3 or beyond, this will directly adjust the
        contents of the project data to include the path. On Sublime Text 2 it
        is required to execute the Sublime executable to ask it to adjust the
        window's folder list.
        """
        if int(sublime.version()) >= 3000:
            # Get the project data out of the window, and then the list of
            # folders out of the project data; either could be missing if this
            # is the first project data/folders in this window.
            project_data = self.window.project_data() or {}
            folders = project_data.get("folders", [])

            # Add in a folder entry for the current file path and update the
            # project information in the window; this will also update the
            # project file on disk, if there is one.
            folders.append({"path": path})
            project_data["folders"] = folders
            self.window.set_project_data(project_data)
        else:
            # Run the Sublime executable and ask it to add this file.
            run_subl(path)
