Sample Plugin Code
------------------

The python files in this directory are simple plugin examples. Most originated
in response to people asking questions in the Sublime forums or on Stack
Overflow. I often take up such challenges as an excuse to hone my python skills
and my understanding of the Sublime Text API.

Each python file contains a link to the web page where I originally posted the
code, for further reading.

Except where noted (which is probably nowhere), you can consider this code an
example of how to achieve the effect that was originally asked about, but by no
means a final "production ready" version.

You can use the code here as an example for how aspects of Sublime work or as a
basis for something more useful.

### Usage

Generally, each python file is a self contained example of the required plugin
code. Some of them may require extra files to be placed somewhere. See inside
of each file for more information on full usage.

### What they do

 * [double_click.py](double_click.py) is an example of how to use the Sublime
   API to emulate a double click somewhere in the view. This involves
   converting a caret position offset to window coordinates and calling a built
   in command that handles mouse clicks. This is useful for cases where double
   clicking would otherwise be the only way to access some functionality, but
   one doesn't want to have to move a hand off the keyboard to the mouse.

 * [find_results_copy.py](find_results_copy.py) is an example of seamlessly
   expanding the capabilities of Sublime to make it work the way you want. This
   provides a command that allows you to copy whole result lines from a Find in
   Files result buffer and have the line numbers that precede the text be
   removed automatically.

 * [generate_cmd_list.py](generate_cmd_list.py) is a sample command that
   introspects the Sublime runtime environment and provides a textual display
   of all known commands (except for those implemented directly in the Sublime
   core), sorted out by package and type (`ApplicationCommand`, `WindowCommand`
   or `TextCommand`).

   Each command also includes the arguments the command takes and any defaults
   they might have, as well as the associated documentation comment.

 * [log_toggler.py](log_toggler.py) is an example `ApplicationCommand` that
   makes it easier to toggle the state of logging for commands, input and
   result regular expressions (useful for testing error capturing in a build
   system) without having to drop to the console. It's also a demonstration on
   how to use the `is_checked` and `description` methods of the command classes
   to give your command a default caption or display as checked in the menu.

 * [minimap_toggler.py](minimap_toggler.py) is a simple example of having the
   sublime text minimap turn itself off only for files of a certain syntax.
   There is no setting that controls this, and the minimap toggles on and off
   on a window-by-window basis (not view-by-view), so some chicanery is needed
   to pull this off.

 * [move_amount.py](move_amount.py) is a simple drop in replacement for the
   standard `move` command that allows you to specify the number of times the
   movement happens. This can be handy for certain kinds of navigation or in
   macros to make them more manageable if they contain a lot of motion.

 * [open_found_files.py](open_found_files.py) is an example of collecting all
   of the files that had a match as a part of a Find in Files operation and
   opening them all at once. Normally in order to do this you would have to
   scroll through and click on each file to open it.

   The command presented should be bound to a key and can optionally open a new
   window and open the files there, instead of opening them in the current
   window.

 * [project_in_statusbar.py](project_in_statusbar.py) is a simple example of
   adding text to the status bar in Sublime text. In this case, it adds the
   name of the current project file, which is already displayed in the Sublime
   title bar.

   The code tries to ensure that the project name is the first thing in the
   status line, although this could easily be modified to make it the last item
   as well.

 * [run_current_file.py](run_current_file.py) came about when someone wanted to
   bind a key that would try to execute a file based on the name of the current
   file. For example if you were editing *cool.c* it would try to execute
   *cool.exe*.

   Turns out that build variable substitutions are not applied in most standard
   commands. This shows how one could go about making such a command.

 * [set_status.py](set_status.py) is a small command that just adds a bit of
   text temporarily to the status bar. This allows you to create a macro that
   displays text in the status bar when you execute it.

 * [set_vc_vars.py](set_vc_vars.py) is a simple plugin for modifying the
   environment of Sublime while it's running to allow you to run Visual Studio
   commands in build systems.

 * [toggle_setting_ext.py](toggle_setting_ext.py) is a version of the internal
   sublime `toggle_setting` command that can toggle any setting between any
   value, instead of just toggling a boolean setting off and on.

 * [wrap_text.py](wrap_text.py) started as a simple plugin for reflowing
   multiline text so that it cuts off (hard wraps) at a predefined width, for
   example at a ruler. It was primarily designed for Python docstrings, but soon
   became apparant that some more related functionality would make it super
   useful - for example, wrapping line comments! - so it became quite a lot more
   advanced. It now also makes it easier to join consecutive comment lines
   together by pressing <kbd>delete</kbd> at the end of the first line.

 * [open_file_env.py](open_file_env.py) implements an enhanced version of the
   `open_file` command in Sublime that will expand all of the `sublime-build`
   variables as well as environment variables in it's `file` argument. Useful
   for creating key bindings or menu entries to open files in the context of
   your current project, for example.

 * [open_file_encoded.py](open_file_encoded.py) is an implementation of the
   `open_file` command in Sublime that allows you to encode a position to open
   the file at by adding `:line` or `:line:col` to the file name, as you can on
   the command line.

 * [menu_exec.py](menu_exec.py) is a simple `exec` command variant for running
   external tools from outside of build systems. It does what `exec` does, but
   also expands variables in its arguments like a `sublime-build`file  would.
   You can also stop the build output panel from displaying, if desired.

 * [scoped_snippet.py](scoped_snippet.py) is an enhanced version of the
   `insert_snippet` command that allows you to specify a scope where the
   snippet will apply, for use in menu or command palette entries, where it's
   not otherwise possible to constrain the scope.
