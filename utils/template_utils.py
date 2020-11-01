from typing import List


def create_itemlist_template(pages: List[str]) -> str:
    """Create a Template:ItemList from a List[str]

    Args:
        pages (List[str]): a list of page names

    Returns:
        The created Template:ItemList
    """

    itemlist_string = "{{ItemList|noDlcIcon = 1|"
    for p in pages:
        itemlist_string += p + "|"

    itemlist_string = itemlist_string[:-1]
    itemlist_string += "}}"

    return itemlist_string
