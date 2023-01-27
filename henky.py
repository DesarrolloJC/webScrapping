import requests
from bs4 import BeautifulSoup
import openpyxl
import imgDownloadName
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def getResult(urlPro):
    page = requests.get(urlPro)
    print(urlPro)
    soupProduct = BeautifulSoup(page.content, "html.parser")
    categories = soupProduct.find_all("li",class_="breadcrumb-item link-unstyled")
    category = categories[-1].text
    name = soupProduct.find("h4",class_="item-tittle").text

    imgProd = soupProduct.find("img",class_="img-thumbnail thumb-item")
    img = imgDownloadName.downloadImages(imgProd['src'],"henky/",name)

    infoM = soupProduct.find_all("div",class_="item-descripcion")
    infoArr = infoM[0].text.split("Marca:")
    marcaArr = infoArr[-1].split(" ")
    marca = str(marcaArr[0])

    infoDes = soupProduct.find_all("td",class_="w-50")

    description = infoDes[1].text
    
    print(img)
    print(name)
    print(marca)
    print(category)
    print(description)

    hoja.append((str(name),str(img),str(urlPro),str(category),str(marca),str(description))) 

wb = openpyxl.Workbook()    # Creamos l ahoja Excel
hoja = wb.active            # Activamos la hoja Excel
hoja.title = "bodegamesones" # Agregamos un titulo a la hoja
hoja.append(('Nombre','Imagen','Link del producto', 'Categoria','Marca','Descripcion')) # Columnas de nuestro archivo excel

urlDomain = "https://henki.com.mx/"
contentPage = requests.get(urlDomain)
soup = BeautifulSoup(contentPage.content, "html.parser")

chrome_path = r".\selenium\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

resultCats = soup.find_all("a") #Todas la etiquetas a
#print(resultCats)
categoriesUrls = []
for cate in resultCats:
    try:    
        x = cate['href'].find("categoria/")
        if x > 0:
            if cate['href'] in categoriesUrls:
                time.sleep(0.1)
            else:
                categoriesUrls.append(str(cate['href']))
    except:
        time.sleep(0.1)

for cat in categoriesUrls:
    driver.get(cat)
    driver.maximize_window()
    msn = driver.find_element(By.ID, "central_message")
    while msn.text != "Sin más resultados":
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    body = driver.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    soup = BeautifulSoup(source, "html.parser")
    resProductCat = soup.find_all("div",class_="items-img")
    print(len(resProductCat))
    for rpc in resProductCat:
        contentProdCat = rpc.find("a")
        urlProductCat = contentProdCat['href']
        getResult(urlProductCat)
        time.sleep(0.5)
wb.save('./excel/henky.xlsx') 