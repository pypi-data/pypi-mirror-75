import os

from bysh.commands._abstract_command import Command


__command__ = 'mkdir'


class mkdir(Command):

    def __init__(self, stdin, stdout, stderr, *args, **kwargs):
        super().__init__(stdin, stdout, stderr)

    def run(self, arguments, *args, **kwargs) -> int:
        if len(arguments) < 2:
            self.stderr.write('Please specify a directory name')
            return 1
        try:
            os.mkdir(arguments[1])
        except IOError:
            self.stderr.write('Unable to create directory')
            return 1
        return 0
