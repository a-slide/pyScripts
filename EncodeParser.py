#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@package    Epi2_Download_ENCODE_datasets
@brief      Download and rename files from encode datasets
@copyright  [GNU General Public License v2](http://www.gnu.org/licenses/gpl-2.0.html)
@author     Adrien Leger - 2016
* <aleg@ebi.ac.uk>
"""

#~~~~~~~GLOBAL IMPORTS~~~~~~~#

NAME = "EncodeParser"
VERSION = "0.1"
USAGE = "Usage: %prog [-t <file type>]  ENCODE_ID1 [ENCODE_ID2 ENCODE_ID3 ...]"


#~~~~~~~GLOBAL IMPORTS~~~~~~~#
try:
    # Standard library imports
    import os, sys, optparse
    from collections import OrderedDict
    from time import time
    from urllib.request import urlopen
    from urllib.parse import urlsplit
    from urllib.error import HTTPError, URLError
    
except ImportError as E:
    print (E)
    print ("Error while trying to import the packages. Please verify your dependencies\n")
    sys.exit(0)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class EncodeParser (object):
    """
    Description
    """
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #~~~~~~~FONDAMENTAL METHODS~~~~~~~#

    def __init__(self, filetype="", encodeID_list=""):
        """
        Initialization function. Store and check args. 
        """
        self.filetype = filetype
        self.encodeID_list = encodeID_list

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
        
        with open ("EncodeParser_report.tsv", "w") as report:
            for encodeID in self.encodeID_list:
                print ("Fetching info for {}".format(encodeID))
                
                # Recompose the URL of the information file
                tsv_url = "https://www.encodeproject.org/metadata/type=Experiment&y.limit=&searchTerm={}/metadata.tsv".format(encodeID)
                with urlopen(tsv_url) as tsv:
                    header = next(tsv)
                    for line in tsv:
                        dl = line.decode('utf-8')
                        sl = dl.split("\t")
                        
                        if not self.filetype or sl[1] == self.filetype:
                            report.write(dl)
                            file_URL = sl[38]
                            new_name= "{}_{}_{}_Rep{}_R{}_{}".format(
                                sl[3].replace(" ", "-"),
                                sl[6].replace(" ", "-"),
                                sl[12].replace(" ", "-"),
                                sl[28].replace(" ", "-"),
                                sl[32].replace(" ", "-"),
                                os.path.basename(sl[38]))
                            
                            output = wget(sl[38], new_name, 100000000)                    

        print ("Done in {}s".format(round(time()-start_time, 3)))
        return(0)


#~~~~~~~FUNCTIONS~~~~~~~#

def cl_init ():
    """
    init class method parsing command line arg and running verification, called only from command line
    """

    try:
        # Define parser usage, options
        optparser = optparse.OptionParser(usage=USAGE, version=NAME+VERSION)
        optparser.add_option('-t', dest="filetype", help="Type of files to dl. Default = everything")

        # Parse options and arguments
        opts, args = optparser.parse_args()
        
        # Test options and arguments
        filetype = opts.filetype

        assert len(args) >=1, "At least 1 ENCODE experiment ID" 
        
        return EncodeParser (opts.filetype, args)
    
    except Exception as E:
        print (E)
        print ("Error while parsing options")
        optparser.print_help()
        sys.exit(0)

def wget(url, out_name="", progress_block=100000000):
    """
    Download a file from an URL to a local storage.
    @param  url             A internet URL pointing to the file to download
    @param  outname         Name of the outfile where (facultative)
    @param  progress_block  size of the byte block for the progression of the download
    """
    
    def size_to_status (size):
        if size >= 1000000000:
            status = "{} GB".format(round(size/1000000000, 1))
        elif size >= 1000000:
            status = "{} MB".format(round(size/1000000, 1))
        elif size >= 1000:
            status = "{} kB".format(round(size/1000, 1))
        else :
            status = "{} B".format(size)
        return status
    
    # function specific imports 
    from urllib.request import urlopen
    from urllib.parse import urlsplit
    from urllib.error import HTTPError, URLError
    
    # Open the url and retrieve info
    try:
        u = urlopen(url)
        scheme, netloc, path, query, fragment = urlsplit(url)
    except (HTTPError, URLError, ValueError) as E:
        print (E)
        return None
        
    # Attribute a file name if not given
    if not out_name:
        out_name = os.path.basename(path)
        if not out_name:
            out_name = 'output.file'

    # Create the output file and 
    with open(out_name, 'wb') as fp:
        
        # Retrieve file meta information 
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_size = meta_func("Content-Length")
        if meta_size:
            file_size = int(meta_func("Content-Length")[0])
            print("Downloading: {}\tBytes: {}".format(url, file_size))
        else:
            file_size=None
            print("Downloading: {}\tSize unknown".format(url))
        
        # Buffered reading of the file to download
        file_size_dl = 0
        block_sz = 1000000
        
        last_pblock = progress_block
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            fp.write(buffer)
            
            # Progress bar
            file_size_dl += len(buffer)
            
            if file_size_dl >= last_pblock:
                status = "{} Downloaded".format(size_to_status(file_size_dl))
                if file_size: 
                    status += "\t[{} %]".format (round(file_size_dl*100/file_size, 2))
                print(status)
                last_pblock += progress_block
        
        # Final step of the progress bar
        status = "{} Downloaded".format(size_to_status(file_size_dl))
        if file_size: 
            status += "\t[100 %]"
        print(status)
        
    return out_name


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#   TOP LEVEL INSTRUCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':
    program = cl_init()
    program()
