from bysh.commands._abstract_command import Command

__command__ = 'help_'


class help_(Command):
    alias = ('help',)

    def __init__(self, stdin, stdout, stderr, *args, **kwargs):
        super().__init__(stdin, stdout, stderr)

        self.store = kwargs.get('_store', None)
        if self.store is None:
            raise RuntimeError('_store: Store was not given in builtin <help> parameters')

    def run(self, arguments, *args, **kwargs) -> int:
        # - performance is not a goal for now -
        results = {}
        for name, cmd in self.store.commands.items():
            if cmd in results.keys():
                results[cmd] = results[cmd] + ' ' + name
            else:
                results[cmd] = name
        self.stdout.write('Command - aliases\n')

        #self.stdout.write(
        #    [(k, n) for k, n in results.items()]
        #)
        self.stdout.write('\n'.join(results.values()) + '\n'
                          )
        return 0
