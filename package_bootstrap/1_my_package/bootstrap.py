import sublime
import textwrap
import traceback

try:
    # Importing these symbols in the top level of this file allows Sublime to
    # see them
    from package_bootstrap.sublime.commands import BootstrapTestCommand
    from package_bootstrap.sublime.events import BootstrapTestListener
    commands_ready = True

except Exception as e:
    commands_ready = False
    traceback.print_exc()


### ---------------------------------------------------------------------------


# When the bootstrapped system package is created or updated, the value of this
# tuple is updated to the version of the dependency that is doing the
# bootstrap.
#
# The bootstrap code looks specifically for this line, so don't modify it.
__core_version_tuple = (0, 0, 0)

__version_tuple = __core_version_tuple
__version__ = ".".join([str(num) for num in __version_tuple])


### ---------------------------------------------------------------------------


def plugin_loaded():
    """
    Warn the user if there was a problem importing the Sublime commands and
    event handlers from the dependency.
    """
    if not commands_ready:
        sublime.error_message(textwrap.dedent(
            """
            An error occurred while initializing my_package.

            All my_package commands will be disabled until the
            situation is resolved.

            If restarting Sublime does not clear the problem,
            please contact the developer with the contents of
            the Sublime Console.
            """).strip())


def plugin_unloaded():
    """
    This is stubbed out since this example doesn't need to know when it is
    being unloaded.
    """
    pass


def version():
    """
    Get the currently installed version of the bootstrapped version of the
    package as a tuple. This is used during the bootstrap check to see if the
    version of the dependency has changed since the bootstrapped package was
    created.
    """
    return __version_tuple


### ---------------------------------------------------------------------------
