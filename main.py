from typing import List, Dict

from actions.ARKWiki import ARKWiki
from classes.ManualPage import ManualPage
from utils import file_utils, template_utils

wiki = ARKWiki()

lines = []
with open("items.txt", "r") as f:
    for l in f.readlines():
        lines.append(l.replace("\n", ""))
    lines.sort()

if wiki.login_result == "Success":
    file_utils.create_pages_json(lines, wiki, True)
    file_utils.create_pages_fast_json(lines, wiki)

    pages: List[ManualPage] = file_utils.get_pages_json("json/pages.json")
    pages_fast: List[ManualPage] = file_utils.get_pages_json("json/pages_fast.json")

    pages_dict: Dict[str, ManualPage] = file_utils.get_pages_json_dict("json/pages.json")
    pages_fast_dict: Dict[str, ManualPage] = file_utils.get_pages_json_dict("json/pages_fast.json")

    itemlist_template: str = template_utils.create_itemlist_template(lines)

    print(itemlist_template)

else:
    print("Login Failed")
