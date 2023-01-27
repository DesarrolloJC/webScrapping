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

def getExtension(nameImg):
    arrEtx = [".jpg",".png",".jpeg"]
    for e in arrEtx:
        res = nameImg.find(e)
        if res > 0:
            arrImg = nameImg.split(".")
            ext = arrImg[-1]
            return ext
    return "jpg"

def downloadImages(url,dir,name):
    listChar = ["/","\\","*","?",":","|","<",">",'"'," "]
    
    for c in listChar:
        res = name.find(c)
        if res > 0:
            name = name.replace(c,"_")
    ext = getExtension(url)
    print("extencion: "+str(name)+"."+str(ext))
    if os.path.isfile("img/"+str(dir)+name+"."+str(ext)):
        return name+"."+str(ext)
    else:
        print("No existe el archivo.")
        imagen = requests.get(url).content
        try:
            with open("img/"+str(dir)+name+"."+str(ext),'wb') as handler:
                handler.write(imagen)
                return name+"."+str(ext)
        except:
            return url