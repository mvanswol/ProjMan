# !/usr/bin/python3

import sys
from os.path import isdir
from os import chdir, getcwd
import re

from subprocessutility import SubProcessUtility

class ProjMan(object):
    def __init__(self, config_file, verbose):
        """
        ProjMan class responsible for keeping track 
        of the repo state and preforming repo operations

        Arguments
        ---------
        config_file : string
            filename of the config file

        Returns
        -------
        None
        """
        self.loadConfig(config_file)
        self.verbose = verbose

    def loadConfig(self, config_file):
        """
        Function to load config file

        Arguments
        ---------
        config_file : string
            full filename of the config file

        Return
        ------
        None
        """

        import json

        self.config = None

        try:
            with open(config_file) as f:
                self.config = json.load(f)
        except OSError as err:
            print("Unable to process {}, {}".format(config_file, err))
            sys.exit(1)


    def loadSuccessful(self):
        """
        Function to determine if config was loaded succesfully
        """

        return (self.config != None)

    def getRepoStatus(self):
        """
        Function to get map of current revisions of repos
        in the workspace listed in the config

        Arguments
        ---------
        None

        Returns 
        -------
        None
        """

        repo_map = {}

        for obj in self.config["repos"]:
            name = obj["name"]
            path = obj["path"]

            if isdir(path):
                rev = self.getRepoRev(path)
                repo_map[name] = rev

        return repo_map

    def getRepoRev(self, path):
        """
        Function to get revision of repo at path

        Arguments
        ---------
        path : string
            path to repo

        Return
        ------
        String
            Revision hash of repo
        """

        if self.verbose:
            print("INFO : Getting info in {}".format(path))

        curr_dir = getcwd()

        # Run git command from repo
        chdir(path)

        rev_cmd_args = ['git', 'rev-parse', 'HEAD']

        if self.verbose:
            print("INFO : Running command : {}".format(" ".join(rev_cmd_args)))

        rev = SubProcessUtility.runCommand(rev_cmd_args)

        # go back to original directory
        chdir(curr_dir)

        if rev == None:
            print("Unable to get revision for {}, make sure config is correct".format(path))

        return rev



        