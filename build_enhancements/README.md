Build Enhancements
------------------

The python files in this directory are simple plugin examples of modifying the
Sublime Text build process to do something other than directly run a
pre-configured executable or script.

Each python file contains a link to the web page where I originally posted the
code, for further reading.

Except where noted (which is probably nowhere), you can consider this code an
example of how to achieve the effect that was originally asked about, but by no
means a final "production ready" version.

You can use the code here as an example for how aspects of Sublime work or as a
basis for something more useful.

### Usage

These plugins all define a new command to be used as a part of a build system.
To use them your `sublime-build` file needs to include a "target" option that
specifies the name of the replacement command. Different examples require extra
setup or modifications to the build file. Each file contains more information
on its specific use.

### What they does

 * [custom_build_variables.py](custom_build_variables.py) is an example showing
   how to provide our own custom build variables to the build system. This
   could be used to insert some project specific information easily into a
   build, for example.

 * [timeout_exec.py](timeout_exec.py) is a custom build target that is capable
   of cancelling a build automatically if it doesn't finish within a configured
   time delay. There are multiple versions here depending on which version of
   Sublime Text you're running.

 * [makefile_build.py](makefile_build.py) is a custom build target that allows
   you to select the Makefile to use from within your project by choosing it
   from the context menu in the side bar. If you use a project structure with
   multiple Makefiles in it for different aspects, you may find this useful.

 * [python_build.py](python_build.py) is an example of configuring a build
   system to have two different commands (here 32-bit and 64-bit versions of
   python) and having the first line in the file have text which tells the
   build which version to use.

 * [relative_python_exec.py](relative_python_exec.py) is a Python centric build
   system that allows you to execute a Python file based on it's module name
   instead of it's file name.

 * [redirect_exec.py](redirect_exec.py) is an example of a custom build target
   that generates a temporary file based on other information (in this case the
   contents of the current file) and then executes it. It also demonstrates
   detecting when a build has finished.

 * [shebanger.py](shebanger.py) is similar to **python_build.py** in that it
   determines what to use to perform the build from the first line of the
   current file. In this case that is a "shebang" line that directly specifies '
   the interpreter.

   Same potato, different bag. (is that a saying? It should be if it's not.)
