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

NAME = "FastqcSummary"
VERSION = "0.1"
USAGE = "Usage: %prog -i fasqc_result_folder_path -o Name_of_the_output_file "


#~~~~~~~GLOBAL IMPORTS~~~~~~~#
try:
    # Standard library imports
    import os, sys, optparse, zipfile, csv
    from time import time
    from glob import glob
    
    
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
        optparser.add_option('-i', dest="infolder", help="Path to the folder containing the fastqc zipped resuts (default ./")
        optparser.add_option('-o', dest="outfile", help="Path to the folder containing the fastqc zipped resuts (default ./fastqc_summary.csv")

        # Parse options and arguments
        opts, args = optparser.parse_args()
        
        # Test options and arguments
        infolder = opts.infolder if opts.infolder else "."
        outfile = opts.outfile if opts.outfile else "./fastqc_summary.csv"
        
        return FastqcSummary (infolder, outfile)
    
    except Exception as E:
        print (E)
        print ("Error while parsing options")
        optparser.print_help()
        sys.exit(0)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class FastqcSummary (object):
    """
    Description
    """
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #~~~~~~~FONDAMENTAL METHODS~~~~~~~#

    def __init__(self, infolder, outfile):
        """
        Initialization function. Store and check args. 
        """
        self.infolder = infolder 
        self.outfile = outfile
        self.file_list = [f for f in glob(self.infolder+"/*_fastqc.zip")]
        print ("Found {} files to aggregate".format(len(self.file_list)))
        
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
            
        # List modules used by FastQC:
        modules = [
            'Basic_Statistics',
            'Per_base_sequence_quality',
            'Per_tile_sequence_quality',
            'Per_sequence_quality_scores',
            'Per_base_sequence_content',
            'Per_sequence_GC_content',
            'Per_base_N_content',
            'Sequence_Length_Distribution',
            'Sequence_Duplication_Levels',
            'Overrepresented_sequences',
            'Adapter_Content',
            'Kmer_Content']

        # Set dict to convert module results to integer scores:
        scores = {'pass': 1,
                  'warn': 0,
                  'fail': -1}

        # List to collect module scores for each '_fastqc.zip' file:
        all_mod_scores = []
        
        for file in self.file_list:
            # open '_fastqc.zip' file
            with zipfile.ZipFile(file, 'r') as archive:
                members = archive.namelist() # return list of archive members
                fname = [member for member in members if 'fastqc_data.txt' in member][0] # find 'fastqc_data.txt' in members
                
                # open 'fastqc_data.txt'
                with archive.open(fname) as data:
                # Get module scores for this file:
                    mod_scores = [file]
                    for line in data:
                        text = line.decode('utf-8') 
                        if '>>' in text and '>>END' not in text:
                            text = text.lstrip('>>').split()
                            module = '_'.join(text[:-1])
                            result = text[-1]
                            mod_scores.append(scores[result])
                    
                    # Append to all module scores list:
                    all_mod_scores.append(mod_scores)
                    
        # Write scores out to a CSV file:
        with open(self.outfile, 'w') as f:
            writer = csv.writer(f)
            for mod_scores in all_mod_scores:
                writer.writerow(mod_scores)

        print ("Done in {}s".format(round(time()-start_time, 3)))
        return(0)
        
   

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#   TOP LEVEL INSTRUCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':
    program = cl_init()
    program()
  
