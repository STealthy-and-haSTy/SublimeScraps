Indent Tester
-------------

This is a prototype plugin for performing tests on the internal indentation
rules that Sublime Text uses to automatically indent files as you type. This
allows you to verify that newly added indent rules make the changes that you
expected without having other effects.

This is provided as a build system with a custom target and associated plugin
command for performing the tests. The build system will be selected
automatically if the current build is set to automatic and the file being built
is an appropriate test file (see below). A variant in the build allows you to
test all indent rules at once.

In order to be recognized as an indent test file, all test files must have a
filename that starts with `indentation_test` and be stored somewhere within the
`Packages` folder. The remainder of the filename (and extension) can be
whatever you like.

Additionally, the first line of the file must contain a header similar to the
following example, marking the file explicitly as an indentation test file and
specifying the syntax of the contents of the file. The header may be preceded
by any text desired (e.g. the comment characters for the language in question).

An example might be the following file, named `indentation_test.c`:

```c
// INDENT TEST "Packages/C++/C.sublime-syntax"

#include <stdio.h>

int main(int argc, char const *argv[])
{
    int i= 0;

    if (i == 0)
        printf("I bet the %s complains about this\n",
            "compiler");

    return 0;
}
```

### Usage

The simplest way to use this would be to drop this entire folder into your
Sublime Text `Packages` folder, where it will become a package.

A new build system named `Indent Tests` is added to the `Tools > Build System`
menu, with a main build action that tries to test based on the current file and
a variant that will run all indent tests in all files.

In the first case the appropriate build will be automatically selected as long
as the build system is set to `Automatic` and you start the build from an
appropriate file as outlined above.

The build output displays the results of the tests. Any lines which fail the
test (i.e. which do not get indented to the same level as in the input file)
will be displayed in the build output, allowing you to quickly jump to the
appropriate source line.

### Caveats

As a prototype plugin, please note the following:

 * After a test, an output panel named `Output: Indent Test` is left behind,
   which will contain the contents of the last tested file. If you're running
   single tests, you can check the panel to see the final output.

 * As a place holder for potential future enhancements, when you run a test on
   a single file, all test files that use the same syntax are also tested as
   well. This could be easily disabled if desired, but is really only of note
   if you happen to have many indent tests for the same syntax.

 * Probably issues not listed here because they haven't been noticed/reported
   yet.
