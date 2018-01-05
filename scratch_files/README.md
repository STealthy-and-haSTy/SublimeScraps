Scratch Files
-------------

Often, when helping people out with problems they might be having it is
required to come up with a code sample or simply play around with sample text.
Although it is simple to create a new view and set the syntax using a keystroke
and the command palette, that leaves you with a file that you get asked to save
when you probably don't care.

This simple blob of code adds a command that creates a view, sets the
appropriate syntax and marks it as a scratch buffer so that it can be closed
with impunity.

An event listener catches a save on the scratch buffer and turns off the
scratch setting so that the buffer becomes an ordinary file buffer again,
stopping you from losing any work if you decide your scratch file should be
more permanent.


### Usage

The simplest way to use this would be to drop this entire folder into your
Sublime Text `Packages` folder, where it will become a package.

The important part of this is the python source file. If desired you can just
put it directly into some package (e.g. your `User` package) and use it that
way. It adds a command called `scratch_buffer` that takes an argument of
`syntax`, which should point to the name of a syntax that you want.

If no `syntax` argument is given, you will be prompted to select the
appropriate syntax from a quick panel containing of all syntaxes that Sublime
currently knows about before the buffer is created.

If you're using build 3154 or later of Sublime Text and invoke the
`scratch_buffer` command from the command palette with without specifying a
value for the `syntax` arg, the selection of the syntax will happen directly in
the command palette instead of a quick panel.

The folder also contains a `sublime-commands` file which adds a variety of
languages to the command palette. You can use this as is, merge it with your
own, add often used syntaxes, etc.

Additional uses of this could might be to add a menu item to create scratch
files or even bind the command to a key press if you happen to often create a
scratch file of a certain type.
