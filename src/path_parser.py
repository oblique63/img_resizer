# Program: Image Resizer
# Module Description: Command Line Argument Parser
# Author: Enrique Gavidia
# E-mail: enrique@enriquegavidia.com
# License: TBD
# Date: 2008-2010

from os import getcwd
from os.path import abspath
from optparse import OptionParser

def parse_paths():
    ''' 
        Parse commandline input for a source path, and destination path.
        Returns the results in a list.
    '''
    
    parse_list = OptionParser()
    _opts, paths = parse_list.parse_args()
    return paths

def get_paths(path = '', destination = ''):
    '''
        Default method for getting the source and destination paths.
        Defaults to reading commandline input if no paramaters are given.
    '''
    
    imgpath, dest = path, destination

    # if either of the paramaters is not present, parse commandline input
    # and store it as a list in 'paths'
    if not imgpath or not dest:
        paths = parse_paths()
        
        # attempt to retrieve the source path from 'paths', if not present,
        # return empty string for other behaviors to handle.  
        if not imgpath:
            try:
                imgpath = abspath(paths[0])
            except:
                imgpath = ''
            
        # attempt to retrieve the destination path from 'paths', if not present,
        # return current directory.
        if not dest:
            try:
                dest = abspath(paths[1]) + '/'
            except:
                dest = getcwd()+'/'
    
    return imgpath, dest
    
