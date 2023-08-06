
import argparse
from osiris.Osiris import Osiris
from osiris.CLI.EnvironmentCli import EnvironmentCli


def main():
    """
    Main function which allows to build the client for the Backup part of osiris.
    :param : (String) The command entered by the user.
    :return: Nothing.
    """
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='Osiris', usage='Osiris <object> <action> <option>')
    parser.add_argument('object', help="Object on which the actions will be done. \n Exemple:System, backup, Osiris object: vm, flavor...")
    SystemCliParser = parser.add_subparsers(title="Actions that can be executed on the object")

    # create the parser for the "list" command
    OsirisList = SystemCliParser.add_parser('list', usage='osiris backup list [--all] : List all backups definition of the target system. --all list backups definition for all system working with the current plugin.')
    OsirisList.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisList.set_defaults(func=backupListCli)

    # create the parser for the "show" command
    OsirisShow = SystemCliParser.add_parser('show', usage='osiris backup show [--system <systemName>] <backupName> : Show instances of the backup definiton.')
    OsirisShow.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisShow.set_defaults(func=backupShowCli)

    # create the parser for the "define" command
    OsirisDefine = SystemCliParser.add_parser('define', usage='osiris backup define <backupName> : Define a new backup with the current selected instances.')
    OsirisDefine.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisDefine.set_defaults(func=backupDefineCli)

    # create the parser for the "export" command
    OsirisExport = SystemCliParser.add_parser('export', usage='osiris backup export <backupName> <path> : Export a backup definition to a path.')
    OsirisExport.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisExport.set_defaults(func=backupExportCli)

    # create the parser for the "import" command
    OsirisImport = SystemCliParser.add_parser('import', usage='osiris backup import <path> : Import a backup definition from a path.')
    OsirisImport.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisImport.set_defaults(func=BackupImportCli)

    # create the parser for the "run " command
    OsirisRun = SystemCliParser.add_parser('run ', usage='osiris backup run [--system <systemName>] <backupName> : Run a backup on the target system.')
    OsirisRun.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisRun.set_defaults(func=backupRunCli)

    # create the parser for the "delete" command
    OsirisDelete = SystemCliParser.add_parser('delete', usage='osiris backup delete [--system <systemName>] <backupName> : Delete a backup definition.')
    OsirisDelete.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisDelete.set_defaults(func=backupDeleteCli)

    args = parser.parse_args()
    args.func(args)


def backupListCli(args):
    """
    Calls the osiris function which allows to list all backups definition of the target system. --all list backups definition for all system working with the current plugin.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing.
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.backupList()


def backupShowCli(args):
    """
    Calls the osiris function which allows to show instances of the backup definiton.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing.
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.backupShow()


def backupDefineCli(args):
    """
    Calls the osiris function which allows to define a new backup with the current selected instances.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.backupDefine()


def backupExportCli(args):
    """
    Calls the osiris function which allows to export a backup definition to a path.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.backupExport()


def BackupImportCli(args):
    """
    Calls the osiris function which allows to import a backup definition from a path.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.BackupImport()


def backupRunCli(args):
    """
    Calls the osiris function which allows to run a backup on the target system.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.backupRun()


def backupDeleteCli(args):
    """
    Calls the osiris function which allows to delete a backup definition.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.backupDelete()


if __name__ == "__main__":
    main()
