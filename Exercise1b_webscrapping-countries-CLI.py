import argparse
import json
from pprint import pprint as pp
from tkinter import E

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--input",
    type=argparse.FileType("r"),
    required=True,
    help="Country information - json file",
)
field_name = ["Population", "Name", "Area", "Capital"]
parser.add_argument(
    "-s",
    "--sort",
    type=str,
    choices=field_name,
    help="Sort json file by field name",
    action="store",
)
args = parser.parse_args()

try:
    res = json.load(args.input)
except Exception as e:
    raise e


# pp(res)
if args.sort == "Population":
    print("input Populationiii009")
elif args.sort == "Name":
    pass
elif args.sort == "Area":
    pass
elif args.sort == "Capital":
    pass

"""
cmd
python3 Exercise1b_webscrapping-countries-CLI.py -i books.json -se  "Population"
"""
