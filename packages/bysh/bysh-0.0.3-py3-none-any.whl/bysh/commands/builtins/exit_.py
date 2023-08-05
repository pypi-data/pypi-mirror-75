from bysh.commands._abstract_command import Command

__command__ = 'exit_'


class exit_(Command):
    alias = ('exit',)

    def __init__(self, stdin, stdout, stderr, *args, **kwargs):
        super().__init__(stdin, stdout, stderr)
        self.store = kwargs.get('_store', None)
        if self.store is None:
            raise RuntimeError('_store: Store was not given in builtin <cd> parameters')

    def run(self, arguments, *args, **kwargs) -> int:
        self.store.exit = True
        return 0
