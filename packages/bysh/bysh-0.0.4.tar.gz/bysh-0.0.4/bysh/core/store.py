import sys
import os
import importlib
import pathlib
import getpass
import platform

from bysh.lib import colorama


class Store:
    """
    This class stores all bash and public variables.
    Example: The engine uses this self.stdout to output data.
    Example: The shell uses this self.ps1 to get the ps1 prompt.
    
    All available commands are stored into self.commands.
    """

    def __init__(self):

        colorama.init()

        # Contains all callables commands. (used as a cache)
        self._commands = {}  # dict[str, Command]

        # Store to handle all variables, their getters and setters
        self._path = pathlib.Path().absolute()  # current directory
        self.user = getpass.getuser()  # current user
        self.host = platform.uname().node  # current hostname

        self.stdin = sys.stdin  # general stdin: (mostly tty)
        self.stdout = sys.stdout
        self.stderr = sys.stderr

        self.exit = False  # main loop          # Global variable to indicate stop (used in shell)

        self._ps1 = (  # template PS1
                colorama.Fore.GREEN
                + '{user}@{host}'
                + colorama.Fore.BLUE
                + ':{path}$'
                + colorama.Fore.RESET
                + ' '
        )
        self.ps2 = ''
        self.ps3 = ''
        self.ps4 = ''
        self.last_return_code = 0  # $?         # Return code of last command

    def _load_commands(self, folder=None) -> None:
        """
        This commands loads all files contained in subdirectories in bysh/commands,
        if the file is a .py and does not start with '_'.
        Only the first folder level is considered.
        :param folder: The subfolder's name inside bysh/commands to load files from
        :return: None
        """

        # The store holds the responsability of loading commands.
        # All subfolders under bysh/commands are supposed to be directories, with each file a command.

        # The first call scans the dir, and calls again this func with the folder s name
        if folder is None:
            base = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'commands')
            for d in os.listdir(base):
                if os.path.isdir(os.path.join(base, d)):
                    self._load_commands(d)

        else:
            importlib.invalidate_caches()  # if commands have been modified: allows hot reload 
            # like bash, same as his hash table

            # all commands files inside folder: public python files.
            cmds = [
                f for f in os.listdir(
                    os.path.join(
                        os.path.join(
                            os.path.dirname(
                                os.path.dirname(__file__)
                            ), 'commands'), folder)
                )
                if (f.endswith('.py') and not f.startswith('_'))
            ]

            for f in cmds:
                mod = importlib.import_module('.' + f[:-3], 'bysh.commands.{}'.format(folder))  # get the module
                cmd = getattr(mod, mod.__command__, None)  # get the command name
                if cmd is None:
                    continue  # ignore .py if __command__ is not defined
                cmd.origin = folder  # write the folder name, so the origin of command is kept
                self._commands[mod.__command__] = cmd  # add the command class to the self._commands dict

                # also add aliases to self._commands
                if getattr(cmd, 'alias', None):
                    for a in getattr(cmd, 'alias'):
                        self._commands[a] = cmd

    @property
    def commands(self) -> dict:
        """
        Accessor for commands.
        if not loaded, forces a reload of the commands.
        :return:
        """
        # load commands, self._commands acts like a cache
        if not self._commands:
            self._load_commands()
        return self._commands

    @commands.setter
    def commands(self, _) -> None:
        """
        Setter for commands. Currently not used, it just empties the
        commands list, which forces a reload on next command
        :param _: Unused
        :return:
        """
        # Reset the cache, so on next command all will be reimported.
        self._commands = {}

    @property
    def ps1(self) -> str:
        """
        Get the PS1, with the PS1 template and the informations.
        :return: The PS1 as a string. Colors are embedded, and ready to be displayed through colorama
        """
        return self._ps1.format_map({'path': self.path,
                                     'user': self.user,
                                     'host': self.host})  # cannot use self.__dict__ anymore because of property

    @ps1.setter
    def ps1(self, value: str):
        """
        Set a new PS1 template. The variables can be added, as python format string.
        The use of colors is allowed, as direct codes or colorama objects.

        Default PS1 :
        (colorama.Fore.GREEN
        + '{user}@{host}'
        + colorama.Fore.BLUE
        + ':{path}$'
        + colorama.Fore.RESET
        + ' ')
        :param value: The new PS1 template, as a string (formatable)
        :return:
        """
        self._ps1 = value

    @property
    def path(self) -> pathlib.Path:
        """
        Get the current stored path
        :return: the stored path, as a pathlib.Path object
        """
        return self._path

    @path.setter
    def path(self, _):
        """
        Set the path to the current folder.
        The parameter is not used.
        :param _: Unused
        :return:
        """
        self._path = pathlib.Path().absolute()

    @property
    def home(self) -> pathlib.Path:
        """
        Get the user's home
        :return: pathlib.Path object
        """
        return pathlib.Path.home()
