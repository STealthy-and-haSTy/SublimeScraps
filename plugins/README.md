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

### What they does

 * **minimap_toggler.py** is a simple example of having the sublime text
   minimap turn itself off only for files of a certain syntax. There is no
   setting that controls this, and the minimap toggles on and off on a
   window-by-window basis (not view-by-view), so some chicanery is needed to
   pull this off.

 * **open_found_files.py** is an example of collecting all of the files that
   had a match as a part of a Find in Files operation and opening them all at
   once. Normally in order to do this you would have to scroll through and
   click on each file to open it.

   The command presented should be bound to a key and can optionally open a new
   window and open the files there, instead of opening them in the current
   window.

 * **project_in_statusbar.py** is a simple example of adding text to the status
   bar in Sublime text. In this case, it adds the name of the current project
   file, which is already displayed in the Sublime title bar.

   The code tries to ensure that the project name is the first thing in the
   status line, although this could easily be modified to make it the last item
   as well.

 * **shebanger.py** is a command that is meant to be used as the `target`
   inside of a build system. It's a proof of concept that is rather naive, but
   the idea is that it would run the current python file using the interpreter
   that is in the shebang line of the current file instead of the version in
   the build system.

   This is naive for a few reasons, but is a good proof of concept for how
   one would bridge together a standard Sublime build system with some custom
   handling.

 * **python_build.py** is similar to **shebanger.py** except that here the
   method is slightly different. Here the interpreter to use is stored as one
   of two options in the build system, and the first line of the file selects
   which one the build uses.

   Same potato, different bag. (is that a saying? It should be if it's not.)

 * **run_current_file** came about when someone wanted to bind a key that would
   try to execute a file based on the name of the current file. For example if
   you were editing *cool.c* it would try to execute *cool.exe*.

   Turns out that build variable substitutions are not applied in most standard
   commands. This shows how one could go about making such a command.