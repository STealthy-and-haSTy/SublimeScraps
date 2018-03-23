### ---------------------------------------------------------------------------


from .core.startup import initialize
from .sublime import commands, events

__version_tuple = (1, 0, 0)
__version__ = ".".join([str(num) for num in __version_tuple])


### ---------------------------------------------------------------------------


__all__ = [
    "initialize",
    "commands",
    "events",
    "version"
]


### ---------------------------------------------------------------------------


def version():
    """
    Get the version of the installed dependency package as a tuple. This is
    used during the bootstrap check to see if the version of the dependency has
    changed.
    """
    return __version_tuple


### ---------------------------------------------------------------------------
