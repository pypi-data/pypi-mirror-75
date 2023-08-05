import os

from bysh.commands._abstract_command import Command


__command__ = 'touch'


class touch(Command):

    def __init__(self, stdin, stdout, stderr, *args, **kwargs):
        super().__init__(stdin, stdout, stderr)

    def run(self, arguments, *args, **kwargs) -> int:
        if len(arguments) < 2:
            self.stderr.write('Please specify a file name')
            return 1
        try:
            with open(arguments[1], 'a'):
                os.utime(arguments[1], None)  # in original touch changes the file timestamp
                pass
        except IOError:
            self.stderr.write('Unable to create file')
            return 1
        return 0
