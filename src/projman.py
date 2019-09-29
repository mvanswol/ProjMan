# !/usr/bin/python3

import sys
from os.path import isdir
from os import makedirs
import re

from subprocessutility import SubProcessUtility
from directoryContextManager import workInDirectory

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

    def initializeBuildArea(self):
        """
        Function to initialize build area checking for existing repos,
        and creating/cloning any that might not exist

        Arguments
        ---------
        None

        Returns
        -------
        None

        """

        repo_map = self.getRepoStatus()

        for obj in self.config["repos"]:
            if obj["name"] not in repo_map:
                if "url" in obj:
                    print("Checking out code to {} for {}".format(obj["path"], obj["name"]))
                    if "branch" in obj:
                        self.cloneGitRepo(obj["url"], obj["path"], obj["branch"])
                    else:
                        self.cloneGitRepo(obj["url"], obj["path"])

                else:
                    print("Creating directory : {} for repo : {}".format(obj["path"], obj["name"]))
                    makedirs(obj["path"])

            else:
                if self.verbose:
                    print("Repo : {}, already exists skipping!!".format(obj["name"]))

        self.santityCheckInitialization()


    def cloneGitRepo(self, url, path, branch=None):
        """
        Function to clone git repo to a specific directory

        Arguments
        ---------
        url : string
            url of the git repo to clone
        path : string
            path to clone to
        branch : string (optional)
            optional argument of branch to clone, if not specified master

        Returns
        -------
        None
        """

        br = "master" if branch is None else branch
        if self.verbose:
            print("INFO : Cloning from {} to {} at branch/rev {}".format(url, path, br))

        git_cmd = ["git", "clone", "-b", branch, url, path]

        if self.verbose:
            print("INFO : Running Command {}".format(git_cmd))

        SubProcessUtility.runCommand(git_cmd)

    def santityCheckInitialization(self):
        """
        Function to check that all repos in config are present in the workspace

        Arguments
        ---------
        None

        Returns
        -------
        None
        """

        for obj in self.config["repos"]:
            if not isdir(obj["path"]):
                print("ERROR : Initialization Failed missing {} at path {}".format(obj["name"], obj["path"]))


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

        rev = None
        with workInDirectory(path):

            rev_cmd_args = ['git', 'rev-parse', 'HEAD']

            if self.verbose:
                print("INFO : Running command : {}".format(" ".join(rev_cmd_args)))

            rev = SubProcessUtility.runCommand(rev_cmd_args)

            if rev == None:
                print("Unable to get revision for {}, make sure config is correct".format(path))

        return rev



        