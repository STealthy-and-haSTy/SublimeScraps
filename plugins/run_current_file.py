import sublime_plugin

# Related reading:
#     https://forum.sublimetext.com/t/concatenating-string-arguments-in-key-bindings/20983/


class RunCurrentFileCommand (sublime_plugin.WindowCommand):
    """
    Replace the extension of the current file with the one passed in to the
    command (default is ".exe") and use the exec command to execute it.

    The working directory is set to the firectory that the file is in.
    """
    def run(self, extension=".exe"):
        # Get vars and make sure that we have all of the ones we need
        vars = self.window.extract_variables ()
        if "file_base_name" in vars and "file_path" in vars:

            # The executable is the current file with a new extension stuck on
            executable = vars['file_base_name'] + extension

            # Make the working directory be the path of the current file
            working_dir = vars['file_path']


            self.window.run_command ("exec", {
                "cmd": [executable],
                 "working_dir": working_dir
                })
        else:
            sublime.status_message ("Error: No file")
