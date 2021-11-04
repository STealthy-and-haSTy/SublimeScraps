import sublime
import sublime_plugin


class SelectionToTopCommand(sublime_plugin.TextCommand):
    """
    Jump the viewport in the file so that the selection is at the top of the
    file display area. Handy while conducting reviews.
    """
    def run(self, edit):
        position = self.view.sel()[0]

        offs = self.view.rowcol(position.begin())[0] * self.view.line_height()
        self.view.set_viewport_position((0.0, offs), True)

        self.view.sel().clear()
        self.view.sel().add(position)
