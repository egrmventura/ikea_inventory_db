from bs4 import BeautifulSoup
import requests

url2 = "https://www.newegg.com/lacie-model-stfr5000800-5tb/p/2WA-0009-000F0?Item=2WA-0009-000F0&SoldByNewegg=1"
url3 = "https://www.ikea.com/us/en/p/uppland-sectional-4-seat-corner-blekinge-white-s49384110/"
results = requests.get(url3)

soup = BeautifulSoup(results.text, "html.parser")
article_id_list = soup.find_all(string="Article Number")

# for f in range(len(article_id_list)):
#     parents = article_id_list[f].find_parent('div').parent


#     print(parents)
parents = article_id_list[1].find_parent('div').parent

print(parents)
print(article_id_list)