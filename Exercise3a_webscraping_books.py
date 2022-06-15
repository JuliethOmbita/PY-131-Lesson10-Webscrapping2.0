from bs4 import BeautifulSoup
import requests as rqs
from pprint import pprint as pp
import json
import os

"""
Books Scrape (http://books.toscrape.com) 
- Write the results to a .json file
- Implement pagination
- Add the "category" field to each entry
"""


BASE_URL = "https://books.toscrape.com/catalogue/"
default_pagues = 5


def scrape_books_pages(num_pag=default_pagues):
    """
    scrape the book by page
    """
    try:
        res = rqs.get("http://books.toscrape.com/index.html")
    except Exception as e:
        raise e
    soup = BeautifulSoup(res.content, "html.parser")
    book_info = []
    CURR_URL = "page-1.html"
    CURRENT_PAGE = 1
    while True:
        try:
            res = rqs.get(os.path.join(BASE_URL, CURR_URL))
        except Exception as e:
            raise e

        soup = BeautifulSoup(res.content, "html.parser")
        article_info = soup.find_all("article", class_="product_pod")

        for article in article_info:
            book_dict = {}
            book_dict["Name"] = article.h3.a["title"]
            book_dict["Img_src"] = article.find("img").get("src")
            book_dict["Price"] = article.find("p", class_="price_color").text.strip()
            book_dict["In_stock"] = article.find(
                "p", class_="instock availability"
            ).text.strip()
            book_dict["Rating"] = article.p["class"][1].lower()
            book_info.append(book_dict)

        print(f"Finished scraping page {CURRENT_PAGE}")
        CURR = soup.find("li", class_="next")

        if not CURR:
            break
        else:
            CURR_URL = CURR.a["href"]
        CURRENT_PAGE += 1

        if CURRENT_PAGE > num_pag:
            break
    return book_info


def scrape_books():
    """
    scrape the book by category
    """
    try:
        res = rqs.get("http://books.toscrape.com/index.html")
    except Exception as e:
        raise e
    soup = BeautifulSoup(res.content, "html.parser")
    categories_dict = category_link(soup)
    book_info = []
    for category, link in categories_dict.items():
        books_URL = link
        CURR_URL = "index.html"
        CURRENT_PAGE = 1
        while True:
            try:
                res = rqs.get(
                    os.path.join("http://books.toscrape.com/", books_URL, CURR_URL)
                )
            except Exception as e:
                raise e
            soup = BeautifulSoup(res.content, "html.parser")
            article_info = soup.find_all("article", class_="product_pod")

            for article in article_info:
                book_dict = {}
                book_dict["Name"] = article.h3.a["title"]
                book_dict["Img_src"] = article.find("img").get("src")
                book_dict["Price"] = article.find(
                    "p", class_="price_color"
                ).text.strip()
                book_dict["In_stock"] = article.find(
                    "p", class_="instock availability"
                ).text.strip()
                book_dict["Rating"] = article.p["class"][1].lower()
                book_dict["Category"] = category
                book_info.append(book_dict)

            CURR = soup.find("li", class_="next")
            if not CURR:
                break
            else:
                CURR_URL = CURR.a["href"]
            CURRENT_PAGE += 1
        # print(f"Finished scraping category {category}")
    return book_info


def category_link(soup):
    """
    Get the link of each category
    """
    links_pages = soup.find("ul", class_="nav nav-list").find_all("a")
    category_names = [link.text.strip() for link in links_pages[1:]]
    category_links = [link["href"][:-10] for link in links_pages[1:]]
    return dict(zip(category_names, category_links))


def write_to_json(results, file_name="books.json"):
    with open(file_name, "w") as outfile:
        json.dump(results, outfile)


if __name__ == "__main__":
    # pp(scrape_books_pages(3))
    # pp(scrape_books())
    results = scrape_books()
    write_to_json(results, "books.json")


"""
python Exercise3a_scraping_books.py
cat books.json | jq 
"""
