from bysh.commands._abstract_command import Command

__command__ = 'nop'


class nop(Command):  # nop command, used in dev
    def __init__(self, stdin, stdout, stderr, *args, **kwargs):
        super().__init__(stdin, stdout, stderr)
        self.node = kwargs.get('_node')
        self.shell = kwargs.get('_shell')
        self.store = kwargs.get('_store')

    def _run(self):
        self.stdout.write(self.node.dump())

    def run(self, arguments, *args, **kwargs):
        if self.parse_input(arguments[1:]):
            return 1

        self.stdout.write(str(self.arguments))
        self._run()
        return 0

