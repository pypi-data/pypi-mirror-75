from typing import Union, List

from bysh.core.store import Store
from bysh.commands._abstract_command import Command
from bysh.core import stdio


class Bysh:
    """
    The main eval loop, executing commands.
    The commands to be executed needs to be loaded with self.load_ast(ast).
    This ast is then executed with self.eval().
    """

    # The main ceval
    def __init__(self, store: Store):
        self.current_ast = None
        self.store = store

    def load_ast(self, ast) -> None:
        """
        Loads the AST given, so it will be executed on next eval() call
        :param ast: The AST to load
        :return:
        """
        self.current_ast = ast

    def get_command_from_name(self, cmd: str) -> Union[Command.__class__, None]:
        return self.store.commands.get(cmd, None)

    @staticmethod
    def node_parts_to_list(node) -> List[str]:
        # returns the words contained in the nodes
        return [s.word for s in node.parts if s.kind == 'word']

    def exec_simple_command(self, node) -> None:  # CommandNode
        """
        Executes a single Command Node.
        :param node: the command node to execute
        :return:
        """
        cls_cmd = self.get_command_from_name(node.parts[0].word)
        if cls_cmd is None:
            self.store.stderr.write('Command not found: {}\n'.format(node.parts[0].word))
            self.store.last_return_code = 1
            return

        command = cls_cmd(stdio.get_new_std(),
                          self.store.stdout,
                          self.store.stderr,
                          _store=self.store,  # TODO: for now all theses are given in **kwargs
                          _shell=self,        # maybe find a cleaner and more standard way to do
                          _node=node)
        try:
            # execute command from ast, with the words in the following nodes.
            self.store.last_return_code = command.run(self.node_parts_to_list(node)) or 0  # default to 0 if nothing
        except NotImplementedError as e:  # exceptions raised by the commands
            self.store.stderr.write('The functionnality you asked is not implemented : {}\n'.format(e))
            self.store.last_return_code = 1
        except Exception as e:
            self.store.stderr.write('BYSH: Unhandled exception : {}\n'.format(e))

    def eval(self) -> None:
        """
        Executes the AST previously loaded by load_ast()
        :return: None
        """
        # simple commands
        for nod in self.current_ast:
            if nod.kind == 'command':  # TODO: Allow execution of pipelines and lists
                try:
                    self.exec_simple_command(nod)
                except Exception as e:
                    self.store.stdout.write('ERROR while executing {} {}'.format(nod, e))
                    raise

        self.current_ast = None         # reset the current ast after execution
