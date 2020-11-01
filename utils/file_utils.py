import json
from typing import List, Dict

from actions.ARKWiki import ARKWiki
from classes.ManualPage import ManualPage
from classes.Page import Page


def chunks(l: List[str], n: int) -> List[List[str]]:
    """Divides l into separate lists of length n

    Args:
        l (List[str]): a list of str to separate
        n (int): the length of each separate list

    Returns:
        A List[List[str]] where each List[str] has a length of n,
        except for the last one, which has a length of the remainder
    """

    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_pages_string(pages: List[str]) -> str:
    """Turns a List[str] into a single str separated by '|' characters

    Args:
        pages (List[str]): a list of page names

    Returns:
        A str made up of each page name separated by a '|' character
    """

    pages_string = ""
    for l in pages:
        pages_string += l + "|"
    return pages_string[:-1]


def create_pages_json(pages: List[str], wiki: ARKWiki, verbose: bool = True) -> None:
    """Creates (or overwrites) json/pages.json.

    Populated with data from the page names in 'pages'
    Fetches data by querying each individual page.

    Args:
        pages (List[str]): a list of page names
        wiki (ARKWiki): the ARKWiki object
        verbose (bool): whether to print page names (default: True)

    Returns:
        Nothing
    """

    with open("json/pages.json", "w+") as f:
        f.write("{}")

    for l in pages:
        if verbose:
            print("Adding " + l + " to pages.json")

        p = Page(l, wiki)

        with open("json/pages.json", "r") as f:
            pages_json = json.loads(f.read())
            pages_json[l] = {}
            pages_json[l]["title"] = p.title

            if "Mod:" in l:
                if "/" in l:
                    t_split = l.split("/")
                    pages_json[l]["simple_title"] = t_split[1]
                else:
                    pages_json[l]["simple_title"] = l.replace("Mod:", "")
            else:
                pages_json[l]["simple_title"] = l

            pages_json[l]["info"] = p.info
            pages_json[l]["categories"] = p.categories
            pages_json[l]["content"] = p.content

        with open("json/pages.json", "w") as f:
            f.write(json.dumps(pages_json))


def create_pages_fast_json(pages: List[str], wiki: ARKWiki) -> None:
    """Creates (or overwrites) json/pages_fast.json

    Populated with data from the page names in 'pages'.
    Fetches data much quicker by querying the API in chunks of 50 instead of every individual page.
    Don't use the ManualPage.categories variable when loading from fast_json (doesn't work correctly).

    Args:
        pages (List[str]): a list of page names
        wiki (ARKWiki): the ARKWiki object

    Returns:
        Nothing
    """

    lines_chunks = list(chunks(pages, 50))

    with open("json/pages_fast.json", "w+") as f:
        f.write("{}")

    all_info = {}
    all_categories = {}
    all_content = {}

    for c in lines_chunks:
        ts = get_pages_string(c)

        all_info.update(wiki.query.get_info(ts))
        all_categories.update(wiki.query.get_categories(ts))
        all_content.update(wiki.query.get_content(ts))

    for l in pages:
        with open("json/pages_fast.json", "r") as f:
            pages_json = json.loads(f.read())

            pages_json[l] = {}
            pages_json[l]["title"] = l

            if "Mod:" in l:
                if "/" in l:
                    t_split = l.split("/")
                    pages_json[l]["simple_title"] = t_split[1]
                else:
                    pages_json[l]["simple_title"] = l.replace("Mod:", "")
            else:
                pages_json[l]["simple_title"] = l

            pages_json[l]["info"] = all_info[l]
            pages_json[l]["categories"] = all_categories[l]
            pages_json[l]["content"] = all_content[l]

        with open("json/pages_fast.json", "w") as f:
            f.write(json.dumps(pages_json))


def get_pages_json(json_file: str) -> List[ManualPage]:
    """Create a List[ManualPage] from either pages.json or pages_fast.json

    Args:
        json_file (str): the name of a json file

    Returns:
        A list of ManualPage classes
    """

    with open(json_file, "r") as f:
        pages_json = json.loads(f.read())
        pages = []
        for p in pages_json:
            pages.append(ManualPage(pages_json[p]["title"], pages_json[p]["simple_title"], pages_json[p]["info"], pages_json[p]["categories"], pages_json[p]["content"]))

    return pages


def get_pages_json_dict(json_file: str) -> Dict[str, ManualPage]:
    """Create a dict from either pages.json or pages_fast.json

    The key is the page name
    The value is a ManualPage class

    Args:
        json_file: the name of a json file

    Returns:
        A dict mapping a page name (key), to a ManualPage class (value)
    """

    with open(json_file, "r") as f:
        pages_json = json.loads(f.read())
        pages = {}
        for p in pages_json:
            pages[str(pages_json[p]["title"])] = ManualPage(pages_json[p]["title"], pages_json[p]["simple_title"], pages_json[p]["info"], pages_json[p]["categories"], pages_json[p]["content"])

    return pages
