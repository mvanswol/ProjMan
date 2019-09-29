# !/usr/bin/python3

import sys

from projman import ProjMan

class ProjManDriver(object):
    def __init__(self, config_file, verbose):
        """
        Constructor

        Arguments
        ---------
        config_file : string
            filename of config file to use

        Return
        ------
        None
        """

        self.config_file = config_file
        self.projman = ProjMan(config_file, verbose)

    def getConfigName(self):
        """
        Function to get the name of the config file

        Arguments
        ---------
        None

        Return
        ------
        string
            Name of the config file
        """

        return self.config_file
    
    def loadSuccessful(self):
        """
        Function to check that config file was loaded successfully

        Arguments
        ---------
        None

        Returns
        -------
        Boolean
            True if config is not None, False if None
        """

        return self.projman.loadSuccessful()

    def getRepoStatus(self):
        """
        Function to get status of repos listed in the config

        Arguments
        ---------
        None

        Returns
        -------
        None
        """

        repo_map = self.projman.getRepoStatus()

        for key in repo_map:
            print("{} at {}".format(key, repo_map[key]))

def main():
    import argparse

    description = """
                  A simple python module useful from managing a project with multiple repositories.
                  This will allow a user to provide a config file with a list of git repositories
                  their location, and their branches, commits.

                  
                  """

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-c", "--config_file", dest="config_file",
                         help="optional config file argument", default="proj.json")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true",
                        help="verbose output", default=False)
    parser.add_argument("action", help="action argument, repo_status, update, init")
    args = parser.parse_args()


    driver = ProjManDriver(args.config_file, args.verbose)
    if not driver.loadSuccessful():
        print("config file {} did not load successfully".format(driver.getConfigName()))
        sys.exit(1)

    if args.action == "init":
        print("init called")
    elif args.action == "update":
        print("update called")
    elif args.action == "repo_status":
        driver.getRepoStatus()


if __name__ == "__main__":
    main()

