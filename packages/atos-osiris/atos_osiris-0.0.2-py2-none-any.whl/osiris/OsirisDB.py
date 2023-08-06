# !/usr/bin/env python3
# -*-coding:utf-8 -*

import sqlite3
import os
import logging


class OsirisDB:

    """
    The OsirisDB class contains all the functions necessary to interact with the database.

    :attribute __dbFilePath: String that contains the path to DB file
    :attribute __dbConn: String - connection object
    :attribute __cursor: String - object represent a database cursor, which is used to manage the context of a fetch operation.
    """

    __dbFilePath = None
    __dbConn = None
    __cursor = None

    def __init__(self, system):
        """
        Constructs a new instance to connect a data base

        :param system: (OsirisSystem) System linked to the database.
        """
        logging.info("Initialize Osiris local database ...")
        self.__setDbFilePath(os.path.join(os.environ['HOME'], '.osiris', 'systems', system.getPlugin().getName(), system.getName(), 'osiris.db'))
        self.__loadDatabase()
        self.__open()

    def __getDbFilePath(self):
        """
        Getter for __dbFilePath attribute.

        :return: String that returns path to DB file.
        """
        return self.__dbFilePath

    def __setDbFilePath(self, path):
        """
        Setter for __dbFilePath attribute.

        :param path: String that contains the path to DB file.
        """
        self.__dbFilePath = path

    def __getDbConn(self):
        """
        Getter for __dbConn attribute.
        """
        return self.__dbConn

    def __setDbConn(self, dbConn):
        """
        Setter for __dbConn attribute.

        :param dbConn: the connection object
        """
        self.__dbConn = dbConn

    def __getCursor(self):
        """
        Getter for __cursor attribute.
        """
        return self.__cursor

    def __setCursor(self, cursor):
        """
        Setter for __cursor attribute.

        :param cursor:
        """
        self.__cursor = cursor

    def __loadDatabase(self):
        """
        Create a database connection to the SQLite database

        :return: Returns nothing
        """
        try:
            self.__setDbConn(sqlite3.connect(self.__getDbFilePath()))
        except sqlite3.Error as e:
            print('Error connecting to database ! >> Error : %s' % (' '.join(e.args)))
            exit(-1)

    def __formatColumnName(self, name):
        """
        Format a object attribute name in database column name.

        :param name: (String) Object's attribute's name
        :return: (String) Formated string
        """
        return name.replace(" ", "")

    def __open(self):
        """
        Connection to the SQLite database
        """
        self.__setCursor(self.__getDbConn().cursor())

    def __close(self):
        """
        Commit and Close the connection with the database
        """
        self.__getDbConn().commit()
        self.__getCursor().close()

    def createTable(self, objectName, objectAttributes):
        """
        Create table for the object if it doesn't exist

        :param objectName: the name of the object
        :param objectAttributes: object instances in json format
        """

        self.__open()

        req = "CREATE TABLE IF NOT EXISTS " + objectName + " (osiris_id INTEGER PRIMARY KEY AUTOINCREMENT, osiris_selected BOOLEAN DEFAULT false, "
        for attribute in objectAttributes:
            if(attribute['type'] == 'litteral'):
                req += self.__formatColumnName(attribute['name']) + " TEXT, "
            elif(attribute['type'] == 'reference'):
                req += self.__formatColumnName(attribute['name']) + " TEXT, "
            elif(attribute['type'] == 'data'):
                req += self.__formatColumnName(attribute['name']) + " TEXT, "
            else:
                raise Exception(objectName + '[' + attribute['name'] + "] Attribute must be litteral, reference or data ...")
        req = req[:-2] + ")"
        self.__getCursor().execute(req)
        self.__close()

    def insert(self, objectDef, data):
        """
        Insert the data in the database

        :param objectDef: object definition in json format
        :param data: object data
        """

        self.__open()

        req = "INSERT INTO " + objectDef["name"] + "("
        for attribute in objectDef["attributes"]:
            req += self.__formatColumnName(attribute['name']) + ", "
        req = req[:-2]
        req += ") VALUES \n"

        for element in data:
            req += '('
            for attribute in objectDef["attributes"]:
                if(attribute['type'] == "litteral"):
                    value = str(element[attribute['name']])
                    req += "null, " if not value else "'" + value.replace("'", "''") + "', "
                elif(attribute['type'] == "reference"):
                    value = str(element[attribute['name']])
                    req += "null, " if not value else "'" + value.replace("'", "''") + "', "
                elif(attribute['type'] == "data"):
                    value = str(element[attribute['name']])
                    req += "null, " if not value else "'" + value.replace("'", "''") + "', "
                else:
                    raise Exception("Attribute must be litteral, reference or data ...")
            req = req[:-2]
            req += "),\n"

        req = req[:-2]
        req += ';'
        self.__getCursor().execute(req)
        self.__close()

    def listInstances(self, objectName):
        """
        List all instances of object of type objectName on the local database.

        :param objectName: (String) Name of the object type to list.
        :return: (JSON) List of instances.
        """
        print("Not yet implemented")
        exit(-1)

    def flush(self, objectName):
        """
        Flush all data on local database for objectName objects.

        :param objectName: (String) Object type to flush.
        :return: 0 if ok, -1 else
        """
        self.__open()
        req = "DELETE FROM " + objectName + ";"
        self.__getCursor().execute(req)
        self.__close()

    def selectInstance(self, objectName, osirisID=None):
        """
        Select objectName instance with osirisID (or all instances) on local database.

        :param objectName: (String) Object type name to select.
        :param osirisID: (Integer) ID of object instance to select. If None, select all instances of objectName type.
        :return: (Integer) 0 if ok, -1 else
        """
        # Put "osiris_selected" field to 1 for osirisID object instance
        # (or all instances if osirisID is None) of table __formatColumnName(objectName)
        print("Not yet implemented")
        exit(-1)

    def unselectInstance(self, objectName, osirisID=None):
        """
        Unselect objectName instance with osirisID (or all instances) on local database.

        :param objectName: (String) Object type name to select.
        :param osirisID: (Integer) ID of object instance to unselect. If None, unselect all instances of objectName type.
        :return: (Integer) 0 if ok, -1 else
        """
        # Put "osiris_selected" field to 0 for osirisID object instance
        # (or all instances if osirisID is None) of table __formatColumnName(objectName)
        print("Not yet implemented")
        exit(-1)

    def deleteInstance(self, objectName, osirisID):
        """
        Delete instance of objectName type and osirisID from local database.

        :param objectName: (String)
        :param osirisID: (Integer)
        :return: (Integer) 0 if ok, -1 else
        """
        # Exec something like `DELETE FROM objectName WHERE osiris_id = osirisID`
        print("Not yet implemented")
        exit(-1)
