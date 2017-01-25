import sublime
import sublime_plugin
import os

class ScratchBufferCommand(sublime_plugin.WindowCommand):
    """
    Create a scratch view with the provided syntax already set. A default title
    is selected based on the syntax.
    """
    def run(self,
            syntax="Packages/Text/Plain text.tmLanguage"):

        view = self.window.new_file ()
        view.set_name ("Scratch: {}".format (os.path.splitext (os.path.basename (syntax))[0]))

        view.set_scratch (True)
        view.assign_syntax (syntax)
        view.settings ().set ("is_temp_scratch", True)

class ScratchBufferListener(sublime_plugin.EventListener):
    """
    Detect when a scratch buffer created by us is saved and turn off the scratch
    setting so that Sublime will warn about changes being lost if the tab is
    closed.

    This presumes that if you save a scratch buffer to disk it is because you
    care about the contents.
    """
    def on_post_save(self,view):
        if view.is_scratch () and view.settings ().get ("is_temp_scratch", True):
            view.set_scratch (False)
