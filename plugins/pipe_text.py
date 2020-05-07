import sublime
import sublime_plugin
from subprocess import run, PIPE
import time
from datetime import datetime


class PipeTextCommand(sublime_plugin.TextCommand):
    """Pipe text from ST - the selections, if any, otherwise the entire buffer contents
       - to the specified shell command.
       Useful for formatting XML or JSON in a quick and easy manner.
       i.e. a workaround for https://github.com/sublimehq/sublime_text/issues/3294
       This command requires Python >= 3.5, and therefore, ST build >= 4050, and for the
       package to have opted in to the Python 3.8 plugin host. (The User package is
       automatically opted-in.)
    """
    def run(self, edit, shell_command):
        # if not all selections are non-empty
        if not all(self.view.sel()):
            # use the entire buffer instead of the selections
            regions = [sublime.Region(0, self.view.size())]
        else:
            # use the user's selections
            regions = self.view.sel()

        failures = False
        start = time.perf_counter()
        logs = list()
        def log(message):
            nonlocal logs
            log_text = str(datetime.now()) + ' ' + message
            logs.append(log_text)
            print(log_text)

        for region in reversed(regions):
            text = self.view.substr(region)
            
            before = time.perf_counter()
            # https://docs.python.org/3/library/subprocess.html#subprocess.run - new in version 3.5
            # therefore, this python file should be in your User package (which defaults to Python 3.8)
            # and you need to be using ST build >= 4050
            p = run(shell_command, capture_output=True, input=text, encoding='utf-8')
            after = time.perf_counter()

            # TODO: also report the selection index?
            log(f'command {repr(shell_command)} executed with return code {str(p.returncode)} in {(after - before) * 1000:.3f}ms')

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
#view.run_command('pipe_text', { 'shell_command': ['xmllint', '--format', '-'] })

# example for pretty printing JSON using jq:
#view.run_command('pipe_text', { 'shell_command': ['jq', '.'] })
