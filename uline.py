#https://es.uline.mx/Cls_18/Safety-Products
import requests
from bs4 import BeautifulSoup
import openpyxl
import imgDownloadName

urlDomain = "https://es.uline.mx/Cls_18/Safety-Products"

urlCat = ''
urlPro = ''

wb = openpyxl.Workbook()    # Creamos l ahoja Excel
hoja = wb.active            # Activamos la hoja Excel
hoja.title = "bodegamesones" # Agregamos un titulo a la hoja
hoja.append(('Nombre','Marca','Imagen','Descripcion','Link del producto', 'Categoria')) # Agregamos las primeras columnas con los nombres

#print(resultListUrl)
def getResult(urlPro):
    contentPage = requests.get(urlPro)
    soup = BeautifulSoup(contentPage.content, "html.parser")
    arr = urlPro.split("/")
    name = str(arr[-1])

    """Obtener Categoria"""
    urlsProd = soup.find_all("a")
    for u in urlsProd:
        try:
            x = u["href"].find("Cls")
            cate = u["href"].text
            category = str(cate)
            break
        except:
            print("sin url")
    """Obtener Categoria"""

    desc = soup.find("td",class_="BrowseCopy subGroupCopy")
    description = desc.text

    brand = "uline"

    image = soup.find("img",class_="itemResultImage")
    img = imgDownloadName.downloadImages(image["src"],"uline/",name)
    print(name)
    print(brand)
    print(description)
    print(category)
    print(img)
    hoja.append((str(name),str(brand),str(img),str(description),str(urlPro),str(category))) 

def getURLS(urlDomain):
    contentPage = requests.get(urlDomain)
    soup = BeautifulSoup(contentPage.content, "html.parser")
    resultListUrl = soup.find_all("a")
    for url in resultListUrl:
        try:
            res = url["href"].find("Grp_")
            if(res >= 0):
                urlCat = str(url["href"])
                print(urlCat)
                getURLS(urlCat)
            else:
                res = url["href"].find("BL_")
                if(res >= 0):
                    urlPro = str(url["href"])
                    print(urlPro)
                    getResult(urlPro)
                else:
                    res = url["href"].find("Cls_")
                    if(res >= 0):
                        urlCls = str(url["href"])
                        print(urlCls)
                        #getURLS(urlCls)
        except:
            print("Fallo en "+str(url))

getURLS(urlDomain)

wb.save('./excel/uline.xlsx') 