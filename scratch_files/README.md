Scratch Files
-------------

I've been using Sublime Text for less than a year and it's already become an
indispensable tool for my every day use. Not only do I use it for all of my
code and text editing, I also use it for temporary scratch pads when I'm
working on stuff.

Often, when helping people out with problems they might be having it is
required to come up with a code sample or simply play around with sample text.
Although it is simple to create a new view and set the syntax using a keystroke
and the command palette, that leaves you with a file that you get asked to save
when you probably don't care.

This simple blob of code adds some commands to the command palette that create
a view, set the appropriate syntax and mark it as a scratch buffer so that it
can be closed with impunity. An event listener catches attempts to try and save
the file and turns off the scratch setting on save so that the buffer is just
an ordinary one again.

Although this is simple and probably useful to only me, I hold this as a great
example of how easy it is to improve your work flow in Sublime Text.

### Usage

The simplest way to use this would be to drop this entire folder into your
Sublime Text `Packages` folder, where it will become a package.

The important part of this is the python source file. If desired you can just
put it directly into some package (e.g. your `User` package) and use it that
way. It adds a command called `scratch_buffer` that takes an argument of
`syntax`, which should point to the name of a syntax that you want.

The default value for this argument if you do not provide it is
`"Packages/Text/Plain text.tmLanguage"`. It is also possible to explicitly pass
`None` for this argument, which will cause the command to prompt you for the
syntax to use first.

If you're using build 3154 or later of Sublime Text and invoke the the
`scratch_buffer` command from the command palette with this argument set to
`None`, the selection of the syntax will happen directly in the command
palette.

In all other cases the syntax selection is done via a quick panel instead.

The folder also contains a `sublime-commands` file which adds a variety of
languages to the command palette. You can use this as is, merge it with your
own, add often used syntaxes, etc.

It is also possible to map this command to a key press, if you have a particular
syntax that you use often for example.