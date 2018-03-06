This folder represents the contentds of your dependency package that aren't
Sublime Commands or Event Handlers (which should be in the
[sublime](../sublime/) folder) or other Sublime resources that should be
injected into the bootstrapped package (in the [1_my_package](../1_my_package)
folder).

For example, your needs for a self bootstrapping dependency might require some
core library code to exist, along with other Sublime resources that take
advantage of that library; said library code could be placed in this folder in
order to allow it to be accessed more easily.

This folder also contains two files used during the bootstrap:

 1. The file [startup.py](startup.py) contains the `initialize` function that 
    is used by the packages that depend on your dependency, which is what
    ensures that everything is up to date and bootstraps as needed.

 2. The file [bootstrapper.py](bootstrapper.py) contains the actual bootstrap
    code. This spawns a background thread that first adds the package that 
    will be bootstrapped to the list of ignored packages, creates a new version
    of the package, and then unignores it so that it will be reloaded.
