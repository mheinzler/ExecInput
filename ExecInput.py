"""ExecInput package for Sublime Text."""

import codecs
import os
import threading

import sublime
import sublime_plugin

from Default.exec import ExecCommand

original_run = ExecCommand.run


class ExecInputCommand(sublime_plugin.WindowCommand):
    """Command to send input to a process through the exec build target."""

    def run(self, quiet=False):
        """
        Run the command.

        :param quiet: Whether to show an error if there is no process.
        """

        # save the currently visible panel
        self.previous_panel = self.window.active_panel()

        if self.get_exec(quiet=quiet):
            # ask for the input
            self.window.show_input_panel(
                "Input", "", self.send_input, None, self.restore_panel)

    def get_exec(self, quiet=False):
        """
        Return the instance of the currently running exec build.

        :param quiet: Whether to show an error if there is no process.

        :returns: The instance of the current ExecCommand class.
        """

        # check if a build was started and we could grab an instance
        exec = getattr(self.window, "exec", None)
        if not exec:
            if not quiet:
                sublime.error_message(
                    "ExecInput:\n"
                    "Couldn't find an instance of the ExecCommand class.\n"
                    "Did you start a build with the exec target?")

            return None

        # check if the process is still running
        if not exec.proc or exec.proc.exit_code() is not None:
            if not quiet:
                sublime.error_message(
                    "ExecInput:\n"
                    "Couldn't find a running process.")

            return None

        return exec

    def send_input(self, input):
        """
        Send input to the exec build target.

        :param input: The input to send to the process
        """

        # append a newline to the input to simulate a terminal
        input = input + "\n"

        # send the input
        exec = self.get_exec()
        if exec:
            # write to the process using a separate thread to avoid deadlocks
            threading.Thread(
                target=self.write_input,
                args=(exec, input)
            ).start()

        # restore the previous panel
        self.restore_panel()

    def restore_panel(self):
        """Restore the panel that was active when the command was run."""
        if self.previous_panel:
            self.window.run_command("show_panel", {
                "panel": self.previous_panel
            })

    # we need the quiet parameter here to show errors when using the key
    # bindings
    def is_enabled(self, quiet=False):
        """
        Return True when there is a process to send input to.

        :param quiet: Whether to show an error if there is no process.

        :returns: True if enabled, False otherwise.
        """
        return self.get_exec(quiet=quiet) is not None

    @classmethod
    def write_input(cls, exec, input):
        """
        Write input to the current process of a ExecCommand instance.

        :param exec:  An instance of the ExecCommand class.
        :param input: The input to write.
        """

        # first write the input to the output panel to show it before any new
        # output of the process
        exec.on_data(exec.proc, input)

        # encode the input
        encoder_cls = codecs.getincrementalencoder(exec.encoding)
        encoder = encoder_cls('replace')
        data = encoder.encode(input)

        # write the data to the process' stdin
        os.write(exec.proc.proc.stdin.fileno(), data)


def run(self, *args, **kwargs):
    """
    Save the current class instance and run the original method.

    We have to overwrite the run method of the ExecCommand class to get access
    to the class instance and the running process.
    """

    # store this instance in the current window
    self.window.exec = self

    # call the original method
    original_run(self, *args, **kwargs)


def plugin_loaded():
    """Call when the package is loaded."""

    # overwrite the original run method
    ExecCommand.run = run


def plugin_unloaded():
    """Call when the package is unloaded."""

    # restore the original run method
    ExecCommand.run = original_run
