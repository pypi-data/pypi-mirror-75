import sys

from bysh.core import Bysh
from bysh.lib import bashlex
from bysh.lib import colorama

from bysh.core.store import Store


class Shell:

    def __init__(self, bysh: Bysh, store: Store):

        self.store = store
        self.bysh = bysh

        self.current_input: str = ''  # last command
        self.current_ast = None       # AST of this command

    def repl_loop(self) -> None:
        """
        Main Read Execute Print Loop of the program
        Get input, parse it and feed the engine.
        :return: None
        """
        while not self.store.exit:
            self.get_input()

            if not self.current_input or self.current_input.isspace():
                continue

            self.parse_ast(self.current_input)

            # [print(a.dump()) for a in self.current_ast]
            self.bysh.load_ast(self.current_ast)
            self.bysh.eval()

    def get_input(self) -> None:
        """
        Get input from store.stdin, and store it in self.current_input
        :return:
        """
        self.store.stdout.write(self.store.ps1)
        self.store.stdout.flush()
        self.current_input = self.store.stdin.readline()

    def parse_ast(self, src: str) -> None:
        """
        Parse the given command (in str), and store it in self.current_ast
        :param src:
        :return:
        """
        self.current_ast = bashlex.parse(src)
