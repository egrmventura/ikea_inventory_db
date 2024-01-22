from bs4 import BeautifulSoup
import requests

url2 = "https://www.newegg.com/lacie-model-stfr5000800-5tb/p/2WA-0009-000F0?Item=2WA-0009-000F0&SoldByNewegg=1"
url3 = "https://www.ikea.com/us/en/p/uppland-sectional-4-seat-corner-blekinge-white-s49384110/"
results = requests.get(url3)


with open(results, 'r') as f:
    contents =  f.read()
    soup = BeautifulSoup(contents, "html.parser")


    for child in soup.descendants:
        if child.name:
            print(child.name)