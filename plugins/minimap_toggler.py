import sublime, sublime_plugin

# Related reading:
#     https://forum.sublimetext.com/t/disable-sublime-minimap-for-a-specific-syntax/21458

# The idea of this plugin is to provide a setting that allows for the minimap to
# be hidden for certain file types. There is no built in setting for this as the
# minimap being displayed or not is specific to a window and not to a file, so
# it's either on or off for all files in the window.
#
# In order to use this, you need to open the syntax specific settings for the
# file type that you would like to hide the minimap for and add the following
# setting:
#    "hide_minimap": true


# Sublime versions 3116 and higher have new functionality for determining
# if the minimap is visible or not without having to resort to some hackery.
ST3116 = int(sublime.version()) >= 3116

class MiniMapToggler(sublime_plugin.EventListener):
    """
    Catch events for views being activated and deactivated, and based on a
    setting, show or hide the minimap.

    This requires that you set the "hide_minimap" setting to true in the
    syntax specific settings for any syntaxes you do not want the minimap
    displayed for.
    """

    # Invoked when a view is deactivated. This triggers prior to the newly
    # activated view becoming active.
    def on_deactivated(self, view):
        # Ignore deactivations of panels
        if view.settings ().get ("is_widget", False):
            return

        # If the option says we should hide the minimap and it's not currently
        # visible, then assume we hid it when we were activated and show it now.
        if (view.settings ().get ("hide_minimap", False) and
                self.is_minimap_visible (view) == False):
            view.window ().run_command ("toggle_minimap")

    # Every time a view is activated. This triggers after the previous
    # view has been deactivated
    def on_activated(self, view):
        # Ignore activations of panels
        if view.settings ().get ("is_widget", False):
            return

        # If the option says we should hide the minimap and it's currently
        # visible, then hide it.
        if (view.settings ().get ("hide_minimap", False) and
                self.is_minimap_visible (view)):
            view.window ().run_command ("toggle_minimap")

    # Check to see if the minimap is currently visible. This takes a view but
    # minimap visibility is a per-window setting, so the view is just used to
    # get at the window.
    #
    # This code is lifted from the DistractionFreeWindow plugin by aziz.
    #     https://github.com/aziz/DistractionFreeWindow/blob/master/distraction_free_window.py
    def is_minimap_visible(self, view):
      if ST3116:
          return view.window().is_minimap_visible()
      else:
          v = view.window().active_view()
          state1_w = v.viewport_extent()[0]
          v.window().run_command("toggle_minimap")
          state2_w = v.viewport_extent()[0]
          v.window().run_command("toggle_minimap")
          if state1_w and state2_w:
              return (state1_w < state2_w)