from osiris.CLI import SystemCli
from osiris.CLI import ObjectCli
from osiris.CLI import BackupCli
from osiris.CLI import BackupExecutionCli
from osiris.CLI.EnvironmentCli import EnvironmentCli
import sys
import os


def main():
    """
    Calls the osiris function which allows to unselect all or specifics instances of the given object.

    :param: Nothing.
    :return: Nothing.
    """
    args = sys.argv[1:]
    if args[0] == 'system':
        EnvironmentCli.checkout()
        SystemCli.main()

    elif args[0] == 'backup' and args[1] == 'execution':
        EnvironmentCli.checkout()
        BackupExecutionCli.main()

    elif args[0] == 'backup':
        EnvironmentCli.checkout()
        BackupCli.main()

    else:
        EnvironmentCli.checkout()
        if EnvironmentCli.getPlugin() == '':
            print("The plugin has not been specified")

        else:
            homeOsiris = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../", "plugins", EnvironmentCli.getPlugin(), "objects")
            files = os.listdir(homeOsiris)
            find = False
            for name in files:
                if os.path.splitext(name)[0] == args[0]:
                    find = True
                    ObjectCli.main()
            if find is False:
                print("The object is not an object " + EnvironmentCli.getPlugin())


if __name__ == "__main__":
    main()
