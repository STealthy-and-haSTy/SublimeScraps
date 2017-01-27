Config Popup
------------

As mentioned in the README for [scratch_files](../scratch_files/README.md), a
lot of the time while helping people with a problem, it is necessary to check
into a configuration file to get default settings, etc. Some (but not all)
options for this are available in the command palette, and it is annoying to
use the menu for this.

Come  to think of it, Sublime has taught me that the menu is evil in general
because it's not as smart as a fuzzy filtered command palette. So if you take
those reasons and add in my desire to also be able to easily edit project
specific settings **AND** wanting to play with the Sublime API, you get this.

Basically this is a simple pop-up that provides the most often used (by me)
configuration options. Additionally, if you have a project open, an option
appears to edit settings for this project as well, which will open up the
current project file in a split pane with the default settings on the left.

When editing a project in this manner, the code ensures that there is a
`settings` field in the project if there is not one already, so that you can
simply go in and add your settings without having to mess around with the
structure of the project itself.

This is ugly as all get out, and I have plans to ultimately try to pull all
configuration items from the menu into it, so it may get updated some day.

### Usage

The simplest way to use this would be to drop this entire folder into your
Sublime Text `Packages` folder, where it will become a package.

The important part of this is the python source file. If desired you can just
put it directly into some package (e.g. your `User` package) and use it that
way. It adds a command called `show_preferences_popup` that  does what it says
on the tin.

The key bindings in this file map `super+,` to this command, which on MacOS
overwrites the default key binding for opening the preferences with this
command. You can of course modify these as needed, delete them and use your
own, etc.