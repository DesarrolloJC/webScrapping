import requests
from bs4 import BeautifulSoup
import openpyxl
import imgDownloadName
import time
import os

wb = openpyxl.Workbook()    # Creamos l ahoja Excel
hoja = wb.active            # Activamos la hoja Excel
hoja.title = "bodegamesones" # Agregamos un titulo a la hoja
hoja.append(('Nombre','Imagen','Link del producto', 'Categoria','Marca','Descripcion')) # Agregamos las primeras columnas con los nombres

def getResult(urlPro,category):
    page = requests.get(urlPro)
    soupProduc = BeautifulSoup(page.content, "html.parser")
    imgProd = soupProduc.find(id="bigpic")
    name = soupProduc.find("h1").text
    img = imgDownloadName.downloadImages(imgProd['src'],"lareynademesones/",name)

    print(img)
    print(name)
    print(category)
    print(urlPro)
    hoja.append((str(name),str(img),str(urlPro),str(category),"Definir marca","Definir descripcion")) 

urlDomain = "http://www.lareynademesones.com.mx/"
contentPage = requests.get(urlDomain)
soup = BeautifulSoup(contentPage.content, "html.parser")

resultCats = soup.find_all("a",class_="itemMenuName level4") #Categorias padre

for cat in resultCats:
    urlCat = cat["href"] 
    nameCat = cat.text
    categoryName = nameCat.replace('-',' ')
    print(categoryName)
    #print(urlCat)

    urlCategory = requests.get(urlCat)
    soupCategory = BeautifulSoup(urlCategory.content, "html.parser")
    prodCategories = soupCategory.find_all("a",class_="product_image")

    for pc in prodCategories:
        #print(pc["href"])
        getResult(pc["href"],categoryName)
    

    
wb.save('./excel/lareynademesones.xlsx')    # Guardamos el Excel

