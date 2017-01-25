Macros
------

Is there more than one of these here? If so I probably forgot to update this
README file; shame on me.

Anyway, this macro is referenced from one of the key bindings in the
**customizations** folder, and it meant to be bound to whatever key you
normally use to toggle a line comment.

In JetBrains tools, that command will advance the cursor down a line when you
invoke it (unless text is selected), and this mimics that behavior. It's one of
the few things that I miss from using those tools.

### Usage

To use a macro, just drop it into some package (e.g. your `User` package) and
Sublime will notice it. You can put it inside of a folder inside of a package
if desired.

By default, Macros show up in the menu under `Tools > Macros` using a structure
that represents the package that they are stored in, and any folders that they
are inside of inside of the package.

See the **customizations** folder for an example of a key binding that maps to
a macro. You could also use the same command as is used there to add the macro
to the command palette if desired.