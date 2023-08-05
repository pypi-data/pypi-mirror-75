from bysh.commands._abstract_command import Command


__command__ = 'rm'


class rm(Command):

    def __init__(self, stdin, stdout, stderr, *args, **kwargs):
        super().__init__(stdin, stdout, stderr)

    def run(self, arguments, *args, **kwargs) -> int:
        raise NotImplementedError
