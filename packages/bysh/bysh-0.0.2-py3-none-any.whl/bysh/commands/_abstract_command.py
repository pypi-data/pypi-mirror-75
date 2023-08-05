# This is the interface that all commands need to comform to.
# 
# A command is an importable module, with the variable __command__ defined as a string.
# This string represents the name of the class to load from this file (so one class per file).
# This is also the name of the command.
# Aliases for this commands are defined using the Command.alias class attribute, as a tuple of strings
# All commands should herit from this abstract.

# When a command is called, it s class get instanciated, and all stdin/stdout/stderr are bound.
# The command should not execute other than setup code in __init__.

# The real command running is done in the run() method. This method gets the arguments passed to the command.


from typing import List, TextIO
import argparse

__command__ = ''


class ParsingError(Exception):
    pass


class Command:
    alias = ()  # tuple of strings, for aliases

    # base class for all commands and builtins

    def __init__(self,
                 stdin: TextIO,
                 stdout: TextIO,
                 stderr: TextIO,
                 *args, **kwargs):

        # in/out/err
        self.stdin: TextIO = stdin
        self.stdout: TextIO = stdout
        self.stderr: TextIO = stderr

        self.origin: str = ''  # the origin of the command (ex: 'builtins').

        # The self.argparser object allows commands to define their parameters,
        # and then call parse_input(str) to store the parsed parameters in self.arguments.
        self.argparser = argparse.ArgumentParser(prog='CMD', add_help=False)
        self.argparser.add_argument('-h', '--help', help='show this help message and exit', action='store_true')
        self.argparser.exit = self.exit
        self.arguments = None

    def run(self, arguments: List[str], *args, **kwargs) -> int:
        """
        Run the command, and return an error code. (0 if ok)
        The arguments are a list of string, containing the argv data (command included)
        Ex: ['ls', '-alh', 'Desktop']

        :param arguments: a list of strings of given arguments (argv)
        :param args:
        :param kwargs:  allow the engine to give variables  #TODO find a better way through dependency inj
        :return: int
        """
        raise NotImplementedError

    def parse_input(self, argus: str) -> int:
        """

        :param argus: the arguments as string to parse.
        :return: int: an error code, currently only one of 0 or 1.
        """
        # convenience function, parsing given arguments into self.arguments.
        # Can be called in beginning of run(), to parse arguments.
        # The functions have to add argparse arguments to the self.argparser object.
        # Commands can choose not to use this, and just dont call it.

        # the return does not mean error, but asks to exit program.
        # used as a way to bubble exit to subclass
        try:
            self.arguments = self.argparser.parse_args(argus)
        except ParsingError:
            return 1
        if self.arguments.help:
            self.argparser.print_help(self.stdout)
            return 1
        return 0

    def exit(self, *args, **kwargs):
        """
        The default implementation of argparse quit everything if a parsing error occurs.
        We override this, and just raise a ParsingError exception, allowing catchs.
        :param args: _
        :param kwargs: _
        :return:
        """
        raise ParsingError
