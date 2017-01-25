import sublime
import sublime_plugin

#
# The core preferences list.
#
g_core_prefs = [
    # This one opens up the global settings file.
    {
        "caption": "Core: Settings",
        "command": "edit_settings",
        "args":
        {
            "base_file": "${packages}/Default/Preferences.sublime-settings",
            "default": "// Settings in here override those in \"Default/Preferences.sublime-settings\",\n// and are overridden in turn by syntax-specific settings.\n{\n\t$0\n}\n"
        }
    },

    # Distraction free settings. These override the settings in the global settings above..
    {
        "caption": "Core: Settings – Distraction Free",
        "command": "edit_settings",
        "args":
        {
            "base_file": "${packages}/Default/Distraction Free.sublime-settings",
            "default": "{\n\t$0\n}\n"
        }
    },

    # Settings specific to the syntax being used in the current file. These
    # settings trump everything else.
    {
        "caption": "Core: Settings – Syntax Specific",
        "command": "edit_syntax_settings",
        "args": None
    },

    # Open up the configuration file for the current key bindings. This one is
    # specific to the current platform.
    {
        "caption": "Core: Key Bindings",
        "command": "edit_settings",
        "args":
        {
            "base_file": "${packages}/Default/Default ($platform).sublime-keymap",
            "default": "[\n\t$0\n]\n"
        }
    },

    # For completeness, open up the packages directory in the system file
    # browser.
    {
        "caption": "Core: Browse Packages",
        "command": "open_dir",
        "args":
        {
            "dir": "${packages}"
        }
    },
]

#
# Project settings
#
# Settings specific to the project; this actually opens up the project file
# so that the settings specific to it can be edited.
#
# A "user_file" argument will be added that points to the project file; The
# open_file command that is used in the menu to open up the project file
# expands ${project} to the project filename, but edit_settings does not.
#
g_proj_prefs = {
    "caption": "Project: Settings - Project Specific",
    "command": "edit_settings",
    "args":
    {
        "base_file": "${packages}/Default/Preferences.sublime-settings",
    }
}

class ShowPreferencesPopupCommand(sublime_plugin.WindowCommand):
    """
    Show a quick panel that includes just options specific to settings. Some of
    these already appear in the command palette, but not all of them.

    This also includes the ability to open the current project file, ensuring
    that it has a settings field if it does not already, so that it is easier
    to populate.
    """

    def on_select(self, items, index):
        if index >= 0:
            if "Project" in items[index]["caption"]:
                project_data = self.window.project_data ()

                if "settings" not in project_data:
                    project_data["settings"] = {}
                    self.window.set_project_data (project_data)

            self.window.run_command (items[index]["command"], items[index]["args"])

    def build_preference_list(self):
        global g_core_prefs
        global g_proj_prefs

        preference_list = list(g_core_prefs)

        if self.window.project_file_name () is not None:
            entry = dict (g_proj_prefs)

            entry["args"]["user_file"] = self.window.project_file_name ()
            preference_list.append (entry)

        return preference_list

    def run(self):
        item_list = self.build_preference_list ()
        self.window.show_quick_panel (
            items=[item["caption"] for item in item_list],
            on_select=lambda index: self.on_select(item_list, index))
