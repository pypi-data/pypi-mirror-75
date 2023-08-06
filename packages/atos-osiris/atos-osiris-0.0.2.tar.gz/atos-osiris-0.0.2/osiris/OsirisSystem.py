#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
This module contains the OsirisSystem class.
"""

from osiris.OsirisDB import OsirisDB
from osiris.OsirisPlugin import OsirisPlugin
import os
import logging


class OsirisSystem:

    """
    The OsirisSystem class contains all methods to interact with a concrete system.
    """

    __name = ""
    __plugin = None
    __db = None

    def __init__(self, systemName, pluginName):
        """
        Constructs a new OsirisSystem instance.

        :param systemName: String that contains the name of the system associate with this Osiris instance
        :param pluginName: String that contains the name of the plugin used by the system.
        :return: Returns nothing.
        """
        logging.info("Initialize Osiris system ...")
        self.__setPlugin(pluginName)
        self.__setName(systemName)
        self.__setDb(OsirisDB(self))

    def getName(self):
        """
        Getter for __name attribute.

        :return: Returns __name (String) attribute
        """
        return self.__name

    def __setName(self, name):
        """
        Setter for __name attribute.

        :param name: (String) System's name
        :return: Returns nothing.
        """
        path = os.path.join(self.getPath(), self.getPlugin().getName(), name, 'def.json')
        if os.path.isfile(path):
            self.__name = name
        else:
            print("no such file : ", path)
            exit(-1)

    def getPlugin(self):
        """
        Getter for __plugin attribute.

        :return: Returns __plugin (OsirisPlugin) attribute.
        """
        return self.__plugin

    def __setPlugin(self, pluginName):
        """
        Setter for __plugin attribut.

        :param name: (String) Plugin's name.
        :return: Returns nothing.
        """
        self.__plugin = OsirisPlugin(pluginName)

    def getDb(self):
        """
        Getter for __db attribute.

        :return: Returns __db (OsirisDB) attribute
        """
        return self.__db

    def __setDb(self, osirisDB):
        """
        Setter for __db attribute.

        :param osirisDB: OsirisDB object
        :return: Returns nothing
        """
        self.__db = osirisDB

    def getPath(self):
        """
        Path to rep system
        :return: Return path to rep system
        """
        return os.path.join(os.environ['HOME'], '.osiris', 'systems')
