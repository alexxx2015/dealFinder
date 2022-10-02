import requests
import re
import json
from pyquery import PyQuery
from lxml import etree

edekaBaseUrl = "https://www.edeka.de/"
edekaOffers = "https://www.edeka.de/eh/angebote.jsp"
edekaMarketSearchUrl = "https://www.edeka.de/marktsuche.jsp"
edekaApiMarketSearchUrl = "https://www.edeka.de/api/marketsearch/markets"
edekaApiProductSearchUrl = "https://www.edeka.de/api/offers"#"https://www.edeka.de/api/offers?limit=999&marketId=10001831"
    
def main():
    priceUSRegEx = re.compile("[\d]{1,}\.\d\d")
    priceEURegEx = re.compile("[\d\.]{1,},\d\d")
    dateRegEx = re.compile("\d\d\.\d\d\.\d\d\d\d")

    # fetch market store
    #https://www.edeka.de/marktsuche.jsp#/?searchstring=89079
    # https://www.edeka.de/api/marketsearch/markets?searchstring=89079
    plz = 89079
    html = requests.get(edekaApiMarketSearchUrl+"?searchstring="+str(plz))
    stores = json.loads(html.text)
    
    storeName = stores["markets"][0]["name"]
    storeMarketId = str(stores["markets"][0]["id"])
    storeUrl = stores["markets"][0]["url"].replace("index.jsp","angebote.jsp")

    print(storeUrl)
    html = requests.get(storeUrl)
    
    #Fetch product
    #pq = PyQuery(html.text)    
    #products = pq("div[data-testid='teaserwall-headline-section']")
    productUrl = edekaApiProductSearchUrl+"?limit=999&marketId="+storeMarketId
    html = requests.get(productUrl)
    products = json.loads(html.text)
    
    if "offers" in products:
        for e in products["offers"]:
            print(e["title"]+str(e["price"]["value"]))
    
    

print("Edeka parser")
main()