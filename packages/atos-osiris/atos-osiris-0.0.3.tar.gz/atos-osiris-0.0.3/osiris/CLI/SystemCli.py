
import argparse
from osiris.Osiris import Osiris
from osiris.CLI.EnvironmentCli import EnvironmentCli
import os


def main():
    """
    Main function which allows to build the client for the system  part of osiris. .

    :param : (String) The command entered by the user.
    :return: Nothing.
    """
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='Osiris', usage='Osiris <object> <action> <option>')
    parser.add_argument('object', help="System on which the actions will be done.")
    SystemCliParser = parser.add_subparsers(title="Actions that can be executed on the system")

    # create the parser for the "set" command
    OsirisSet = SystemCliParser.add_parser('set', usage='osiris system set [--plugin (-p) <pluginName>] [--system (-s) <systemName>] : Set target system')
    OsirisSet.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisSet.add_argument('--plugin', "-p", action="store", nargs=1, dest="plugin", type=str, help="<Plugin name>")
    OsirisSet.add_argument('--system', "-s", action="store", nargs=1, dest="system", type=str, help="<System name>")
    OsirisSet.set_defaults(func=setSysCli)

    # create the parser for the "get" command
    OsirisGet = SystemCliParser.add_parser('get', usage='osiris system get : Get taget system')
    OsirisGet.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisGet.set_defaults(func=getSysCli)

    # create the parser for the "add" command
    OsirisAdd = SystemCliParser.add_parser('add', usage='osiris system add pathToDefJson : Add a system with a definition json file.')
    OsirisAdd.add_argument('pathToDefJson', type=str, help="path definition system json file")
    OsirisAdd.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisAdd.set_defaults(func=systemAddCli)

    # create the parser for the "remove" command
    OsirisRemove = SystemCliParser.add_parser('remove', usage='osiris system remove [--plugin (-p) <pluginName>] [--system (-s) <systemName>] : Remove a system and all his data.')
    OsirisRemove.add_argument('--plugin', "-p", action="store", nargs=1, dest="plugin", type=str, help="<Plugin name>")
    OsirisRemove.add_argument('--system', "-s", action="store", nargs=1, dest="system", type=str, help="<System name>")
    OsirisRemove.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisRemove.set_defaults(func=systemRemoveCli)

    # create the parser for the "list" command
    OsirisList = SystemCliParser.add_parser('list', usage='osiris system list : List all systems known')
    OsirisList.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisList.set_defaults(func=systemListCli)

    # create the parser for the "introspect" command
    OsirisIntrospect = SystemCliParser.add_parser('introspect', usage='osiris system introspect : Introspect all objects on the target system')
    OsirisIntrospect.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisIntrospect.set_defaults(func=systemIntrospectCli)

    # create the parser for the "show" command
    OsirisShow = SystemCliParser.add_parser('show', usage='osiris system show : Show all objects instances currently on the local database')
    OsirisShow.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisShow.set_defaults(func=systemShowCli)

    # create the parser for the "selectAll" command
    OsirisSelectAll = SystemCliParser.add_parser('selectAll', usage='osiris system selectAll : Select all objects instances currently on the local database')
    OsirisSelectAll.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisSelectAll.set_defaults(func=systemSelectAllCli)

    # create the parser for the "unselectAll" command
    OsirisUnselectAll = SystemCliParser.add_parser('unselectAll', usage='osiris system unselectAll : Unselect all objects instances currentry on the local database')
    OsirisUnselectAll.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisUnselectAll.set_defaults(func=systemUnselectAllCli)

    args = parser.parse_args()
    args.func(args)


def setSysCli(args):
    """
    Assigns the system attribute according to the given parameters.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    system = args.system[0]
    plugin = args.plugin[0]
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    EnvironmentCli.setSystem(system)
    EnvironmentCli.setPlugin(plugin)


def getSysCli(args):
    """
    Displays  the system and plugin object of the current environment.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    print("Here is the current system: \n" + "\nsystem: " + EnvironmentCli.getSystem() + "\nPlugin: " + EnvironmentCli.getPlugin())


def systemAddCli(args):
    """
    Calls the osiris function which allows to add a system to local ~/.osiris from the definition given in JSON file at path.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    path = args.pathToDefJson
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    EnvironmentCli.verboseCli(verbose)
    osirisSystemAdd = Osiris.systemAdd(path)
    if osirisSystemAdd == 0:
        print("The system was successfully added")
    elif osirisSystemAdd == -1:
        print("The specified file does not exist")
    elif osirisSystemAdd == -2:
        print("The file is incorrect (plugin or system missing)")
    elif osirisSystemAdd == -3:
        print("The name of the plugin or system is not written in the right format.(Osiris does not accept special characters. )")
    elif osirisSystemAdd == -4:
        print("there is an OS problem to read the file")
    elif osirisSystemAdd == -5:
        print("if decondig JSON failed")
    else:
        print("We encountered a problem loading the directory")


def systemRemoveCli(args):
    """
    Calls the osiris function which allows to remove locally a system definition.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osirirsSystemRemove = Osiris.systemRemove(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    if osirirsSystemRemove == 0:
        print("The system has been successfully removed")
    elif osirirsSystemRemove == -1:
        print("The name of the system or plugin is incorrect. (Osiris does not accept special characters)")
    elif osirirsSystemRemove == -2:
        print("The system was not found ")
    else:
        print("Unknown error")


def systemListCli(args):
    """
    Calls the osiris function which allows to list all systems known.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    if not os.path.isdir(os.path.join(os.environ['HOME'], '.osiris', 'systems')):
        print("You have not initialized the system for this, please use the command 'osiris system add'.")
    else:
        print(Osiris.systemList())


def systemIntrospectCli(args):
    """
    Calls the osiris function which allows to introspect all objects on the target system.
    At this time, introspect a system remove previous introspects.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osirirsSystemIntrospect = osiris.systemIntrospect()
    if osirirsSystemIntrospect >= 0:
        print("The instropect has been successfully achieved.")
    else:
        print("The instropect hasn't come to an end.")


def systemShowCli(args):
    """
    Calls the osiris function which allows to show all objects instances currently on the local database.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    print(osiris.systemShow())


def systemSelectAllCli(args):
    """
    Calls the osiris function which allows to select all objects instances currently on the local database.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    print(osiris.systemSelectAll())


def systemUnselectAllCli(args):
    """
    Calls the osiris function which allows to unselect all objects instances currentry on the local database.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    print(osiris.systemUnselectAll())


if __name__ == "__main__":
    main()
