from bysh.commands._abstract_command import Command

__command__ = 'pwd'


class pwd(Command):
    def __init__(self, stdin, stdout, stderr, *args, **kwargs):
        super().__init__(stdin, stdout, stderr)

        self.store = kwargs.get('_store', None)
        if self.store is None:
            raise RuntimeError('_store: Store was not given in builtin <pwd> parameters')

    def run(self, arguments, *args, **kwargs) -> int:
        self.stdout.write(str(self.store.path) + '\n')
        self.stdout.flush()
        return 0
