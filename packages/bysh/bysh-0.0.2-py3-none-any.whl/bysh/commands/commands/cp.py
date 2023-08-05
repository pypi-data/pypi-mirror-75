from bysh.commands._abstract_command import Command

import shutil

__command__ = 'cp'


class cp(Command):
    alias = ('cp',)

    def __init__(self, stdin, stdout, stderr, *args, **kwargs):
        super().__init__(stdin, stdout, stderr)

    def run(self, arguments, *args, **kwargs) -> int:
        if len(arguments) < 3:
            self.stderr.write('Please specify a source and destination')
            return 1
        try:
            shutil.copyfile(
                arguments[1],
                arguments[2]
            )
        except IOError:
            self.stderr.write('Unable to copy file')
            return 1
        return 0
