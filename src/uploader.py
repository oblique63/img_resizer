# Program: Image Resizer
# Module Description: Image Uploader
# Author: Enrique Gavidia
# E-mail: enrique@enriquegavidia.com
# License: TBD
# Date: 2008-2010

class ImgUploader():
    def __init__(self, resizer, server_info):
        """Accepts one Resizer object, and a tuple: 
        (host,login,password,[Directory])"""
        self.__source = resizer.destination()
        self.__server = {
            'host': server_info[0],
            'login': server_info[1],
            'pass': server_info[2]
            'dir': ''
        }
        if server_info[3]:
            self.__server['dir'] = server_info[3]
        
