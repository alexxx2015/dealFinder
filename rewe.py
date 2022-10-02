import requests
import re
import json
import urllib.parse
import cloudscraper
import cfscrape
from pyquery import PyQuery
from lxml import etree

reweBaseUrl = "https://www.rewe.de"
reweSearchUrl = "https://www.rewe.de/api/marketsearch?searchTerm="#89079" 
reweOfferUrl = "https://www.rewe.de/angebote/"
reweOfferUrlMobile = "https://mobile-api.rewe.de/api/v3/all-offers?marketCode="
reweUrl = [
    
]

        
def main():
    proxies={"http":"127.0.0.1:8080","https":"127.0.0.1:8080"}
    priceUSRegEx = re.compile("[\d]{1,}\.\d\d")
    priceEURegEx = re.compile("[\d\.]{1,},\d\d")
    dateRegEx = re.compile("\d\d\.\d\d\.\d\d\d\d")
    marketsCookie = json.loads('{"online":{},"stationary":{"wwIdent":"840266","marketZipCode":"89079","serviceTypes":["STATIONARY"]}}')
    reweHeaders = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36","Referrer Policy":"strict-origin-when-cross-origin"}
    reweHeaders = {}

    #fetch local store data
    reweStorePLZ = "76187"
    print("request "+str(reweStorePLZ))
    html = requests.get(reweSearchUrl+reweStorePLZ)    
    resp = html.json()
    marketsCookie["stationary"]["wwIdent"] = resp[0]["wwIdent"]
    marketsCookie["stationary"]["marketZipCode"] = resp[0]["contactZipCode"]
    
    marketCode = resp[0]["wwIdent"]
    reweHeaders["rd-market-id"] = resp[0]["wwIdent"]
    reweHeaders["rd-postcode"] = resp[0]["contactZipCode"]
    reweHeaders["User-Agent"] = "REWE-Mobile-App/3.4.56 Android/7.1.1 (Tablet)"
    #reweHeaders["Host"] = "mobile-api.rewe.de"
    reweHeaders["ruleVersion"] = "3"
    reweHeaders["rdfa"] = "eb66f508-2f21-4957-8c7f-bb24cec166fd"
    reweHeaders["Correlation-Id"] = "4df758c0-7164-4602-ba1f-70264d31428d"
    reweHeaders["Connection"] = "Keep-Alive"

    #fetch product data
    #https://mobile-api.rewe.de/api/v3/all-offers?marketCode=840277
    print("start calling")
    reqUrl = reweOfferUrlMobile+str(marketCode)
    print("calling "+reqUrl)
    html = requests.get(reqUrl, headers=reweHeaders, verify=False)#, cert=("E:\git_repo\dealFinder\key.pem","E:\git_repo\dealFinder\cert.pem")#, cookies=html.cookies
    print(html.status_code)
    products = json.loads(html.text)
    for k in products["categories"]:
        print(k["title"])
        
        for e in k["offers"]:            
            if ("priceData" in e and "price" in e["priceData"]):
                print(e["title"]+" "+e["priceData"]["price"])
            else:
                print(e["title"])

    exit()
    
    urlAdded = False
    for x in reweUrl:
        print(x)
        html = requests.get(x, cookies={"x-aem-variant":"DE1730"})
        pq = PyQuery(html.text)

        # add missing urls from categories
        if urlAdded == False:
            urlAdded = True
            categories = pq("div.t-offers-overview__categories a")
            if categories is not None:
                for e in categories:
                    reweUrl.append(reweBaseUrl + e.get("href"))            


        
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
    
    

print("Rewe parser")
main()