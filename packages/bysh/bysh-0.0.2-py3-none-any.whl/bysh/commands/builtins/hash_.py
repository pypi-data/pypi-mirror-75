from bysh.commands._abstract_command import Command

__command__ = 'hash_'


class hash_(Command):
    alias = ('hash',)

    def __init__(self, stdin, stdout, stderr, *args, **kwargs):
        super().__init__(stdin, stdout, stderr)

    def run(self, arguments, *args, **kwargs) -> int:
        raise NotImplementedError('Bysh does not uses a $PATH to find commands, '
                                  'and does not optimizes with a hash table.')
