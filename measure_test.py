from bs4 import BeautifulSoup
import requests
import unicodedata as uni

test = 'Width : 36 ½ "'
test2 = 'Weight :  15 lb 4 oz'
test3 = 'Package(s) : 1'

def soup_shop(url):
    global soup
    result = requests.get(url)
    soup = BeautifulSoup(result.text)
    return soup

def product_summary(url):
    soup = soup_shop(url)

def product_dataset(soup):
    global product_dict
    product_dict = {}
    pack = soup.find("div", class_ = "pip-seo-content").find("div", class_ = "pip-product-dimensions__package-container")
    product_dict["product_id"] = pack.find("span", class_ = "pip-product-identifier__value").string
    product_dict["product_series"] = pack.find("span", class_ = "pip-product-identifier__value").string
    product_dict["product_description"] = pack.find("span", {"aria-hidden" : "true"}).string

def package_dataset(pack, package_ord=0):
    global package_dict
    package_dict = {}
    for package in pack.find_all("div", class_="pip-product-dimensions__measurment-container"):
        package_dict["package_ord"] = package_ord + 1
        for measurement in package.find_all("p", class_ = "pip-product-dimensions__measurement-wrapper"):
            measurement_list = measurement_break(measurement)
            package_dict[measurement_list[0]] = measurement_list[1]

def measurement_break(measurement):
    list = [None,[[],[]],0]
    list[0] = measurement.split(":")[0][:-1].lower()
    measure = measurement.split(":")[1][1:] if uni.name(measurement.split(":")[1][:1]).split()[-1] == "SPACE" else measurement.split(":")[1]
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
            if list_output[1] == None: list_output[1] = "lb"
            if list_output[1] == "lb": list_output[0] += (coef * measurement_list[0][n])
    return list_output

measure_dict = {}
for nTest in [test, test2, test3]:
    temp = measurement_break(nTest)
    measure_dict[temp[0]] = temp[1]

print(measure_dict)