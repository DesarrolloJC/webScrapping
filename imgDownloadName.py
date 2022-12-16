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
    arrayImg = name.split("/")
    imgNombre = arrayImg[0]
    imagen = requests.get(url).content
    with open("img/"+str(dir)+imgNombre+".jpg",'wb') as handler:
        handler.write(imagen)
        return imgNombre