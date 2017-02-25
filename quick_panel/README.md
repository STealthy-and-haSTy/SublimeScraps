Quick Panel
-----------

The python files in this directory are simple code samples for using the quick
panel API in Sublime text to display a list of items to the user. Since these
are samples, they don't perform a useful task, instead pointing out how you
might go about using the panel in a particular way.

Unlike some of the other items, unless otherwise noted the code samples here
are examples I worked up for my own use. This means that they don't contain a
link to further reading and instead have more verbose comments to describe how
to use them.

Note that there is no example here on the simplest use of the quick panel (i.e.
just presenting a single list of items), as such an example is available with
Sublime Text itself in the file `Packages\Default\quick_panel.py`.

### Usage

At the time of writing, each Python file contains a single Sublime Text command
(and any other required supporting code) which shows how to present the quick
panel in a certain way.

As they are examples they only show you how to present the panel and allow a
particular use case, leaving it up to you to decide what to do with the
information on what item was eventually selected.

### What they does

 * [nested_panel.py](nested_panel.py) is an example of displaying a hierarchy of
   items in a quick panel. Normally the list presents itself with a single list
   of items, but here each item can trigger opening a new list of sub items or
   allow you to go back to a previous level.
