import requests
from pyquery import PyQuery
from lxml import etree
import re

aldiUrl = {
    "fresh":"https://www.aldi-sued.de/de/angebote/frischekracher.html"
    , "priceAction":"https://www.aldi-sued.de/de/angebote/preisaktion.html"
    , "brandAction": "https://www.aldi-sued.de/de/angebote/markenaktion-der-woche.html"
    }

def extractDates(e):
    txt = PyQuery(e).text()
    cmp = txt.split("bis")
    if(len(cmp) == 2):
        print ("K")
        
def main():
    priceUSRegEx = re.compile("[\d]{1,}\.\d\d")
    priceEURegEx = re.compile("[\d\.]{1,},\d\d")
    dateRegEx = re.compile("[\d]{1,2}\.[\d]{1,2}\.")
    for x in aldiUrl:
        print(aldiUrl[x])
        html = requests.get(aldiUrl[x])        
        pq = PyQuery(html.text)

        productDesc = pq("div.E12-grid-gallery")
        week = pq("div.E05-basic-text div div div div h2")
                
        for idx, e in enumerate(week):
            weekHeading = PyQuery(e).text()
            print("\n"+weekHeading)

            dateFromTo = dateRegEx.findall(weekHeading)
            print(dateFromTo)

            if idx >= len(productDesc):
                break
            prodGrid = PyQuery(productDesc[idx])
            for n in prodGrid("figcaption"):
                products = PyQuery(n)
                productTitle = products("h3").text()
                productPrice = products("p").eq(2).remove("span").text()
                priceRes = priceUSRegEx.search(productPrice)
                if priceRes is None:
                    productPrice = products("p").eq(1).remove("span").text()
                    priceRes = priceUSRegEx.search(productPrice)
                if priceRes is not None:
                    productPrice = priceRes.group()
                
                print(productTitle + " " + productPrice)
        
        #break
    
    

print("Aldi parser")
main()