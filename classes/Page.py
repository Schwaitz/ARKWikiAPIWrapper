from actions.ARKWiki import ARKWiki


class Page:
    """Page class

    Takes in a str (page name) and an ARKWiki object, then
    sets the other attributes by fetching data from the API.

    Attributes:
        title (str): the page name
        simple_title (str): a simplified name for when title is in the Mod: namespace
        info (Dict[Any]): a dict containing {page id (int), page name (str), length (int), exists (bool)}
        wiki (ARKWiki): the ARKWiki object
        exists (bool): a boolean of if the page exists
        categories (List[str]): a list of categories the page belongs to
        content (List[str]): the content of the page split by newlines
    """

    def __init__(self, title: str, wiki: ARKWiki) -> None:
        """Inits a Page

        Args:
            title (str): the page name
            wiki (ARKWiki): the ARKWiki object
        """
        self.title = title

        if "Mod:" in self.title:
            if "/" in self.title:
                t_split = self.title.split("/")
                self.simple_title = t_split[1]
            else:
                self.simple_title = self.title.replace("Mod:", "")
        else:
            self.simple_title = self.title

        self.info = wiki.query.get_info(self.title)

        self.wiki = wiki

        if self.info["exists"]:
            self.exists = True
        else:
            self.exists = False

        self.categories = self.wiki.query.get_categories(self.title)
        self.content = self.wiki.query.get_content(self.title)

    def get_text(self) -> str:
        """Fetches text of the page

        Returns:
            The raw text of the page in wikitable format
        """

        return self.wiki.query.get_text(self.title, True, "wiki")

    def print_all(self) -> None:
        """Prints all attributes of Page"""

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
