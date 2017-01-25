import sublime, sublime_plugin, webbrowser

# Related reading:
#     https://forum.sublimetext.com/t/how-does-the-open-url-command-select-the-browser-to-use/21590


class OpenUrlCommand(sublime_plugin.WindowCommand):
    """
    Override the build in `open_url` command. This command is used from the Help
    menu, but under Linux it does not select the correct browser.

    This fixes the problem and is fairly low risk since it's not used anywhere
    in the Default package.
    """
    def run(self, url):
        webbrowser.open_new_tab (url)