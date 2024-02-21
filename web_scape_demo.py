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
    product_id = soup.find("span", class_="pip-product-identifier__value").string
    product_series = soup.find("div", class_="pip-header-section__container-text").find("span").string
    product_description_parts = soup.find("span", class_="pip-header-section__description")
    product_description = product_description_parts.find("span").string
    try:
        product_descr_append = " " + product_description_parts.find(class_="pip-link-button pip-header-section__description-measurement").string
    except:
        product_descr_append = ""
    product_description = product_description + product_descr_append

def product_parts(soup):

    for f in range(len(article_id_list)):
        parents = article_id_list[f].find_parent('div').parent


#     print(parents)
# parents = article_id_list[1].find_parent('div').parent

print(item_id)
print(item_name_series)
print(item_description)
# print(parents)
print(article_id_list)

'''
    json = {
        products_category : {
            furniture : {
                product_data : {
                    product_id : '994.319.82',
                    product_series : 'LAGKAPTEN / ALEX',
                    product_description : 'Desk, white, 55 1/8x23 5/8 "',
                    packaging_data : {
                        package_id : '404.608.15'
                        package_series : 'LAGKAPTEN',
                        package_description : 'Tabletop',
                        package : {
                            package_ord : 1,
                            width : 24.0,
                            height : 1.5,
                            length : 55.5,
                            weight : 18.625,
                            count : 1
                        }
                    },
                    {
                        package_id : '004.735.46',
                        package_series : 'ALEX',
                        package_description : 'Drawer unit',
                        package : {
                            package_ord : 1,
                            width : 23.5,
                            height : 4.25,
                            length : 32.0,
                            weight : 61.6875,
                            count : 2
                        }
                    },
                    prod_url : 'https://www.ikea.com/us/en/p/lagkapten-alex-desk-white-s99431982/'
                },
                {
                    product_id : '493.841.10',
                    product_series : 'UPPLAND',
                    product_description : 'Sectional, 4-seat corner, Blekinge white',
                    packaging_data : {
                        package_id : '904.727.07',
                        package_series : 'UPPLAND',
                        package_description : 'Frame for corner secional, 4-seat'
                        package : {
                            package_ord : 1,
                            width : 36.5,
                            height : 17.25,
                            length : 61.0,
                            weight : 122.6875,
                            count : 1
                        },
                        {
                            package_ord : 2,
                            width : 36.5,
                            height : 17.25,
                            length : 61.0,
                            weight : 110.25,
                            count : 1
                        },
                        {
                            package_ord : 3,
                            width : 36.25,
                            height : 25.5,
                            length : 36.5,
                            weight : 73.0625,
                            count : 1
                        }
                    },
                    {
                        package_id : '804.876.29',
                        package_series : 'UPPLAND',
                        package_description : 'Cover for sectional, 4-seat',
                        package : {
                            package_ord : 1,
                            width : 14.75,
                            height : 5.5,
                            length : 29.75,
                            weight : 24.5,
                            count : 1
                        }
                    }
                    product_url : 'https://www.ikea.com/us/en/p/uppland-sectional-4-seat-corner-blekinge-white-s49384110/'
                }

            }
        }
    }
'''