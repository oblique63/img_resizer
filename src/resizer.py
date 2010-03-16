# Program: Image Resizer
# Module Description: Image Resizing Object
# Author: Enrique Gavidia
# E-mail: enrique@enriquegavidia.com
# License: TBD
# Date: 2008-2010

from path_parser import parse_paths, get_paths
from PIL import Image
from os.path import isdir, getsize, abspath, exists
from os import listdir, mkdir, remove
from zipfile import ZipFile, is_zipfile 


class Resizer():
    """
    
    """
    #----{ Constructor }----------------------------------------------------------------
    def __init__(self, imgpath='', destination=''):
        if not imgpath or not destination:
            self.__path_input = parse_paths()
            self.__imgpath, self.__destination = get_paths()
        self.__max_size = 1024 * 300
        self.__resolution = ()
        self.__res_accuracy = .7
        self.__files_done = 0
        self.__suffix = ''
        
        if isdir(self.__imgpath):
            self.__type = 'dir'
            self.__total_files = len(listdir(self.__imgpath))
            if len(self.__path_input) < 2:
                self.__destination += self.__imgpath.rsplit('/',1)[1]+'__resized/'
        elif is_zipfile(self.__imgpath):
            self.__type = 'zip'
            self.__zip = ZipFile(self.__imgpath, 'r')
            self.__total_files = len(self.__zip.namelist())
            if len(self.__path_input) < 2:
                self.__destination += self.__imgpath.rsplit('.',1)[0].rsplit('/',1)[1]+'__resized/'
        else:
            self.__type = 'file'
            self.__total_files = 1
            self.__suffix = '__resized'
        
        if not exists(self.__destination):
            mkdir(self.__destination)
        
    
    #----{ Interface }----------------------------------------------------------------
    
    #---> Setters
    def set_imgpath(self, path):
        # Fix for paths in Windows
        if '\\' in path:
            path = path.split('\\')
            temp_path = ''
            for i in path:
                temp_path += i+'/'
            path = temp_path.rsplit('/',1)[0]

        self.__init__(path)
        self.__imgpath = path

    def set_suffix(self, suffix):
        self.__suffix = suffix
    
    def set_destination(self, dest):
        "Sets the destination for the resized images."
        self.__destination = dest
    
    def set_max_size(self, size):
        "In Kilobytes (KB); default size is 300KB"
        self.__max_size = size * 1024
        
    def set_res_accuracy(self, accuracy):
        """Set how close to the Max Filesize the output should be.  
           Accepts a number from 1-9, 1 being most accurate.  
           Note: Used in conjunction with max_size property [resizing by file size], 
           but only when user does not specify an output resolution.
        """
        self.__res_accuracy = accuracy / 10
        
    def set_resolution(self, width):
        "Maintains aspect ratio, and calculates resolution with respect to width"
        self.__resolution = (width,width)
    
    #---> Getters
    def path_input(self):
        """Returns original commandline [path] input. if object was 
           not initiated via commandline tool, returns empty string."""
        try:
            return self.__path_input
        except:
            return ''
        
    def img_path(self):
        "Returns the path of the original image(s)."
        return self.__imgpath

    def suffix(self):
        "Returns the string set to append the resized image(s)."
        return self.__suffix
    
    def max_size(self):
        return self.__max_size
    
    def res_accuracy(self):
        return self.__res_accuracy
    
    def destination(self):
        return self.__destination
    
    def total_files(self):
        return self.__total_files
    
    def files_done(self):
        return self.__files_done
    
    def percentage_done(self):
        return ((self.files_done() * 1.0)/(self.total_files() * 1.0)) * 100
    
    def status(self):
        working_on = str(self.files_done()+1)
        total = str(self.total_files())
        if len(working_on) < len(total):
            working_on = ' ' * (len(total) - len(working_on)) + working_on
        
        return 'working on image ' + working_on + ' of ' + total + '. . . '
    

    #----{ Magic }----------------------------------------------------------------------------
    
    def __format_percentage(self, indentation = 0 ):
        "Private method used to format the percentage displayed in the commandline output when resizing."
        percentage = str(int(self.percentage_done()))
        percentage = ' ' * (3 - len(percentage)) + percentage
        indentation = ' ' * indentation
        return indentation + percentage + '% done.'
    
    def __action(self, img, name=''):
        """Private method that does all the actual resizing.
        Note: Only accepts Image objects. Name parameter 
        only used by the __zip_handle method"""
        
        print self.status(),
        
        # Set name for output file
        if not name:
            name = img.filename.rsplit('.',1)[0].rsplit('/',1)[1]
        else:
            name = name.rsplit('.',1)[0]
               
        outfile = self.__destination + name + self.__suffix + '.' 
        outfile += img.filename.rsplit('.',1)[1]
        
        try:
            img.save(outfile, img.format)
            
            if not self.__resolution:
                while getsize(outfile) > self.__max_size:
                    x, y = img.size
                    size = (int(x * self.__res_accuracy), int(y * self.__res_accuracy))
                    img.thumbnail(size, Image.ANTIALIAS)
                    img.save(outfile, img.format)
            else:
                img.thumbnail(self.__resolution, Image.ANTIALIAS)
                img.save(outfile, img.format)
            
            self.__files_done += 1    
            print self.__format_percentage(4)
        
        except:
            self.__files_done += 1  
            print "Error making file."
        

    #----{ Handlers }----------------------------------------------------------------------------- 
       
    def __dir_handle(self):
        "Handles cases in which the given path is a directory."
        # iterates through all the files in the directory, resizing 
        # whatever image it finds in each iteration.
        for img in listdir(self.__imgpath):
            try:
                im = Image.open(self.__imgpath+'/'+img) 
                self.__action(im)
            except:
                pass
    
    def __zip_handle(self, zip):
        "Handles cases in which the given path is a zip file."
        
        # iterates through the files in the Zip archive....
        for img in zip.infolist():
            file = img.filename
            data = zip.read(file)
            
            # checks if the current file is a directory; if it is,
            # mirror that structure in the destination path.
            if isdir(file):
                mkdir(self.__destination + file)
                self.__total_files -= 1
            else:
                # if not, write the data of the current file, 
                # to a new [temporary] file in the destination path...
                # (i.e. extract it.)
                outfile = open(self.__destination + file, 'w')
                outfile.write(data)
                outfile.close()
                try:
                    # resize the extracted file; if no suffix is set,
                    # the resized file will overwrite the extracted file.
                    im = Image.open(self.__destination + file) 
                    self.__action(im,file)
                except:
                    pass

                if self.__suffix:
                    # if a suffix is set (making the output filename 
                    # different name from the original), then
                    # remove the original extracted file.
                    remove(self.__destination + file)
    
    #----{ Resize method }----------------------------------------------------------------------------
        
    def resize(self):
        print 
        try:
            if self.__type == 'file':
                im = Image.open(self.__imgpath)
                self.__action(im)
            elif self.__type == 'zip':
                self.__zip_handle(self.__zip)
            elif self.__type == 'dir':
                self.__dir_handle()
            print '-' * len(self.status() + self.__format_percentage(4) + ' ')
            print 'Resized image(s) located in:', self.destination()
        except:
            print "ERROR: Invalid Image Path."
        print


#---> Debug
#foo = Resizer()
#foo.set_max_size(100)
#foo.set_resolution(300)
#foo.resize()

