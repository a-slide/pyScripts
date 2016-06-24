#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@package    
@brief      
@copyright  [GNU General Public License v2](http://www.gnu.org/licenses/gpl-2.0.html)
@author     Adrien Leger - 2016
* <aleg@ebi.ac.uk>
"""

#~~~~~~~GLOBAL IMPORTS~~~~~~~#

NAME = "GenericClass"
VERSION = "0.1"
USAGE = "Usage: %prog -w [-y -z] "


#~~~~~~~GLOBAL IMPORTS~~~~~~~#
try:
    # Standard library imports
    import os, sys, optparse
    from collections import OrderedDict
    from time import time
    
    # Local Package import
    
    # Third Party Package import
    
except ImportError as E:
    print (E)
    print ("Error while trying to import the packages. Please verify your dependencies\n")
    sys.exit(0)

#~~~~~~~CL ARG OPTS PARSING ~~~~~~~#

def cl_init ():
    """
    init class method parsing command line arg and running verification, called only from command line
    """

    try:
        # Define parser usage, options
        optparser = optparse.OptionParser(usage=USAGE, version=NAME+VERSION)
        optparser.add_option('-X', dest="X", help="")
        optparser.add_option('-Y', dest="Y", action='store_true', help="")

        # Parse options and arguments
        opts, args = optparser.parse_args()
        
        # Test options and arguments
        assert opts.X, "X is a mandatory option"
        assert len(args) == 2, "2 arguments are required"
        
        return GenericClass (opts.X, opts.Y, args[0], args[1])
    
    except Exception as E:
        print (E)
        print ("Error while parsing options")
        optparser.print_help()
        sys.exit(0)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class GenericClass (object):
    """
    Description
    """
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #~~~~~~~FONDAMENTAL METHODS~~~~~~~#

    def __init__(self, W, X, Y, Z):
        """
        Initialization function. Store and check args. 
        """
        self.W = W 
        self.X = X
        self.Y = Y
        self.Z = Z

    def __str__(self):
        msg = "{} Class\nParameters list\n".format(self.__class__.__name__)
        # list all values in object dict in alphabetical order
        for key, value in OrderedDict(sorted(self.__dict__.items(), key=lambda t: t[0])).items():
            msg+="\t{}\t{}\n".format(key, value)
        return (msg)

    def __repr__(self):
        return "<Instance of {} from {} >\n".format(self.__class__.__name__, self.__module__)

    #~~~~~~~PUBLIC METHODS~~~~~~~#

    def __call__ (self):
        """
        Main function of the script
        """

        start_time = time()
        
        print(self)
        
        print ("Done in {}s".format(round(time()-start_time, 3)))
        return(0)


    #~~~~~~~PRIVATE METHODS~~~~~~~#

    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#   TOP LEVEL INSTRUCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':
    program = cl_init()
    program()
