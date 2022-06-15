from bs4 import BeautifulSoup
import requests as rqs
from pprint import pprint as pp
import json

"""
This file is webscraping the countries of the world information
Web side: https://www.scrapethissite.com/pages/simple/
    Country Name
    Capital  
    Population
    Area    

- Saving it to json file

- Create a CLI that helps us sort this data from a .json file by different metrics ("population", "surface area" .. )
i.e.
"""


def countries_info():
    try:
        res = rqs.get("https://www.scrapethissite.com/pages/simple/")
    except Exception as e:
        raise e

    soup = BeautifulSoup(res.content, "html.parser")
    divs_info = soup.find_all("div", class_="col-md-4 country")
    country_info = []

    for country in divs_info:
        cnty_dict = {}
        cnty_dict["Name"] = country.h3.text.strip()
        cnty_dict["Capital"] = country.find("span", class_="country-capital").text
        cnty_dict["Population"] = country.find("span", class_="country-population").text
        cnty_dict["Area"] = country.find("span", class_="country-area").text
        country_info.append(cnty_dict)
    return country_info


def save_json(data):
    with open("world_data.json", "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    res = countries_info()
    save_json(res)

"""
cmd
python Exercise1a_webscrapping-countries.py               
cat world_data.json | jq
"""
