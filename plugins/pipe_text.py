import sublime
import sublime_plugin
from subprocess import run, PIPE
import time
from datetime import datetime
import sys


def execute_with_stdin(cmd, shell, text):
    before = time.perf_counter()
    # https://docs.python.org/3/library/subprocess.html#subprocess.run - new in version 3.5
    # therefore, this python file should be in your User package (which defaults to Python 3.8)
    # and you need to be using ST build >= 4050
    p = run(cmd, shell=shell, capture_output=True, input=text, encoding='utf-8')
    after = time.perf_counter()
    return (p, after - before)


class PipeTextCommand(sublime_plugin.TextCommand):
    """Pipe text from ST - the selections, if any, otherwise the entire buffer contents
       - to the specified shell command.
       Useful for formatting XML or JSON in a quick and easy manner.
       i.e. a workaround for https://github.com/sublimehq/sublime_text/issues/3294
       This command requires Python >= 3.5, and therefore, ST build >= 4050, and for the
       package to have opted in to the Python 3.8 plugin host. (The User package is
       automatically opted-in.)
    """
    def run(self, edit, cmd=None, shell_cmd=None):
        # if not all selections are non-empty
        if not all(self.view.sel()):
            # use the entire buffer instead of the selections
            regions = [sublime.Region(0, self.view.size())]
        else:
            # use the user's selections
            regions = self.view.sel()

        if not shell_cmd and not cmd:
            raise ValueError("shell_cmd or cmd is required")

        if shell_cmd and not isinstance(shell_cmd, str):
            raise ValueError("shell_cmd must be a string")

        # this shell_cmd/cmd logic was borrowed from Packages/Default/exec.py
        if shell_cmd:
            if sys.platform == "win32":
                # Use shell=True on Windows, so shell_cmd is passed through
                # with the correct escaping
                cmd = shell_cmd
                shell = True
            else:
                cmd = ["/usr/bin/env", "bash", "-c", shell_cmd]
                shell = False
        else:
            shell = False

        failures = False
        start = time.perf_counter()
        logs = list()
        def log(message):
            nonlocal logs
            log_text = str(datetime.now()) + ' ' + message
            logs.append(log_text)
            print(log_text)

        # TODO: the commands could take a while to execute, and it may be an idea to not block the ui
        # - so maybe just mark the buffer as read only until they complete and do the replacements async
        # maybe even with some phantoms or annotations near the selections to tell the user what is going on

        for region in reversed(regions):
            text = self.view.substr(region)
            
            p, time_elapsed = execute_with_stdin(cmd, shell, text)

            # TODO: also report the selection index?
            log(f'command "{cmd!r}" executed with return code {p.returncode} in {time_elapsed * 1000:.3f}ms')

            if p.returncode == 0:
                self.view.replace(edit, region, p.stdout)
            else:
                failures = True
                log(p.stderr.rstrip())

        total_elapsed = time.perf_counter() - start
        if failures:
            sublime.error_message('\n'.join(logs)) # TODO: don't include the datetimes here?
        else:
            sublime.status_message(f'text piped and replaced successfully in {total_elapsed * 1000:.3f}ms')

# example for pretty printing XML using xmllint:
# TODO: option for no xml prolog when working with selections? https://stackoverflow.com/q/37118327/4473405
#view.run_command('pipe_text', { 'cmd': ['xmllint', '--format', '-'] })

# example for pretty printing JSON using jq:
#view.run_command('pipe_text', { 'cmd': ['jq', '.'] })

#view.run_command('pipe_text', {"shell_cmd": "sort | uniq"})
