User Package Customizations
---------------------------

The files here are files that I keep in my `User` package that I use to
customize Sublime Text 3 to my whims and desires. There's nothing ground
breaking or earth shattering here.

However, since I use git to keep my `User` package backed up and synced across
all of my machines, and this repository started as a clone of that one, here we
are.

Note that I use Sublime Text over all three platforms and everything here will
work across all platforms. However, for the sake of brevity I included my
custom key bindings as a single file which has entirely the wrong name.

Should you actually be interested in the bindings themselves, I recommend
copying them to your own bindings file.

### Usage

With the exception of the `sublime-keymap` file, any of these files can be put
directly into your `User` package (or any other package) and they will take
effect. If you already have such a file, you should open both and copy the
entries from my files into yours so you don't lose your own customizations.

For the `sublime-keymap` file, you should copy the key bindings into your own
custom bindings, which are stored in a similar file but which contains the name
of your platform in it (e.g. `Default (Windows).sublime-keymap`) so that
Sublime knows what platform it is for.