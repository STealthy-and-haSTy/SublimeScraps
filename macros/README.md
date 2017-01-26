Macros
------

One of the features of Sublime that people seem to forget about sometimes is the
macro facility. A combination of a simple macro along with a suitable keyboard
shortcut is a powerful way to enhance your editing experience.

Here there are the following simple macros:

 * **comment_line** can be used to modify the functionality of toggling a line
   comment by having the cursor advance to the next line after the current line
   is toggled.

 * **xml_line_comment** is an example of using a macro and a key binding to
   make Sublime comment multiple lines of XML at once as single lines instead
   of as a group.

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