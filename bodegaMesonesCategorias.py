import requests
from bs4 import BeautifulSoup
import openpyxl
import imgDownloadName
import time
import os

wb = openpyxl.Workbook()    # Creamos l ahoja Excel
hoja = wb.active            # Activamos la hoja Excel
hoja.title = "bodegamesones" # Agregamos un titulo a la hoja
hoja.append(('Nombre','Marca','Imagen','Descripcion','Link del producto', 'Categoria')) # Agregamos las primeras columnas con los nombres



def getResult(urlPro,category):
    print("categoria ingresada:"+str(category))
    page = requests.get("https://www.bodegamesones.mx"+urlPro)
    soupProduc = BeautifulSoup(page.content, "html.parser")
    imgTag = soupProduc.find("img",class_="product-gallery__image")
    img = "https:"+imgTag["data-zoom"]
    nameProd = soupProduc.find("h1",class_="product-meta__title heading h1")
    name = nameProd.text
    brandPro = soupProduc.find("a", class_="product-meta__vendor")
    brandInfo = brandPro.text
    brand = brandInfo.split(":")
    infoDesc = soupProduc.find("div",class_="rte text--pull")
    descrip = infoDesc.text
    imgArr = img.split("?v")
    img = imgArr[0]
    img = imgDownloadName.downloadImages(img,"bodegamesones/",name)
    print(img)
    print(name)
    print(brand[1])
    print(descrip)
    hoja.append((str(name),str(brand[1]),str(img),str(descrip),str(urlPro),str(category)))
   
    #print(urlcompuesta)

urlDomain = "https://www.bodegamesones.mx/"
contentPage = requests.get(urlDomain)
soup = BeautifulSoup(contentPage.content, "html.parser")

resultCats = soup.find_all("a",class_="nav-dropdown__link link")

for cat in resultCats:
    urlCat = cat["href"] 
    nameCat = cat.text
    print(nameCat)

    urlCategory = str(urlDomain)+str(urlCat)
    contentPageCat = requests.get(urlCategory)
    soupCat = BeautifulSoup(contentPageCat.content, "html.parser") #Obetnemos la info de la pagina de la categoria actual

    numPag = soupCat.find_all("a",class_="pagination__nav-item link")

    if(numPag):
            lastPag = numPag[-1]
            for page in range(1,int(lastPag.text)+1):
                urlcompuesta = str(urlCategory)+"?page="+str(page)
                print("URL: "+str(urlcompuesta))
                contentPageForURL = requests.get(urlcompuesta)
                soupCatForURL = BeautifulSoup(contentPageForURL.content, "html.parser")
                resultsCatsPro = soupCatForURL.find_all("a",class_="product-item__image-wrapper" ) #Se obtiene los productos de esa categoria
                for p in resultsCatsPro:
                    urlPro = p["href"]
                    print("url producto: "+str(urlPro))
                    getResult(urlPro,nameCat)
    

    
wb.save('./excel/bodegamesonesTodosLosProductos.xlsx')    # Guardamos el Excel

