Self Bootstrapping Dependency Example
-------------------------------------

[Package Control](https://packagecontrol.io/) allows you to create and
distribute a [dependency](https://packagecontrol.io/docs/dependencies) package,
which allows you to access Python modules that aren't built into the Python
interpreter that ships with Sublime.

Generally speaking, such a dependency cannot contain any Sublime specific
resources such as syntaxes or plugins because due to the way that Package
Control installs dependencies, there is no guarantee that Sublime will be able
to see all of the required files.

This folder provides some example code that shows how you could create a
dependency that is capable of creating a bootstrapped version of some of its
contents into a `sublime-package` file, allowing it to contain such resources
safely.

This assumes that you want your dependency to be available as a standard
dependency (say some library of code) while also presenting some facet of
itself to Sublime as a regular package, and so the sample code is laid out in
a way that illustrates how to keep core code in the dependency and access it
while still bootstrapping.

The same mechanism as is used here could also be used to just put all
functionality into a bootstrapped package without leaving any in the dependency
by putting all of the related files into the `1_my_package` folder (see below).

An example of this might be a dependency which provides a custom context
listener for key bindings that many packages might want to use without having
to implement it themselves.

---

**Note:** The contents and structure of this folder are not directly suitable
for a dependency and are provided here as they are for illustrative purposes.
The actual structure you need varies depending on whether or not you need any
platform specific support or not.

Read the documentation on
[dependencies](https://packagecontrol.io/docs/dependencies) for more
information on the required structure.

---


The Bootstrapped Package Name
-----------------------------

In this sample, the name of the package that's created is `1_my_package`, and
is referenced as such throughout this README and throughout the code in
general.

Since Sublime loads packages in lexical order, creating a package with a number
in the same ensures that the package loads prior to other packages. Depending on
your use case, this may or may not be important to you.

The [bootstrapper.py](core/bootstrapper.py) file contains a variable you can
change to alter the name of the generated `sublime-package` file. All of the
code responsible for generating a new package and checking the version of an
existing package uses that variable to know what to do.

You can change this to anything you wish, but keep in mind that it shouldn't be
a name of an existing package (which includes your own dependency) or bad
things will happen. Additionally, the directory that contains the files to be
added to the bootstrapped package needs to match the value in the variable so
that the code knows where to look for files.

For more information on this process in general, see the section below on how
the code words.


Usage Requirements
------------------

Although a regular Python dependency is just providing access to a third party
library or other code functionality, in the specific case of a dependency that
bootstraps parts of itself out to a `sublime-package` file there are more
stringent requirements on code that actually depends on your dependency.

In particular, in order for the bootstrap to work, code has to be triggered at
Sublime startup so that it can be determined if a bootstrap needs to happen or
not (i.e. is the package missing or out of date and thus in need of update?).

The bootstrap process requires that the Sublime plugin environment be available,
so code that is using the dependency needs to include the following code (or
something similar):

```python
import my_dependency

def plugin_loaded():
    my_dependency.initialize()
```


How it works
------------

When Sublime starts and loads packages, one by one each package that depends on
your dependency will invoke the `initialize()` method as outlined above as a
part of their `plugin_loaded()` code.

The first time this is called, a check is performed to see if the bootstrap
needs to happen or not. Regardless of the results of this check, a flag is set
so that all other calls to the `initialize()` method in the same Sublime
session do nothing.

In order to determine if a bootstrap needs to happen, two things are checked:

 1. The existence of a bootstrapped `sublime-package` from a previous start,
    if any. If there is no existing package, a bootstrap has to happen to
    create one. Generally this happens the first time your dependency is
    imported or when the user deletes the bootstrapped version of the package.

 2. A version check is done to see if the existing bootstrapped package is
    older than the current version of the dependency, which would indicate that
    it contains older resources and needs to be updated.

These checks help to ensure that the data contained in the created
`sublime-package` file not only exist but are up to date as well. This means
that every time you modify the contents of the dependency, you need to update
its version information in order to ensure that everything updates correctly.


Bootstrapping
-------------

The bootstrap process itself is fairly simple. The following steps are carried
out in a background thread so that Sublime remains properly interactive while
the bootstrap is happening, which is transparent to the user.

  1. Add the package we're about to create or update to the `ignored_packages`
     setting so that Sublime won't try to load the files before the bootstrap
     is complete.

  2. Create a new copy of the `sublime-package` file in the
     `Installed Packages` folder; the package will contain the contents of the
     [1_my_package](1_my_package/) folder.

     During this process, any files with a suffix of `.sublime-ignored` are
     renamed to remove that suffix; this is used to stop Sublime from loading
     resource files from the dependency.

     Additionally, the `bootstrap.py` boiler plate code has the version number
     of the dependency injected into it so that the version check at startup
     knows what version of the dependency created the bootstrapped package.

  3. Remove the bootstrapped package from the `ignored_packages` setting so
     that Sublime will load it and make its contents available.

  4. Notify the user that the package has either been created or updated,
     depending on what happened.

     If the package was updated, this message tells the user that they should
     restart Sublime, since an update of an existing package means that the
     dependency may have changed. Restarting Sublime will allow it to reload
     the changed dependency so that everything is up to date.

     If the package was just created, the user can generally continue to work
     without a restart since this is the first time the dependency was loaded
     and thus everything is up to date already.


Extra Protections
-----------------

Along with being able to bootstrap an initial package and keep it up to date as
the dependency changes, the sample code also imposes the following extra
protective measure on the dependency code.

Depending on your needs and desires, these could be extended or removed
entirely.

  1. **Check at startup if the bootstrapped package is being ignored**

     If the package we've created is being ignored, it potentially means that
     something happened during the bootstrap that stopped it from completing,
     such as the user restarting Sublime before the update was complete.

     In such a case, things are left in an inconsistent state and may not be
     what the user expects. To counter this, if this is detected at startup the
     user is notified and told to remove the package from the list of ignored
     packages.

     The sample code provides an optional setting that the user can apply in
     order to block the warning, which is needed to actually ignore the
     bootstrapped package if you meant to do so intentionally.

     This is an extra step to take but also ensures that the user is fully
     aware of the consequences of what they're doing so that they're not
     surprised later.

  2. **Check at startup if the bootstrapped package is unpacked**

     If the package we've created also existed as an unpacked folder in the
     `Packages` folder, Sublime will load the contents of that folder instead
     of the contents of the `sublime-package` file.

     When this is the case we can no longer properly keep things updated
     because no matter how much we modify the `sublime-package`, the files it
     contains won't get read.

     For this reason the sample code displays a warning dialog box at startup
     when this is detected in order to alert the user to possible problems.

     As with the ignored package check, the sample has an optional setting the
     user can apply to stop this warning, again so that they are made fully
     aware of the consequences of what they're doing.

  3. **Protection from package resources going away**

     During the part of the bootstrap which ignores and un-ignores the
     bootstrapped package, a check is done to see if resources provided by the
     package are currently in use in a way that is going to cause problems when
     the package is ignored.

     For example, if the bootstrapped package contains a syntax definition and
     there is currently a file open which uses that syntax, once we ignore the
     package Sublime will generate an error message to warn you that the syntax
     is missing.

     In order to stop this from happening, before the package is ignored all
     such views are found and have their syntax set to `Plain text`. Once the
     package is un-ignored, the syntax is set back to what it used to be.

     In the sample code only syntax definitions are handled this way. If your
     dependency contains a theme or color scheme, you would also need to take
     special action for those files as well.
