# Program: Image Resizer
# Module Description: Command Line Interface
# Author: Enrique Gavidia
# E-mail: enrique@enriquegavidia.com
# License: TBD
# Date: 2008-2010

from resizer import Resizer
import os

def __print_intro():
    print "Image Resizer" 
    print "=" * 40
    
def __print_menu():
    print
    print "Please enter your preferences for each of the Menu Options you would" 
    print "like to adjust, and enter '7' when you are done to execute your request."
    print "(note: default values for options 2-6 will be used if none are given)"
    print "-" * 40
    print "[1] Image Source"
    print "[2] Destination for resized file(s)"
    print "[3] Resized file(s) suffix"
    print "[4] Maximum file size"
    print "[5] Image resolution"
    print "[6] Upload Images -- Currently Unavailable"
    print "[7] Resize!"
    print "[8] Help"
    print "[9] Exit"
    print

def __print_help():
    print "HELP!"
    raw_input()

def __clear():
    if os.sys.platform.startswith('win'):
        os.system("cls")
    else:
        os.system("clear")
    
def display_interface():
    #"Takes Resizer objects."
    resizer = Resizer()
    __clear()
    
    choice = " "
    exit_menu = False
    __print_intro()
    while not exit_menu:
        __print_menu()
        choice = raw_input("Choice:  ")
        print
    
        # Set source path
        if choice == '1':
            path = raw_input("Please enter the path for the file(s) you would like to resize:  ")
            resizer.set_imgpath(path)
            print resizer.img_path()
            raw_input()
         
        # Set destination path
        elif choice == '2':
            dest = raw_input("Please enter the path where you would like your resized file(s) to go:  ")
            resizer.set_destination(dest)
            
        # Set file suffix
        elif choice == '3':
            suffix = raw_input("Please enter the what suffix you would like your resized file(s) to have:  ")
            resizer.set_suffix(suffix)
            
        # Set max file size
        elif choice == '4':
           max_size = raw_input("Please enter the maximum file size you would like your resized file(s) to have (in Kilobytes [KB]):  ")
           resizer.set_max_size(max_size)
            
        #  Set resolution
        elif choice == '5':
            res = raw_input("Please enter the [horizontal] resolution you would like your resized file(s) to have:  ")
            resizer.set_resolution(res)
            
        # Upload
        elif choice == '6':
            raw_input("This feature has not yet been implemented.")
            
        # Resize
        elif choice == '7':
            if not resizer.img_path():
                print "ERROR: Please provide a Source for the Image(s) in option 1 before proceeding."
            else:
                resizer.resize()
                exit_menu = True
        
        # Help
        elif choice == '8':
            __print_help()
        
        # Exit
        elif choice == '9':
            print "Goodbye!"
            exit_menu = True
            
        else:
            print "ERROR: Please enter a number between 1 and 9."
            
            
