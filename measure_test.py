from bs4 import BeautifulSoup
import requests
import unicodedata as uni
import json

test = 'Width : 36 ½ "'
test2 = 'Weight :  15 lb 4 oz'
test3 = 'Package(s) : 1'

def soup_shop(url):
    global soup
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    return soup

def product_dataset(url):
    global product_dict
    product_dict = {}
    soup = soup_shop(url)
    product_dict["product_id"] = soup.find("span", class_ = "pip-product-identifier__value").string
    product_dict["product_series"] = soup.find("div", class_ = "pip-header-section__container-text").find("span").string
    product_description_soup = soup.find("span", class_ = "pip-header-section__description")
    product_description = product_description_soup.find("span").string
    try:
        product_description += " " + product_description_soup.find(class_ = "pip-link-button pip-header-section__description-measurement").string
    except: pass
    product_dict["product_description"] = product_description
    packaging_soup = soup.find("div", class_ = "pip-product__left-bottom").find("div", class_ = "pip-seo-content")
    product_dict["packaging_count"] = packaging_soup.find("div", class_ = "pip-product-dimensions__package-count").string
    product_dict["packaging_data"] = []
    for packaging in packaging_soup.find_all("div", class_ = "pip-product-dimensions__package-container"):
        packaging_dict = packaging_dataset(packaging)
        product_dict["packaging_data"].append(packaging_dict)
    product_dict["product_url"] = url
    return product_dict

def packaging_dataset(packaging):
    global packaging_dict
    packaging_dict = {}
    packaging_dict["packaging_id"] = packaging.find("span", class_ = "pip-product-identifier__value").string
    packaging_dict["packaging_series"] = packaging.find("span", class_ = "pip-product-dimensions__package-header notranslate").string
    packaging_dict["packaging_description"] = packaging.find("span", {"aria-hidden" : "true"}).string
    package_list = package_dataset(packaging)
    packaging_dict["package"] = package_list
    return packaging_dict

def package_dataset(packaging):
    global package_list
    package_list = []
    package_ord = 1
    for package in packaging.find_all("div", class_ = "pip-product-dimensions__measurement-container"):
        package_dict = {}
        package_dict["package_ord"] = package_ord
        for measurement in package.find_all("p", class_ = "pip-product-dimensions__measurement-wrapper"):
            measurement_list = measurement_break(measurement)
            package_dict[measurement_list[0]] = measurement_list[1]
        measurement = packaging.find("p", class_ = "pip-pip-product-dimensions__measurement-wrapper")
        measurement_list = measurement_break(measurement)
        package_dict[measurement_list[0]] = measurement_list[1]
        package_ord+=1
        package_list.append(package_dict)
    return package_list

def measurement_break(measurement):
    list = [None,[[],[]],0]
    list[0] = measurement.get_text().split(":")[0].lower()
    measure = measurement.get_text().split(":")[1][1:] if uni.name(measurement.get_text().split(":")[1][:1]).split()[-1] == "SPACE" else measurement.get_text().split(":")[1]
    for piece in measure.split():
        measure_stage = list[2]
        if piece.isnumeric():
            try:
                piece = uni.numeric(piece)
            except TypeError: pass
            try:
                list[1][0][measure_stage]+=float(piece)
            except:
                list[1][0].append(float(piece))
        
        elif piece.isalpha():
            list[1][1].append(piece)
            if len(list[1][0]) < list[2]+1: list[1][0].append(0)
            list[2]+=1
        else:
            try:
                if uni.name(piece).split()[0] in ["APOSTROPHE", "QUOTATION"]:
                    list[1][1].append(piece)
                    if len(list[1][0]) < list[2]+1: list[1][0].append(0)
                    list[2]+=1
            except: pass
    if len(list[1][0]) > len(list[1][1]): list[1][1].append("count")
    list_output = unit_conversion(list[1])

    return [list[0], list_output]

def unit_conversion(measurement_list):
    list_output = [0, None]
    for n in range(len(measurement_list[0])):
        try:
            if uni.name(measurement_list[1][n]).split()[0] == "APOSTROPHE":
                coef = 12
            elif uni.name(measurement_list[1][n]).split()[0] == "QUOTATION":
                coef = 1
            if list_output[1] == None: list_output[1] = "inches"
            if list_output[1] == "inches": list_output[0] += (coef * measurement_list[0][n])
        except:
            if measurement_list[1][n] == "lb":
                coef = 1
            elif measurement_list[1][n] == "oz":
                coef = 0.0625
            if measurement_list[1][n] == "count" and list_output[1] == None:
                list_output[1] = "count"
                list_output[0] = measurement_list[0][n]
            if list_output[1] == None: list_output[1] = "lb"
            if list_output[1] == "lb": list_output[0] += (coef * measurement_list[0][n])          

    return list_output

test_url = 'https://www.ikea.com/us/en/p/uppland-sectional-4-seat-corner-blekinge-white-s49384110/'
test_url_bed = 'https://www.ikea.com/us/en/p/hemnes-bed-frame-with-2-storage-boxes-dark-gray-stained-loenset-s69275214/#content'
product_data = product_dataset(test_url_bed)

pretty_json = json.dumps(product_data, indent=4)

print(pretty_json)

'''
-- above python script creates product_data dictionary --

-- demo of json from comprising product_data from mutliple urls --

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