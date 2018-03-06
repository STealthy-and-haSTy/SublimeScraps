When the included bootstrap code determines that it needs to update the
bootstrapped version of the package for any reason, the contents of this folder
become the contents of the created `sublime-package` file.

Generally, the entire contents of this folder (and all sub-folders) will be
added directly to the generated package, with the following exceptions:

 1. The file [bootstrap.py](bootstrap.py) is modified as it is added to the
    package to set the `__core_version_tuple` variable to the version of the
    dependency that is creating the bootstrap package; that is, the created
    package inherits the version of the dependency that created it.

 2. Files are added with the same name that they are seen here, but any that
    have an extension of `.sublime-ignored` will have that suffix removed 
    before they are added to the package. This keeps Sublime from seeing those
    files as potential resources in cases where the dependency is stored
    inside of the `Packages` folder.
