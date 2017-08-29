import sublime
import sublime_plugin
import os


class ScratchBufferCommand(sublime_plugin.WindowCommand):
    """
    Create a scratch view with the provided syntax already set. If syntax is
    None, you get prompted to select a syntax first.
    """
    def run(self,
            syntax="Packages/Text/Plain text.tmLanguage"):

        if syntax is None:
            return self.query_syntax()

        view = self.window.new_file()
        view.set_name("Scratch: %s" % self.syntax_name(syntax))

        view.set_scratch(True)
        view.assign_syntax(syntax)
        view.settings().set("is_temp_scratch", True)

    def syntax_name(self, syntax):
        syntax_file = os.path.basename(os.path.split(syntax)[1])
        return os.path.splitext(syntax_file)[0]

    def pick(self, langs, name, idx):
        if idx != -1:
            self.window.run_command("scratch_buffer", {"syntax": langs[name]})

    def parse(self, langs, resource_spec):
        for syntax in sublime.find_resources(resource_spec):
            langs[self.syntax_name(syntax)] = syntax

    def query_syntax(self):
        langs = {}

        self.parse(langs, "*.tmLanguage")
        self.parse(langs, "*.sublime-syntax")

        captions = [[syntax, langs[syntax]] for syntax in sorted(langs.keys())]

        self.window.show_quick_panel(
            captions,
            on_select=lambda idx: self.pick(langs, captions[idx][0], idx))


class ScratchBufferListener(sublime_plugin.EventListener):
    """
    When a scratch buffer is saved, turn off the scratch setting so that further
    changes do not get lost on accidental close.
    """
    def on_post_save(self, view):
        if view.is_scratch() and view.settings().get ("is_temp_scratch", True):
            view.set_scratch(False)
