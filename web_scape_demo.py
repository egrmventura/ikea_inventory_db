from bs4 import BeautifulSoup
import requests
import json

url2 = "https://www.newegg.com/lacie-model-stfr5000800-5tb/p/2WA-0009-000F0?Item=2WA-0009-000F0&SoldByNewegg=1"
url3 = "https://www.ikea.com/us/en/p/uppland-sectional-4-seat-corner-blekinge-white-s49384110/"

ikea_catalog_json = {}

def product_soup(prod_url):
    results = requests.get(prod_url)
    soup = BeautifulSoup(results.text, "html.parser")
    return soup
    # article_id_list = soup.find_all(string="Article Number")

def product_main(soup):
    item_id = soup.find("span", class_="pip-product-identifier__value").string
    item_name_series = soup.find("div", class_="pip-header-section__container-text").find("span").string
    item_description_parts = soup.find("span", class_="pip-header-section__description")
    item_description = item_description_parts.find("span").string
    try:
        item_descr_append = " " + item_description_parts.find(class_="pip-link-button pip-header-section__description-measurement").string
    except:
        item_descr_append = ""
    item_description = item_description + item_descr_append

def product_parts(soup):
    
# for f in range(len(article_id_list)):
#     parents = article_id_list[f].find_parent('div').parent


#     print(parents)
# parents = article_id_list[1].find_parent('div').parent
print(item_id)
print(item_name_series)
print(item_description)
# print(parents)
print(article_id_list)