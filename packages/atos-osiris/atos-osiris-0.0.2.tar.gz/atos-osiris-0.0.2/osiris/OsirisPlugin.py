#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
This module contains the OsirisPlugin class.
"""

import os
import json
import re
import osiris.const as const
import logging


class OsirisPlugin:
    """
    The OsirisPlugin class contains all methods to permit the translation between Osiris and a (like Openstack)
    :attribute __name: String contains the name of the plugin.
    """

    __name = ""

    def __init__(self, name):
        """
        Constructs a new OsirisPlugin instance.

        :param name: String that contains the name of the plugin.
        :return: Returns nothing.
        """
        logging.info("Initialize Osiris plugin ...")
        self.__setName(name)
        checkingCode = self.__check()
        if(checkingCode != 0):
            print("Error while loading plugin ... Error code (see __check()): ", checkingCode)
            exit(-1)

    def __check(self):
        """
        Check if plugin is ok :
            * def.json file exists
            * plugin name match pattern
            * objects folder exists
            * there is at least one object type
            * object's names match pattern

        :return: (Integer)
            * 0 if plugin is ok
            * -1 if def.json file doesn't exist
            * -2 if plugin name doesn't match pattern
            * -3 if objects folder doesn't exists
            * -4 if there is 0 object type
            * -5 if object's names doesn't match pattern
        """
        pluginName = self.getName()
        pluginPath = os.path.join(self.getPath())

        # Test : def.json file exists
        if(not os.path.isfile(os.path.join(pluginPath, 'def.json'))):
            return -1

        # Test : plugin name match pattern
        pluginNamePattern = re.compile(const.PLUGINS_NAMES_PATTERN)
        if(not pluginNamePattern.match(pluginName)):
            return -2

        # Test : objects folder exists
        if(not os.path.isdir(os.path.join(pluginPath, "objects"))):
            return -3

        # Test : there is at least one object type
        objectsDef = self.getObjectsDef()
        if(len(objectsDef) <= 0):
            return -4

        # Test : object's names match pattern
        objectsNamesPattern = re.compile(const.OBJECTS_NAMES_PATTERN)
        for objectDef in objectsDef:
            if(not objectsNamesPattern.match(objectDef['name'])):
                return -5

        # OK!
        else:
            return 0

    def getName(self):
        """
        Getter for __name attribute.

        :return: Returns __name (String) attribute.
        """
        return self.__name

    def __setName(self, name):
        """
        Setter for __name attribute.

        :param name: String that contains the name of the plugin.
        :return: Returns nothing.
        """
        self.__name = name

    def getPath(self):
        """
        Path to rep plugin
        :return: Return path to rep plugin .
        """
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "plugins", self.getName())

    def getObjectsDef(self):
        """
        Get list of object definition

        :return: Returns a list with all objects definition of the current plugin.
        """

        dataList = []

        # Get the list of all object descriptor files
        path = os.path.join(self.getPath(), "objects/")
        allObjectsFiles = os.listdir(path)

        # Put on our list all the json data
        for i in allObjectsFiles:

            pluginObject = os.path.join(path, i)

            with open(pluginObject) as jsonData:
                dataList.append(json.load(jsonData))

        return dataList

    def getObjectDef(self, objectName):
        """
        Get objectName object definition.

        :param objectName: (String) Name of the object type.
        :return: (JSON) ObjectName object definition or empty json if objectName object doesn't exists.
        """
        # Get object descriptor files
        objpath = os.path.join(self.getPath(), "objects/", objectName + ".json")
        if os.path.isfile(objpath):
            with open(objpath) as jsonData:
                return json.load(jsonData)
        else:
            return {}
