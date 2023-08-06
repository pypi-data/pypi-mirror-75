#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
This module contains the Osiris class.
"""

from osiris.OsirisSystem import OsirisSystem
import os
import json
import subprocess
import stat
import shutil
import re
import osiris.const as const
import logging


class Osiris:

    """
    The Osiris class contains all Osiris actions (introspect, list, backup ...)

    :attribute __system: OsirisSystem instance associate to this Osiris Instance.
    """

    __system = None

    def __init__(self, systemName, pluginName):
        """
        Constructs a new Osiris instance and init environment variables

        :param systemName: String that contains the name of the system associate with this Osiris instance. By default, gets the value present in osiris_env.json.
        :param pluginName: String that contains the name of the plugin used by the system. By default, gets the value present in osiris_env.json
        :return: Returns nothing.
        """

        logging.info("Initialize Osiris ...")

        self.__setSystem(systemName, pluginName)

        # Init env var
        os.environ['OSIRIS_PLUGIN'] = self.__getSystem().getPlugin().getName()
        os.environ['OSIRIS_SYSNAME'] = self.__getSystem().getName()
        initScriptPath = os.path.join(self.__getSystem().getPlugin().getPath(), "scripts", "scriptInit")
        if(os.path.isfile(initScriptPath)):
            exec(open(initScriptPath).read())

    def __getSystem(self):
        """
        Getter for __system attribute.

        :return: Returns __system (OsirisSystem) attribute.
        """
        return self.__system

    def __setSystem(self, systemName, pluginName):
        """
        Setter for __system attribute.

        :param systemName: Name of the system associate with this Osiris instance. By default, gets the value present in osiris_env.json.
        :param pluginName: Name of the plugin used by the system. By default, gets the value present in osiris_env.json
        :return: Returns nothing.
        """
        self.__system = OsirisSystem(systemName, pluginName)

    def __substitute(self, cmd, params=None):
        """
        Replace @keys on cmd ny associated value in dict.

        :param cmd: (String[]) Command to complete
        :param params: (Dict) @keys : values to inject in cmd
        :return: (String[]) Command with values instead of @keys
        """

    def __execCmd(self, cmd):
        """
        Execute the command or the script passed on parameter

        :param cmd: String with the shell command or a script name present on the plugin script folder
        :return: Returns script or command output
        """
        potential_script_path = os.path.join(self.__getSystem().getPlugin().getPath(), "scripts", cmd[0])
        # if a script with cmd name exists
        if(os.path.isfile(potential_script_path)):

            logging.info("%s%s%s", "Giving execution right to script `", potential_script_path, "`")
            os.chmod(potential_script_path, stat.S_IRWXU)

            script = potential_script_path + ' ' + ' '.join(cmd[1:])
            logging.info("%s%s%s", "Executing script `", script, "`")
            data = json.loads(subprocess.check_output(script, shell=True, stderr=subprocess.DEVNULL).decode("utf-8"))

        # it's a command
        else:
            logging.info("%s%s%s", "Executing command `", ' '.join(cmd), "`")
            data = json.loads(subprocess.check_output(' '.join(cmd), shell=True, stderr=subprocess.DEVNULL).decode("utf-8"))

        return data

    @staticmethod
    def systemAdd(path):
        """
        Add a system to local ~/.osiris from the definition given in JSON file at path.

        :param path: (String) Path to the system definition JSON file.
        :return: (Integer) 0 if ok, -1 if file not found, -2 if file is incorrect (plugin or system missing), -3 if plugin or system doesn't match pattern (const.SYSTEMS_NAMES_PATTERN), -4 if there is an OS problem to read the file, -5 if decondig JSON failed
        """

        logging.info("Adding system ...")

        # Check if path point on a real file
        if os.path.isfile(path):

            # Open file and load JSON data
            try:
                with open(path, 'r') as f:
                    data = json.loads(f.read())
            except OSError:
                logging.error("%s%s%s", "`", path, "` cannot be opened. Please cheack path and access rights.")
                return -4
            except ValueError:
                logging.error("%s%s%s", "Decoding JSON of `", path, "` has failed. Please check typos.")
                return -5

            # Test if plugin and name values are present
            namesPattern = re.compile(const.SYSTEMS_NAMES_PATTERN)
            if('plugin' not in data or 'name' not in data):
                logging.error("%s%s%s", "Missing plugin or system name on `", path, "`")
                return -2

            # Test if plugin and name values match with pattern
            if(not namesPattern.match(data['plugin']) or not namesPattern.match(data['name'])):
                logging.error("%s%s%s", "Plugin or system name on `", path, "` doesn't match pattern ^[A-Za-z0-9_\\-.]+$")
                return -3

            # Create path `~/.osiris/systems/<pluginName>/<systemName>`
            pathToDefFolder = os.path.join(os.environ['HOME'], '.osiris', 'systems', data['plugin'], data['name'])
            os.makedirs(pathToDefFolder, exist_ok=True)

            # Insert json data into `~/.osiris/systems/<pluginName>/<systemName>/def.json`
            with open(os.path.join(pathToDefFolder, 'def.json'), 'w') as f:
                f.write(json.dumps(data, indent=4, sort_keys=True))

            # Return OK!
            logging.info("System added !")
            return 0

        else:
            logging.error("%s%s%s", "`", path, "` is not a file or cannot be opened. Please cheack path and access rights.")
            return -1

    @staticmethod
    def systemRemove(systemName, pluginName):
        """
        Remove locally a system definition.

        :param systemName: (String) Name of the system to delete.
        :param pluginName: (String) Name of the system's plugin.
        :return: (Integer) 0 if ok, -1 if incorrect systemName or pluginName, -2 if system not found
        """
        logging.info("Removing system ...")
        pluginNamePattern = re.compile(const.PLUGINS_NAMES_PATTERN)
        systemNamePattern = re.compile(const.SYSTEMS_NAMES_PATTERN)
        if(not pluginNamePattern.match(pluginName) or not systemNamePattern.match(systemName)):
            logging.error("Plugin or system name doesn't match pattern ^[A-Za-z0-9_\\-.]+$")
            return -1
        else:
            try:
                pathToDelete = os.path.join(os.environ['HOME'], '.osiris', 'systems', pluginName, systemName)
                shutil.rmtree(pathToDelete)
            except FileNotFoundError:
                logging.error("%s%s", "`", pathToDelete, "` is not found.")
                return -2

            logging.info("System removed !")
            return 0

    @staticmethod
    def systemList():
        """
        List all systems known.

        :return: Returns list of systems in JSON. Ex : {'pluginA': ['SystemA'], 'pluginB': ['SystemB1', 'SystemB2']}
        """
        sysList = {}
        path = os.path.join(os.environ['HOME'], '.osiris', 'systems')
        for i in os.listdir(path):
            sysList[i] = os.listdir(os.path.join(path, i))
        return sysList

    def systemIntrospect(self):
        """
        Introspect all objects on the target system.
        At this time, introspect a system remove previous introspects.

        :return: Returns number of objects introspected if ok, -1 else.
        """
        logging.info("Introspecting whole system ...")
        objectsDefs = self.__getSystem().getPlugin().getObjectsDef()
        totalNbObjects = 0
        for objectDef in objectsDefs:
            nbObjects = self.objectIntrospect(objectDef['name'])
            if(nbObjects == -1):
                logging.info("%s%s%s", "Error while introspecting `", objectDef['name'], "` objects ...")
                return -1
            else:
                totalNbObjects += nbObjects

        logging.info("Whole system has been introspected !")
        return totalNbObjects

    def systemShow(self):
        """
        Show all objects instances currently on the local database.

        :return: Returns all objects instances in JSON.
        """
        # Use objectList(self, objectName) (like systemIntrospect with objectIntrospect)
        print("Not yet implemented")
        exit(-1)

    def systemSelectAll(self):
        """
        Select all objects instances currently on the local database.

        :return: Returns number of objects selected if ok, -1 else.
        """
        # Use self.objectSelect(..)
        print("Not yet implemented")
        exit(-1)

    def systemUnselectAll(self):
        """
        Unselect all objects instances currentry on the local database.

        :return: Returns number of objects unselected if ok, -1 else.
        """
        # Use self.objectUnselect(..)
        print("Not yet implemented")
        exit(-1)

    def objectIntrospect(self, objectName):
        """
        Introspect a specific object type on the target system.
        At this time, introspect an object remove previous introspects.

        :param objectName: (String) Name of the object type to instropect.
        :return: Returns number of objects introspected if ok, -1 else.
        """

        logging.info("%s%s%s", "Introspecting `", objectName, "` ...")
        # get def object
        objectDef = self.__getSystem().getPlugin().getObjectDef(objectName)
        if(objectDef == {}):
            logging.error("%s%s%s%s%s", "`", objectName, "` is not found on `", self.__getSystem().getPlugin().getName(), "` plugin.")
            return -1

        # Create table for the object if it doesn't exist
        self.__getSystem().getDb().createTable(objectDef['name'], objectDef['attributes'])

        # Execute introspect command and get data from system
        introspectCommand = objectDef["actions"]["introspect"]
        data = self.__execCmd(introspectCommand)

        # Remove data present into database
        self.__getSystem().getDb().flush(objectDef['name'])

        # Insert data into database
        self.__getSystem().getDb().insert(objectDef, data)

        return len(data)

    def objectList(self, objectName):
        """
        List all object instances currently on the local database.

        :param objectName: (String) Name of the object type to list.
        :return: Returns list of object instances in JSON.
        """
        # Use `listInstances(self, objectName)` of `OsirisDB.py`
        print("Not yet implemented")
        exit(-1)

    def objectCreate(self, objectName, args=None):
        """
        Create a new object instance (on the local database and on the target system).

        :param objectName: (String) Name of the object type to create.
        :param args: (Dict) Arguments needed to create the instance (None by default).
        :return: Returns id of the new instance if ok, -1 else.
        """
        # Create object on local database
        # use OsirisPlugin : getObjectDef
        # use OsirisDB > insert(..)

        # Get command from plugin definition
        # reuse OsirisPlugin : getObjectDef

        # Subtitute variables of the command with args dict
        # use self __substitute(..)

        # Execute command to create object on system
        # use self __execCMD(..)

        print("Not yet implemented")
        exit(-1)

    def objectSelect(self, objectName, id=None):
        """
        Select all or specifics instances of the given object.

        :param objectName: (String) Name of the object type to select.
        :param id: (List of Strings) ID of the instance to select. If not provided (None by default), select all instances of this type.
        :return: Returns number of objects selected if ok, -1 else.
        """
        # Use `selectInstance(..)` of `OsirisDB`
        print("Not yet implemented")
        exit(-1)

    def objectUnselect(self, objectName, id=None):
        """
        Unselect all or specifics instances of the given object.

        :param objectName: (String) Name of the object type to unselect.
        :param id: (String) ID of the instance to unselect. If not provided (None by default), unselect all instances of this type.
        :return: Returns number of objects unselected if ok, -1 else.
        """
        # Use `unselectInstance(..)` of `OsirisDB`
        print("Not yet implemented")
        exit(-1)

    def objectDelete(self, objectName, id):
        """
        Delete an instance of an object (on the local database and on the target system).

        :param objectName: (String) Name of the object type to delete.
        :param id: (String) ID of the instance to delete.
        :return: Returns 0 if ok, -1 else.
        """
        # Use deleteInstance(..) from OsirisDB
        print("Not yet implemented")
        exit(-1)

    def backupList(self, all=False):
        """
        List all backups definition of the target system. --all list backups definition for all system working with the current plugin.

        :param all: (Boolean) If all is True, list all backups of all systems with target plugin. Else, by default, list all backups of target system.
        :return: Returns backups list in JSON.
        """
        print("Not yet implemented")
        exit(-1)

    def backupShow(self, backupName, systemName=None):
        """
        Show instances of the backup definiton.

        :param backupName: (String) Name of the backup to show.
        :param systemName: (String) Name oh the system of the backup. By default (None), target system.
        :return: Return description of the backup in JSON.
        """
        print("Not yet implemented")
        exit(-1)

    def backupDefine(self, backupName):
        """
        Define a new backup with the current selected instances.

        :param backupName: (String) Name of the new backup definition.
        :return: Returns 0 if ok, -1 else.
        """
        print("Not yet implemented")
        exit(-1)

    def backupExport(self, backupName, path):
        """
        Export a backup definition to a path.

        :param backupName: (String) Name of the backup to export.
        :param path: (String) Relative path where the backup will be export.
        :return: Returns 0 if ok, -1 else.
        """
        print("Not yet implemented")
        exit(-1)

    def backupImport(self, path):
        """
        Import a backup definition from a path.

        :param path: (String) Relative path where the backup to import is.
        :return: Returns 0 if ok, -1 else.
        """
        print("Not yet implemented")
        exit(-1)

    def backupRun(self, backupName, systemName=None):
        """
        Run a backup on the target system.

        :param backupName: (String) Name of the backup to run.
        :param systemName: (String) Name of the system where the backup come. By default (None), target system.
        :return: Returns number of instances backuped if ok, -1 else.
        """
        print("Not yet implemented")
        exit(-1)

    def backupDelete(self, backupName, systemName=None):
        """
        Delete a backup definition.

        :param backupName: (String) Name of the backup to delete.
        :param systemName: (String) Name of the system where the backup come. By default (None), target system.
        :return: Returns 0 if ok, -1 else.
        """
        print("Not yet implemented")
        exit(-1)

    def backupExecutionList(self, systemName=None, backupName=None, all=False):
        """
        List executions of the current backup (or of all backups of the target system).

        :param systemName: (String) Name of the system of backup executions. By default (None), target system.
        :param backupName: (String) Name of the backup definition of backup executions. By default (None), all backups of the system.
        :param all: (Boolean) If true, list backup executions of all systems of the target plugin. Else, just list backup executions of systemName (or target system by default).
        :return: Returns backup execution list in JSON.
        """
        print("Not yet implemented")
        exit(-1)

    def backupExecutionExport(self, backupName, timestamp, path, systemName=None):
        """
        Export a backup execution to a path.

        :param backupName: (String) Name of the backup of the backup execution.
        :param timestamp: (String) Timestamp (yyyymmddhhmmss) of the backup execution.
        :param path: (String) Relative path where the backup execution will be exported.
        :param systemName: (String) Name of the system of the backup execution. By default (None), target system.
        :return: Returns 0 if ok, -1 else.
        """
        print("Not yet implemented")
        exit(-1)

    def backupExecutionImport(self, path):
        """
        Import a backup execution from a path.

        :param path: (String) Relative path of the backup execution to import.
        :return: Returns 0 if ok, -1 else.
        """
        print("Not yet implemented")
        exit(-1)

    def backupExecutionRestore(self, backupName, timestamp, systemName=None):
        """
        Restore a backup execution into target system.

        :param backupName: (String) Name of the backup of the backup execution.
        :param timestamp: (String) Timestamp (yyyymmddhhmmss) of the backup execution.
        :param systemName: (String) Name of the system of backup execution. By default (None), target system.
        :return: Returns number of instances restored if ok, -1 else.
        """
        print("Not yet implemented")
        exit(-1)

    def backupExecutionDelete(self, backupName, timestamp, systemName=None):
        """
        Delete a backup execution.

        :param backupName: (String) Name of the backup of the backup execution.
        :param timestamp: (String) Timestamp (yyyymmddhhmmss) of the backup execution.
        :param systemName: (String) Name of the system of the backup execution. By default (None), target system.
        :return: Returns 0 if ok, -1 else.
        """
        print("Not yet implemented")
        exit(-1)
