import sublime
import sublime_plugin
import os



st_ver = int(sublime.version())
HandlerBase = sublime_plugin.ListInputHandler if st_ver >= 3154 else object


def _syntax_name(syntax_res):
    syntax_file = os.path.basename(os.path.split(syntax_res)[1])
    return os.path.splitext(syntax_file)[0]


class SyntaxListInputHandler(HandlerBase):
    """
    Input handler for the syntax argument of the scratch_buffer command; allows
    for the selection of one of the available syntaxes.
    """
    def name(self):
        return "syntax"

    def placeholder(self):
        return "Buffer Syntax"

    def parse(self, langs, resource_spec):
        for syntax in sublime.find_resources(resource_spec):
            langs[_syntax_name(syntax)] = syntax

    def list_items(self):
        langs = {}

        self.parse(langs, "*.tmLanguage")
        self.parse(langs, "*.sublime-syntax")

        return [(syntax, langs[syntax]) for syntax in sorted(langs.keys())]


class ScratchBufferCommand(sublime_plugin.WindowCommand):
    """
    Create a scratch view with the provided syntax already set. If syntax is
    None, you get prompted to select a syntax first.
    """
    def run(self, syntax=None):
        if syntax is None:
            return self.query_syntax()

        view = self.window.new_file()
        view.set_name("Scratch: %s" % _syntax_name(syntax))

        view.set_scratch(True)
        view.assign_syntax(syntax)
        view.settings().set("is_temp_scratch", True)

    def input(self, args):
        if args.get("syntax", None) is None:
            return SyntaxListInputHandler()

    def input_description(self):
        return "Scratch Buffer"

    def query_syntax(self):
        items = [list(val) for val in SyntaxListInputHandler().list_items()]

        def pick(idx):
            if idx != -1:
                self.new_view(items[idx][1])

        self.window.show_quick_panel(
            items,
            on_select=lambda idx: pick(idx))


class ScratchBufferListener(sublime_plugin.EventListener):
    """
    When a scratch buffer is saved, turn off the scratch setting so that further
    changes do not get lost on accidental close.
    """
    def on_post_save(self, view):
        if view.is_scratch() and view.settings().get ("is_temp_scratch", True):
            view.set_scratch(False)
