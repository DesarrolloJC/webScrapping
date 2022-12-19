import requests
import time
import os
from exif import Image

def downloadImg(url,name,dir):
    arrayImg = url.split("/")
    imgNombre= arrayImg[-1]
    imagen = requests.get(url).content
    with open("img/"+str(dir)+name+".jpg",'wb') as handler:
        handler.write(imagen)
        return imgNombre

def downloadImages(url,dir,name):
    listChar = ["/","\\","*","?",":","|","<",">",'"'," "]
    
    for c in listChar:
        res = name.find(c)
        if res > 0:
            name = name.replace(c,"_")

    imagen = requests.get(url).content
    with open("img/"+str(dir)+name+".jpg",'wb') as handler:
        handler.write(imagen)
        return name+".jpg"