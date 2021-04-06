import pandas as pd
import requests
import json
import re

from pandas import json_normalize
from selectorlib import Extractor

from time import sleep

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('venv/data/search_results.yml')


def scrape(url):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s" % url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)


# product_data = []
def startRead():
    with open("venv/data/search_results_urls.txt", 'r') as urllist, open('venv/data/search_results_output.jsonl', 'w') as outfile:
        for url in urllist.read().splitlines():
            data = scrape(url)
            if data:
                for product in data['products']:
                    product['search_url'] = url
                    print("Saving Product: %s" % product['title'])
                    json.dump(product, outfile)
                    outfile.write("\n")
                    # sleep(5)
    pass


def getAsin():
    with open('venv/data/search_results_output.jsonl', 'r') as json_file:
        json_list = list(json_file)

    for json_str in json_list:
        result = json.loads(json_str)
        print("New Element")
        asin = re.search("B0[\d\w]{8}",str(result['url']))
        print("asin -> " + asin.group())
        print("title -> " + str(result['title']))
        print("url -> " + str(result['url']))
        print("rating -> " + str(result['rating']))
        print("reviews -> " + str(result['reviews']))
        print("price -> " + str(result['price']))
        print("search_url -> " + str(result['search_url']))
    pass


def getHistoricData():
    with open('venv/data/search_results_output.jsonl', 'r') as json_file:
        json_list = list(json_file)
    search_df = pd.DataFrame(columns=['asin','title','url','rating','reviews','price_day_call', 'search_url'])
    df_iniciado = False

    for index, json_str in enumerate(json_list):
        print ("iteracion " + str(index+1) + " de " + str(len(json_list)))

        result = json.loads(json_str)

        print("New Element")
        asin = re.search("B0[\d\w]{8}", str(result['url']))

        print("asin -> " + asin.group())
        print("title -> " + str(result['title']))
        print("url -> " + str(result['url']))
        print("rating -> " + str(result['rating']))
        print("reviews -> " + str(result['reviews']))
        print("price -> " + str(result['price']))
        print("search_url -> " + str(result['search_url']))

        new_row ={
            'asin':asin.group(),
            'title':str(result['title']),
            'url':str(result['url']),
            'rating':str(result['rating']),
            'reviews':str(result['reviews']),
            'price':str(result['price']),
            'search_url':str(result['search_url'])
        }

        try:
            json_response = amazonPriceRequest(asin.group())
            json_normalized = json_normalize(data=json_response.json(), record_path='price_history',
                                             meta=['asin', 'currency', 'price_type'])
            if df_iniciado==False:
                json_df = json_normalized
                df_iniciado = True
            else:
                json_df = json_df.append(json_normalized, ignore_index=True, sort=False)
            search_df = search_df.append(new_row, ignore_index=True)
        except:
            print("Response - KO")

    df_merge = pd.merge(json_df,search_df, on='asin')
    df_merge.to_csv(r'venv/data/data.csv',index=False,header=True)
    pass

def amazonPriceRequest(asin):
    url = "https://amazon-price-history.p.rapidapi.com/api/us/price_history"

    querystring = {"asin":asin,"price_type":"amazon"}

    headers = {
        'x-rapidapi-key': "7a03787ae6msh833680465f5a2aep1dc51cjsnbd77cf857f41",
        'x-rapidapi-host': "amazon-price-history.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response



print(" -1- **** FASE 1 **** scrapping amazon")
print(" -2- **** FASE 2 **** recuperar asin (identificador único de producto")
print(" -3- **** FASE 3 **** llamada API histórico precios")

opcion = -1

while opcion < 0 or opcion > 3:
    opcion = (int(input("Elija una opción ")))
    if opcion == 1:
        startRead()
    elif opcion == 2:
        getAsin()
    elif opcion == 3:
        getHistoricData()
    else:
        print("opcion incorrecta")
