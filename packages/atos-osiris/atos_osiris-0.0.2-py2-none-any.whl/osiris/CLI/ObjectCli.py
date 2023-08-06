import argparse
from osiris.Osiris import Osiris
from osiris.CLI.EnvironmentCli import EnvironmentCli


def main():
    """
    Main function which allows to build the client for the object part of osiris. .

    :param : (String) The command entered by the user.
    :return: Nothing.
    """
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='Osiris', usage='Osiris <object> <action> <option>')
    parser.add_argument('object', help="Object on which the actions will be done. \n Osiris object: vm, flavor...")
    ObjectSystemCli = parser.add_subparsers(title="Actions that can be executed on the object")

    # create the parser for the "introspect" command
    OsirisIntrospect = ObjectSystemCli.add_parser('introspect', usage='osiris <object> introspect : Introspect a specific object type on the target system')
    OsirisIntrospect.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisIntrospect.set_defaults(func=objectIntrospectCli)

    # create the parser for the "list" command
    OsirisList = ObjectSystemCli.add_parser('list', usage='osiris <object> list : List all object instances currently on the local database')
    OsirisList.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisList.set_defaults(func=objectListCli)

    # create the parser for the "create" command
    OsirisCreate = ObjectSystemCli.add_parser('create', usage='osiris <object> create [args...] : Create a new object instance (on the local database and on the target system)')
    OsirisCreate.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisCreate.set_defaults(func=objectCreateCli)

    # create the parser for the "select" command
    OsirisSelectAll = ObjectSystemCli.add_parser('select', usage='osiris <object> select [<id>... | --all] : Select all or specifics instances of the given object')
    OsirisSelectAll.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisSelectAll.add_argument('-id', action="store", nargs=-1, dest="id", type=str, help="instance id")
    OsirisSelectAll.add_argument('--all', "-a", action="store", nargs=1, dest="system", type=str, help="select all objects")
    OsirisSelectAll.set_defaults(func=objectSelectCli)

    # create the parser for the "unselect" command
    OsirisUnselectAll = ObjectSystemCli.add_parser('unselect', usage='osiris <object> unselect [<id>... | --all] : Unselect  all or specifics instances of the given object')
    OsirisUnselectAll.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisUnselectAll.set_defaults(func=objectUnselectCli)

    # create the parser for the "delete" command
    OsirisDelete = ObjectSystemCli.add_parser('delete', usage='osiris <object> delete <id> : Delete an instance of an object (on the local database and on the target system)')
    OsirisDelete.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisDelete.set_defaults(func=objectDeleteCli)

    args = parser.parse_args()
    args.func(args)


def objectIntrospectCli(args):
    """
    Calls the osiris function which allows to introspect a specific object type on the target system.
    At this time, introspect an object remove previous introspects.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    objectName = args.object
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osirirsSystemIntrospect = osiris.objectIntrospect(objectName)
    if osirirsSystemIntrospect >= 0:
        print("The " + objectName + " instropect has been successfully achieved.")
    else:
        print("The instropect hasn't come to an end.")


def objectListCli(args):
    """
    Calls the osiris function which allows to list all object instances currently on the local database.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.objectList(args.object)


def objectCreateCli(args):
    """
    Calls the osiris function which allows to create a new object instance (on the local database and on the target system).

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.objectCreate(args.object)


def objectSelectCli(args):
    """
    Calls the osiris function which allows to select all or specifics instances of the given object.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.objectSelect(args.object)


def objectUnselectCli(args):
    """
    Calls the osiris function which allows to unselect all or specifics instances of the given object.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.objectUnselect(args.object)


def objectDeleteCli(args):
    """
    Calls the osiris function which allows to delete an instance of an object (on the local database and on the target system).

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    objectName = args.object
    osiris.objectDelete(objectName, id)


if __name__ == "__main__":
    main()
