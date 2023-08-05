from bysh.commands._abstract_command import Command
import os

__command__ = 'ls'


class ls(Command):
    def __init__(self, stdin, stdout, stderr, *args, **kwargs):
        super().__init__(stdin, stdout, stderr)

    def run(self, arguments, *args, **kwargs):
        try:
            dt = '\n'.join(os.listdir()) + '\n'
        except PermissionError:
            self.stderr.write('Permission denied\n')
            return 1
        self.stdout.write(dt)
        self.stdout.flush()
        return 0
