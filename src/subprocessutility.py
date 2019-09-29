# !/usr/bin/python3

import subprocess
import sys

class SubProcessUtility(object):

    @staticmethod
    def runCommand(arg_list):
        """
        Function to run command in argument list, check for errors
        and return output

        Arguments
        ---------
        arg_list : list
            list of program arguments

        Returns
        -------
        String
            Output of command
        """

        proc = subprocess.Popen(arg_list, stdout=subprocess.PIPE)

        outs = None
        errs = None


        try:
            outs, errs = proc.communicate()
        except Exception as e:
            print("Exception encountered!!, {}".format(e))
            return None

        if errs:
            print("Error : {}".format(errs.decode("utf-8")))
            return None

        if outs == None:
            return None

        return outs.decode('utf-8').strip()