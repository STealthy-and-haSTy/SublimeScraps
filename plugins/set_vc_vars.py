import sublime
import sublime_plugin

from threading import Thread
from subprocess import Popen, PIPE
from os import environ

# Related reading;
#     https://stackoverflow.com/questions/39881091/how-to-run-sublimetext-with-visual-studio-environment-enabled/

# For the unfamiliar, Visual Studio ships with a batch file which sets up the
# environment variables you need to be able to run visual studio tools from a
# command prompt.
#
# This pluguin was written in response to someone that wanted to know how you
# could run Sublime and have it have the visual studio environment already set
# up.
#
# This plugin will use a subprocess to execute the batch file in the background
# and then issue the 'set' command to get the command interpreter to output the
# state of the environment before it exits.
#
# This output is gathered and parsed to come up with a dictionary similar to
# the environ table that python uses. From here we can easily detect what new
# environment variables were added and the values of those that changed, and
# set them as appropriate.
#
# As written Sublime needs to be restarted  in order to execute the batch file
# again. A more elegant solution would be to save the environment prior to
# modifying it so that it could be restored and a new environment applied.

# To use this, you need to specify a setting in your user preferences named
# 'vc_vars_cmd' which should contain a complete path to the batch file you want
# to execute. Optionally you can also specify 'vc_vars_arch', which will be
# passed as a command line argument to the batch file executed. Remember that
# the preferences are JSON, so you need to quote all path separators.

SENTINEL="SUBL_VC_VARS"

def _get_vc_env():
    """
    Run the batch file specified in the vc_vars_cmd setting (with an
    optional architecture type) and return back a dictionary of the
    environment that the batch file sets up.

    Returns None if the preference is missing or the batch file fails.
    """
    settings = sublime.load_settings("Preferences.sublime-settings")
    vars_cmd = settings.get("vc_vars_cmd")
    vars_arch = settings.get("vc_vars_arch", "amd64")

    if vars_cmd is None:
        print("set_vc_vars: Cannot set Visual Studio Environment")
        print("set_vc_vars: Add 'vc_vars_cmd' setting to settings and restart")
        return None

    try:
        # Run the batch, outputting a sentinel value so we can separate out
        # any error messages the batch might generate.
        shell_cmd = "\"{0}\" {1} && echo {2} && set".format(
            vars_cmd, vars_arch, SENTINEL)

        output = Popen(shell_cmd, stdout=PIPE, shell=True).stdout.read()

        lines = [line.strip() for line in output.decode("utf-8").splitlines()]
        env_lines = lines[lines.index(SENTINEL) + 1:]
    except:
        return None

    # Convert from var=value to dictionary key/value pairs. We upper case the
    # keys, since Python does that to the mapping it stores in environ.
    env = {}
    for env_var in env_lines:
        parts = env_var.split("=", maxsplit=1)
        env[parts[0].upper()] = parts[1]

    return env

def install_vc_env():
    """
    Try to collect the appropriate Visual Studio environment variables and
    set them into the current environment.
    """
    vc_env = _get_vc_env()
    if vc_env is None:
        print("set_vc_vars: Unable to fetch the Visual Studio Environment")
        return sublime.status_message("Error fetching VS Environment")

    # Add newly set environment variables
    for key in vc_env.keys():
        if key not in environ:
            environ[key] = vc_env[key]

    # Update existing variables whose values changed.
    for key in environ:
        if key in vc_env and environ[key] != vc_env[key]:
            environ[key] = vc_env[key]

    # Set a sentinel variable so we know not to try setting up the path again.
    environ[SENTINEL] = "BOOTSTRAPPED"
    sublime.status_message("VS Environment enabled")

def plugin_loaded():
    if sublime.platform() != "windows":
        return sublime.status_message("VS is not supported on this platform")

    # To reload the environment if it changes, restart Sublime.
    if SENTINEL in environ:
        return sublime.status_message("VS Environment already enabled")

    # Update in the background so we don't block the UI
    Thread(target=install_vc_env).start()
