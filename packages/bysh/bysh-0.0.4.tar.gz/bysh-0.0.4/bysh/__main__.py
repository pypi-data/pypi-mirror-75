# main entry point

from bysh.core import Shell
from bysh.core import Store
from bysh.core import Bysh


def console_run():
    # Main entry point.
    # Creates a three elements:
    #    - Store : the place where all internal and public data is stored
    #    - Bysh  : the engine, which executes commands. Relies on store for some variables
    #    - Shell : A shell, creating a loop and passing commands to the engine.

    # We then execute the Read Execute Print Loop of the Shell.

    # TODO: The store should be created by the engine.
    # TODO: Some of the store's variables should be in Shell

    # TODO: We could to from bysh import Shell, and just launch it

    s = Store()

    sh = Shell(
        Bysh(s),
        s
    )
    sh.repl_loop()


if __name__ == '__main__':
    console_run()
