Sublime Scraps
--------------

This repository contains a mixed bag of simple Sublime Text 3 plugin examples
and customizations that are probably better stored as gists, but what can I
say, I'm a rebel.

Some of the contents are customizations that I use myself that others may
find useful, possibly as a jumping off point for their own user specific
customizations.

Others are small snippets of code that I've worked up in response to other
users questions (e.g. on the Sublime forum or Stack Overflow) that I have been
keeping in my User package.

Everything provided here is without warranty and with the proviso that as a C
programmer and not a Python programmer, much of this is probably ugly to the
gurus out there. Also some code is meant to be proof of concept and thus may
not cover all use cases or scenarios.

The layout of the files here is:

 * [customizations](customizations/README.md) contains files that I keep in my
   own `User` package that I use day to day. This does not include my settings,
   however.

 * [macros](macros/README.md) contains some sample macros (commented with an
   associated key binding) which illustrate how easy it is to customize Sublime
   to work your way.

 * [snippets](snippets/README.md) contains sample snippets that I have in my
   user package that others may find useful. Maybe. Probably not.

 * [scratch_files](scratch_files/README.md) is a simple plugin that I use all
   the time when playing around with code samples. See the README in there for
   more information.

 * [config_popup](config_popup/README.md) is another simple plugin I made to
   make my life easier. It opens a small pop-up with configuration related
   entries only, including one for editing project specific settings. Handier
   than using the menu as not all of the options listed are in the command
   palette by default.

 * [indent_test](indent_test/README.md) is a simple prototype plugin that
   performs tests on the indent rules in Sublime in a manner similar to how
   the internal syntax file testing works.

 * [plugins](plugins/README.md) is a bunch of one-off plugin samples that I
   have worked up in response to helping others (great excuse to learn the
   Sublime API) to stop them from getting lost in the mists of time, although
   I'm sure nobody would notice if they did.

 * [quick_panel](quick_panel/README.md) is a list of examples for using the
   Sublime text `quick_panel` in more complex ways than just a simple list of
   text.

 * [build_enhancements](build_enhancements/README.md) is similar to
   [plugins](plugins/README.md) except that here the commands are for modifying
   how a `sublime-build` file is used. This allows for things like custom
   variables in command lines and selecting the command to build at runtime
   instead of hard coding it.

 * [session_cleaner](session_cleaner/README.md) is a Python script that cleans
   the recent workspaces section of the `Session.sublime_session` file so that
   projects that no longer exist don't show up in the project switch panel.

 * [package_bootstrap](package_bootstrap/README.md) is example code that shows
   how one might construct a Sublime Text dependency that contains Sublime
   resources and have the dependency bootstrap those resources into a
   `sublime-package` package file and keep it up to date.
