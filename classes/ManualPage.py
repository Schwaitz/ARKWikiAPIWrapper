from typing import Dict, Any, List


class ManualPage:
    """ManualPage class

    Takes in values for all attributes except for exists.

    Attributes:
        title (str): the page name
        simple_title (str): a simplified name for when title is in the Mod: namespace
        info (Dict[Any]): a dict containing {page id (int), page name (str), length (int), exists (bool)}
        exists (bool): a boolean of if the page exists
        categories (List[str]): a list of categories the page belongs to
        content (List[str]): the content of the page split by newlines
    """

    def __init__(self, title: str, simple_title: str, info: Dict[str, Any], categories: List[str], content: List[str]) -> None:
        """Inits a ManualPage

        Args:
            title (str): the page name
            simple_title: a simplified name
            info: a dict of info
            categories: a list of categories
            content: a list of content lines
        """

        self.title = title
        self.simple_title = simple_title
        self.info = info

        if self.info["exists"]:
            self.exists = True
        else:
            self.exists = False

        self.categories = categories
        self.content = content

    def print_all(self) -> None:
        """Prints all attributes of ManualPage"""

        print("title: " + str(self.title))
        print("simple_title: " + str(self.simple_title))
        print("info: " + str(self.info))
        print("exists: " + str(self.exists))
        print("categories: " + str(self.categories))
        print("content: " + str(self.content))

    def __str__(self):
        if self.exists:
            return self.simple_title + " (exists)"
        else:
            return self.simple_title + " (doesn't exist)"
