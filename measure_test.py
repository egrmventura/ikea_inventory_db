from bs4 import BeautifulSoup
import requests
import unicodedata as uni

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
product_data = product_dataset(test_url)
print(product_data)