import os
import json
import os.path
import logging


class EnvironmentCli:

    def checkout():
        """
        Checks if the .osiris folder and the file osiris_env.json exist and if not, creates it.

        :param : Nothing.
        :return: Nothing.
        """
        homeOsiris = os.environ['HOME']
        if not os.path.isdir(os.path.join(homeOsiris, ".osiris/")):
            os.mkdir(os.path.join(homeOsiris, ".osiris/"))
        if not os.path.isfile(os.path.join(homeOsiris, ".osiris/", "osiris_env.json")):
            env = {"OSIRIS_SYSTEM": "", "OSIRIS_PLUGIN": ""}
            with open(EnvironmentCli.getPath(), 'w') as f:
                json.dump(env, f)

    def getPath():
        """
        Gives the path where the environment definition should be placed in this specific case in the user's home.

        :param: It has no parameters
        :return: Return the path of the json file that allows to declare the environment.
        """
        # 'HOME' environment variable
        homeOsiris = os.environ['HOME']
        # Join various path components
        envJson = os.path.join(homeOsiris, ".osiris/", "osiris_env.json")
        return envJson

    def setSystem(system):
        """
        Assigns the system attribute according to the given parameters.

        :param system: Name of the system associate with this Osiris instance. By default, gets the value present in osiris_env.json.
        :return: Nothing.
        """
        with open(EnvironmentCli.getPath()) as f:
            env = json.load(f)
        env["OSIRIS_SYSTEM"] = system
        with open(EnvironmentCli.getPath(), 'w') as f:
            json.dump(env, f)

    def getSystem():
        """
        Returns the Osiris system object of the current environment.

        :param : Nothing.
        :return: Returns setSystem(system) attribute.
        """
        with open(EnvironmentCli.getPath()) as f:
            env = json.load(f)
            system = env["OSIRIS_SYSTEM"]
        return system

    def setPlugin(plugin):
        """
        Assigns the plugin attribute according to the given parameters.

        :param plugin: Name of the system associate with this Osiris instance. By default, gets the value present in osiris_env.json.
        :return: Nothing
        """
        with open(EnvironmentCli.getPath()) as f:
            env = json.load(f)
        env["OSIRIS_PLUGIN"] = plugin
        with open(EnvironmentCli.getPath(), 'w') as f:
            json.dump(env, f)

    def getPlugin():
        """
        Returns the Osiris plugin object of the current environment.

        :param : Nothing.
        :return: Returns setPlugin(plugin) attribute.
        """
        with open(EnvironmentCli.getPath()) as f:
            env = json.load(f)
            plugin = env["OSIRIS_PLUGIN"]
        return plugin

    def verboseCli(verbose):
        """
        Gives information on the actions that carry out the CLI in the background.

        :param args: List of the necessary arguments indicated by the user when the command is inputted.
        :return: :Nothing.
        """
        if verbose is True:
            logging.basicConfig(level=logging.INFO)
