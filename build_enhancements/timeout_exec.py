import sublime
import sublime_plugin

from Default.exec import ExecCommand

# Related Reading:
#     https://stackoverflow.com/q/61381000/814803
#
# This is an example of a custom build target that allows you to specify right
# inside the build the maximum amount of time the build should be allowed to
# run. If the build takes longer, it will automatically cancel itself.
#
# To use this, you need to include a key named "timeout" in your sublime-build
# file that specifies how long (in seconds) the build should be allowed to
# run. Setting it to zero or not including it will make the build run as
# normal. An example build might look like:
#
# {
#     "target": "timeout_exec",
#     "cancel": {"kill": true},
#
#     "timeout": 4,
#
#     "shell_cmd": "echo \"Start\" && sleep 10 && echo \"Done\""
# }
#
# There are two versions of this command here, the first one is for use in
# Sublime Text 4 while the second (older) one is for Sublime Text 3. You should
# choose and install only the one you need; if you're using ST3, make sure you
# change the name of the class or use the appropriate command name in your
# build file.


class TimeoutExecCommand(ExecCommand):
    """
    This is a custom build target which can optionally self cancel a build if
    it runs more than a configurable amount of time.

    This version will only work in Sublime Text 4.
    """
    def run(self, **kwargs):
        self.timeout = kwargs.pop("timeout", 0)
        self.build_complete = False

        super().run(**kwargs)

        if self.timeout:
            sublime.set_timeout(self.time_out_build, self.timeout * 1000)

    def time_out_build(self):
        if self.proc and not self.build_complete:
            self.write("\n[Timeout exceeded: %.1f]" % self.timeout)
            self.proc.kill()

    def on_finished(self, proc):
        self.build_complete = True
        super().on_finished(proc)


class TimeoutExecOldStyleCommand(ExecCommand):
    """
    This is a custom build target which can optionally self cancel a build if
    it runs more than a configurable amount of time.

    This version will only work in Sublime Text 3.
    """
    def run(self, **kwargs):
        self.timeout = kwargs.pop("timeout", 0)

        super().run(**kwargs)

        if self.timeout:
            sublime.set_timeout(self.time_out_build, self.timeout * 1000)

    def time_out_build(self):
        if self.proc:
            self.append_string(self.proc, "[Timeout exceeded: %.1f]" % self.timeout)
            self.proc.kill()
            self.proc = None
