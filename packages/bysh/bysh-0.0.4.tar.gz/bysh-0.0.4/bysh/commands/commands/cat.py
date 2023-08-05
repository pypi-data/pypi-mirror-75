from bysh.commands._abstract_command import Command

__command__ = 'cat'


class cat(Command):

    def __init__(self, stdin, stdout, stderr, *args, **kwargs):
        super().__init__(stdin, stdout, stderr)

    def run(self, arguments, *args, **kwargs) -> int:
        if len(arguments) <= 1:
            raise NotImplementedError('cat command needs at least one file to output, other '
                                      'functionnalities are not implemented')
        for arg in arguments[1:]:
            try:
                with open(arg, 'r', encoding='utf8') as f:
                    self.stdout.write(f.read())
            except FileNotFoundError:
                self.stderr.write('No such file or directory\n')
                return 1
            except IsADirectoryError:
                self.stderr.write('Is a directory\n')  # TODO: never hit, Permission denied is raised in place
                return 1
            except PermissionError:
                self.stderr.write('Permission denied\n')
                return 1
        return 0
