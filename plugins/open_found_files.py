import sublime
import sublime_plugin

# Related reading:
#     http://stackoverflow.com/questions/40088877/sublime-text-open-all-files-containing-search-term


class OpenAllFoundFilesCommand(sublime_plugin.TextCommand):
    """
    Collect the names of all files from a Find in Files result and open them
    all at once, optionally in a new window.
    """
    def run(self, edit, new_window=False):
        # Collect all found filenames
        positions = self.view.find_by_selector ("entity.name.filename.find-in-files")
        if len(positions) > 0:
            # Set up the window to open the files in
            if new_window:
                sublime.run_command ("new_window")
                window = sublime.active_window ()
            else:
                window = self.view.window ()

            # Open each file in the new window
            for position in positions:
                window.run_command ('open_file', {'file': self.view.substr (position)})
        else:
            self.view.window ().status_message ("No find results")