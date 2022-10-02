import requests
from pyquery import PyQuery
from lxml import etree
import re

kauflandBaseUrl = "https://filiale.kaufland.de"
kauflandUrl = [
    "https://filiale.kaufland.de/angebote/aktuelle-woche/uebersicht.category=01_Fleisch__Gefl%C3%BCgel__Wurst.html"
]

def extractDates(e):
    txt = PyQuery(e).text()
    cmp = txt.split("bis")
    if(len(cmp) == 2):
        print ("K")
        
def main():
    priceUSRegEx = re.compile("[\d]{1,}\.\d\d")
    priceEURegEx = re.compile("[\d\.]{1,},\d\d")
    dateRegEx = re.compile("\d\d\.\d\d\.\d\d\d\d")
    urlAdded = False
    for x in kauflandUrl:
        print(x)
        html = requests.get(x, cookies={"x-aem-variant":"DE1730"})
        pq = PyQuery(html.text)

        # add missing urls from categories
        if urlAdded == False:
            urlAdded = True
            categories = pq("div.t-offers-overview__categories a")
            if categories is not None:
                for e in categories:
                    kauflandUrl.append(kauflandBaseUrl + e.get("href"))            


        
        week = pq("div.a-icon-tile-headline__subheadline").text()
        dateFromTo = dateRegEx.findall(week)
        if dateFromTo is not None:
            print(dateFromTo)
        print(week)
        

        productDesc = pq("div.t-offers-overview__tiles .o-overview-list .m-offer-tile")           

        for idx, e in enumerate(productDesc):
            product = PyQuery(e)            
            productTitle = product(".m-offer-tile__text .m-offer-tile__title").text()
            productPrice = product(".a-pricetag__price").text()
            print(productTitle + " " +productPrice)
        #break
    
    

print("Kaufland parser")
main()