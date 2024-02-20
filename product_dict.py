from bs4 import BeautifulSoup
import requests
import json

#get urls - surfing web scrape into unique list/ tuple?
#after or while attaining urls, run dictionary summaries
product_dict = {"product_category" : None}

def product_input(prod_url, product_dict):
    soup = product_soup(prod_url)
    product_raw_list = product_data(soup)
    #product_raw_list[0] = product_category key (i.e. "furniture")
    #product_raw_list[1] = product_sub_category key 1 (i.e. "sofas & sectionals")
    #product_raw_list[2] = product_data dict
    if product_dict["product_category"] == None: 
        product_dict["product_category"] = {product_raw_list[0] : {product_raw_list[1] : product_raw_list[2]}}
        return product_dict
    try:
        return product_dict["product_category"][product_raw_list[0]][product_raw_list[1]].append(product_raw_list[2])
    except KeyError:
        pass # product_category or product_sub_category do not exist
    try: 
        product_dict["product_category"][product_raw_list[0]][product_raw_list[1]] = product_raw_list[2]
        return product_dict
    except KeyError:
        pass # product_category does not exist
    try:
        product_dict["product_category"][product_raw_list[0]] = {product_raw_list[1] : product_raw_list[2]}
        return product_dict
    except:
        return product_dict # duplicate product or bug in web scrape