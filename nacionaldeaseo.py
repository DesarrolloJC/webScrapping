import requests
from bs4 import BeautifulSoup
import openpyxl
import imgDownloadName
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def getResult(urlPro,brand,numero):
    img = ''
    driver.get(urlPro)
    time.sleep(3)
    bodyBrand = driver.execute_script("return document.body")
    sourceBrand = bodyBrand.get_attribute('innerHTML')
    soupPage = BeautifulSoup(sourceBrand, "html.parser")
    name = soupPage.find("h2",class_="product_title entry-title show-product-nav").text
    description = soupPage.find("div",class_="nda-woo-long-description")
    listImages = soupPage.find_all("img",class_="img-responsive owl-lazy")
    categoryInfo = soupPage.find("span",class_="posted_in")
    categoryArr = categoryInfo.text.split(":")
    category = categoryArr[1]
    print(name)
    print(description)
    print(brand)
    print(category)
    if listImages != []:
        contador = 1
        for imgProd in listImages:
            numNew = str(numero)+'-'+str(contador)
            imgName = imgDownloadName.downloadImages(imgProd['src'],"nacionales/",str(numNew))
            img = str(img) +","+ str(imgName) 
            print(imgProd['src'])
            contador= contador+1
    else:
        imgProd = soupPage.find_all("img",class_="porto-lazyload woocommerce-main-image img-responsive lazy-load-loaded")
        imgName = imgDownloadName.downloadImages(imgProd[0]['src'],"nacionales/",str(numero))

    hoja.append((str(name),str(brand),str(img),str(description),str(urlPro),str(category))) 

wb = openpyxl.Workbook()    # Creamos l ahoja Excel
hoja = wb.active            # Activamos la hoja Excel
hoja.title = "bodegamesones" # Agregamos un titulo a la hoja
hoja.append(('Nombre','Marca','Imagen','Descripcion','Link del producto', 'Categoria')) # Agregamos las primeras columnas con los nombres

urlDomain = "https://nacionaldeaseo.com/catalogo/"
chrome_path = r".\selenium\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.get(urlDomain)
driver.maximize_window()
time.sleep(2)
body = driver.execute_script("return document.body")
source = body.get_attribute('innerHTML')
soup = BeautifulSoup(source, "html.parser")

resultListBrands = soup.find_all("a")
cont = 1
for brand in resultListBrands:
    x = brand["href"].find("https://nacionaldeaseo.com/catalogo/?filter_marca=")
    if(x >= 0):
        brandName = str(brand.text) # -> Marca
        driver.get(str(brand["href"]))
        time.sleep(3)
        bodyBrand = driver.execute_script("return document.body")
        sourceBrand = bodyBrand.get_attribute('innerHTML')
        soupPage = BeautifulSoup(sourceBrand, "html.parser")
        listProducts = soupPage.find_all("a",class_="product-loop-title")
        for product in listProducts:
            getResult(product['href'],brandName,cont)
            cont=cont+1

wb.save('./excel/nacionalesdeaseo.xlsx') 