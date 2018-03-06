This folder represents the the parts of your dependency package that contain
Sublime Text Commands and Event Handlers.

In order for Sublime to see commands and event handlers defined in your
dependency, the classes need to be imported by another package so that they're
seen by the Sublime runtime.

This job is taken up by the bootstrapped version of the package, which is
created from the contents of the [1_my_package](../1_my_package) folder. The
code in the [bootstrap.py](../1_my_package/bootstrap.py) plugin imports the
classes from this folder so that Sublime will see them.

The code for these items could also be included directly in the
[1_my_package](../1_my_package) folder as well if desired. Here we're doing it
this way as a demonstration of how you would go about something like this if
you want to.

For the purposes of this simple example there is a single command and event
handler defined in this folder for the purpose of displaying something to the
Sublime console and thus verifying that they are being seen properly.
