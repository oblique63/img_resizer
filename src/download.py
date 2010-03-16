from resizer import Resizer
import urllib

def download(url):
    local_filename = url.split('/')[-1]
    urllib.urlretrieve(url, local_filename)
    resized_img = Resier(local_filename)
    resized_img.resize()
    
