import shutil

from bysh.commands._abstract_command import Command


__command__ = 'mv'


class mv(Command):

    def __init__(self, stdin, stdout, stderr, *args, **kwargs):
        super().__init__(stdin, stdout, stderr)

    def run(self, arguments, *args, **kwargs) -> int:
        if len(arguments) < 3:
            self.stderr.write('Please specify a src and dst')
            return 1
        try:
            shutil.move(
                arguments[1],
                arguments[2]
            )
        except IOError:
            self.stderr.write('Unable to move file')
            return 1
        return 0
