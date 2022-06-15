import argparse
import json
from pprint import pprint as pp
from tkinter import E
from Exercise3a_webscraping_books import scrape_books_pages, write_to_json

"""
CLI
Allows us to only download a specific number of pages from the pagination and also 
search results by title and output to a specfic file output.json
i.e. Will download 10 pages of results:
    python3 scraper_books.py --pages 10
i.e. search results by title
    python3 scraper_books.py --input books.json --search "1st"
    -> "1st to Die (Women's Murder Club #1)"
i.e. write to output
    python3 scraper_books.py --pages 10 --output books.json
"""


def books_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=argparse.FileType("r"),
        help="Books information - json file",
    )

    parser.add_argument(
        "-p",
        "--pages",
        type=int,
        action="store",
        help="Number of pages to download",
    )

    parser.add_argument(
        "-se",
        "--search",
        action="store",
        help="Search by title",
    )

    args = parser.parse_args()

    if args.search and args.input:
        try:
            res = json.load(args.input)
        except Exception as e:
            raise e
        search_results = []
        for entry in res:
            if args.search.lower() in entry["Name"].lower():
                search_results.append(entry)

        print(f"{len(search_results)} results were found: ")
        for result in search_results:
            pp(result)

    if args.pages:
        results = scrape_books_pages(args.pages)
        file_name = "".join(["books-scraped-", str(args.pages), "-pages.json"])
        write_to_json(results, file_name)
        print(f"Wrote {args.pages} scraped pages to {file_name}")


if __name__ == "__main__":
    books_cli()


"""
cmd
python3 Exercise3b_book-CLI.py -i books.json -se  "The Long Shadow" 
python3 Exercise3b_book-CLI.py -p 3
cat books-scraped-3-pages.json | jq .
"""
