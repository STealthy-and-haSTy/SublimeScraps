Scratch Files
-------------

I've been using Sublime Text for less than a year and it's already become an
indispensible tool for my every day use. Not only do I use it for all of my
code and text editing, I also use it for temporary scratch pads when I'm working
on stuff.

Often, when helping people out with problems they might be having it is required
to come up with a code sample or simply play around with a sample. Although it
is simple to create a new view and set the syntax using a keystroke and the
command palette, that leaves you with a file that you get asked to save when you
probably don't care.

This simple blob of code adds some commands to the command palette that create a
view, set the appropriate syntax and mark it as a scratch buffer so that it can be
closed with impunity. An event listener catches attempts to try and save the
file and turns off the scratch setting on save so that the buffer is just an
ordinary one again.

Although this is simple and probably useful to only me, I hold this as a great
example of how easy it is to improve your workflow in Sublime Text.