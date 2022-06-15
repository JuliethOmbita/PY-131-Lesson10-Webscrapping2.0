import cmd
from bs4 import BeautifulSoup
import requests as rqs
from pprint import pprint as pp
import json
import os

"""
Hockey Teams Scrape (https://www.scrapethissite.com/pages/forms/) 
- Write the results to a .json file
- Implement pagination
"""
hokey_URL = "https://www.scrapethissite.com/"


def teams_info():
    try:
        res = rqs.get(os.path.join(hokey_URL, "pages/forms/"))
    except Exception as e:
        raise e

    soup = BeautifulSoup(res.content, "html.parser")
    links = pagination_hokey(soup)
    team_info = []

    for link in links:
        try:
            res = rqs.get(link)
        except Exception as e:
            raise e
        soup = BeautifulSoup(res.content, "html.parser")
        tr_info = soup.find_all("tr", class_="team")

        for team in tr_info:
            team_dict = {}
            team_dict["Name"] = team.find("td", class_="name").text.strip()
            team_dict["Year"] = team.find("td", class_="year").text.strip()
            team_dict["Wins"] = int(team.find("td", class_="wins").text)
            team_dict["Losses"] = int(team.find("td", class_="losses").text)
            team_dict["ot-losses"] = team.find("td", class_="ot-losses").text.strip()
            team_dict["Win porcentaje"] = float(
                soup.find("td", class_="pct").text.strip()
            )
            team_dict["Goals for"] = int(team.find("td", class_="gf").text)
            team_dict["Goals against"] = int(team.find("td", class_="ga").text)
            team_dict["Difference-score"] = int(
                team.find("td", class_="diff").text.strip()
            )
            team_info.append(team_dict)
    return team_info


def pagination_hokey(soup):
    links_pages = soup.find("ul", class_="pagination").find_all("a")
    links = [os.path.join(hokey_URL, link["href"][1:]) for link in links_pages[:-1]]
    return links


def save_json(data):
    with open("hokey_team_data.json", "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    res = teams_info()
    save_json(res)


"""
cmd
python Exercise2_webscape-hockey-team-pagination.py               
cat hokey_team_data.json | jq
"""
