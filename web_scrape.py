from bs4 import BeautifulSoup
import requests

url_prod = "https://www.ikea.com/us/en/cat/products-products/"
url_prod_furn_sofa_fabr_sect = "https://www.ikea.com/us/en/cat/fabric-sectionals-10671/"
url_prod_furn_sofa_fabr_sect_uppland  = "https://www.ikea.com/us/en/p/uppland-sectional-4-seat-corner-blekinge-white-s49384110/"

result = requests.get(url_prod_furn_sofa_fabr_sect_uppland)
soup = BeautifulSoup(result.text, "html.parser")
article_id_list = soup.find_all(string="Article Number")
for f in range(len(article_id_list)):
    parents = article_id_list[f].parent.parent
    print(parents)
print(article_id_list)