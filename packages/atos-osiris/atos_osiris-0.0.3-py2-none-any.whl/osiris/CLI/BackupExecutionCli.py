import argparse
from osiris.Osiris import Osiris
from osiris.CLI.EnvironmentCli import EnvironmentCli


def main():
    """
    Main function which allows to build the client for the Backup instance part of osiris. .

    :param : (String) The command entered by the user.
    :return: Nothing.
    """
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='Osiris', usage='Osiris <object> <action> <option>')
    parser.add_argument('object', help="Backup on which the actions will be done.")
    parser.add_argument('execution', help="Backup on which the actions will be done.")
    SystemCliParser = parser.add_subparsers(title="Actions that can be executed on the instance object")

    # create the parser for the "list" command
    OsirisList = SystemCliParser.add_parser('list', usage='osiris backup execution list [--system <systemName>] [--backup <backupName>] [--all] : List executions of the current backup (or of all backups of the target system).')
    OsirisList.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisList.set_defaults(func=backupExecutionListCli)

    # create the parser for the "export" command
    OsirisExport = SystemCliParser.add_parser('export', usage='osiris backup execution export [--system <systemName>] <backupName> <timestamp> <path> : Export a backup execution to a path.')
    OsirisExport.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisExport .set_defaults(func=backupExecutionExportCli)

    # create the parser for the "import" command
    OsirisImport = SystemCliParser.add_parser('import', usage='osiris backup execution import <path> : Import a backup execution from a path.')
    OsirisImport.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisImport.set_defaults(func=backupExecutionImportCli)

    # create the parser for the "restore" command
    OsirisRestore = SystemCliParser.add_parser('restore', usage='osiris backup execution restore [--system <systemName>] <backupName> <timestamp> : Restore a backup execution into target system.')
    OsirisRestore.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisRestore.set_defaults(func=backupExecutionRestoreCli)

    # create the parser for the "delete" command
    OsirisDelete = SystemCliParser.add_parser('delete', usage='osiris backup execution delete [--system <systemName>] <backupName> <timestamp> : Delete a backup execution.')
    OsirisDelete.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisDelete.set_defaults(func=backupExecutionDeleteCli)

    args = parser.parse_args()
    args.func(args)


def backupExecutionListCli(args):
    """
    Calls the osiris function which allows to list executions of the current backup (or of all backups of the target system).

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.backupExecutionList()


def backupExecutionExportCli(args):
    """
    Calls the osiris function which allows to export a backup execution to a path.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.backupExecutionExport()


def backupExecutionImportCli(args):
    """
    Calls the osiris function which allows to import a backup execution from a path.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.backupExecutionImport()


def backupExecutionRestoreCli(args):
    """
    Calls the osiris function which allows to restore a backup execution into target system.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.backupExecutionRestore()


def backupExecutionDeleteCli(args):
    """
    Calls the osiris function which allows to delete a backup execution.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osiris.backupExecutionDelete()
