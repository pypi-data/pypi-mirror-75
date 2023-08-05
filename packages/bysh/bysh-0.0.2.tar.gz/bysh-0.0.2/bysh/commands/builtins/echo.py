from bysh.commands._abstract_command import Command

__command__ = 'echo'


class echo(Command):
    def __init__(self, stdin, stdout, stderr, *args, **kwargs):
        super().__init__(stdin, stdout, stderr)

    def run(self, arguments, *args, **kwargs) -> int:
        if len(arguments) > 1:
            self.stdout.write(''.join(arguments[1:]))
        self.stdout.write('\n')
        return 0
