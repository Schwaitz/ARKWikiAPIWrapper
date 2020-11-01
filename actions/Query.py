from typing import Union, Dict, Any, List

import config


class Query:
    """Performs query actions

    Attributes:
        wiki (ARKWiki): the ARKWiki object
    """

    def __init__(self, wiki) -> None:
        """Inits a Query

        Args:
            wiki (ARKWiki): the ARKWiki object
        """

        self.wiki = wiki

    def get_content(self, page: str) -> Union[List[str], Dict[str, List[str]]]:
        """Fetches content for the given page(s)

        Args:
            page (str): the page name(s)

        Returns:
            Either a list of the page content or a dict mapping a page name (key), to a list of the page content (value)
        """

        r_params = {
            "action": "query",
            "prop": "revisions",
            "titles": page,
            "rvslots": "*",
            "rvprop": "content",
            "format": "json",
            "redirects": "true"
        }

        r_json = self.wiki.session.post(config.api_url, data=r_params).json()

        if len(list(r_json["query"]["pages"])) == 1:
            id_key = list(r_json["query"]["pages"])[0]
            page = r_json["query"]["pages"][id_key]

            if id_key != "-1":
                return str(page["revisions"][0]["slots"]["main"]["*"]).split("\n")
            else:
                return ["DNE"]
        elif len(list(r_json["query"]["pages"])) > 1:
            pages = r_json["query"]["pages"]
            return_dict = {}
            for key, page in pages.items():
                if key[0] != "-":
                    return_dict[str(page["title"])] = str(page["revisions"][0]["slots"]["main"]["*"]).split("\n")
                else:
                    return_dict[str(page["title"])] = ["DNE"]

            return return_dict

    def get_info(self, page: str) -> Union[Dict[str, Any], Dict[str, Dict[str, Any]]]:
        """Fetches info for the given page(s)

        Args:
            page (str): the page name(s)

        Returns:
            Either a dict mapping a str (key), to Any (value) or a dict mapping a page name (key), to a dict mapping a str (key), to Any (value)
        """

        r_params = {
            "action": "query",
            "prop": "info",
            "titles": page,
            "format": "json",
            "redirects": "true"
        }

        r_json = self.wiki.session.post(config.api_url, data=r_params).json()

        if len(list(r_json["query"]["pages"])) == 1:
            id_key = list(r_json["query"]["pages"])[0]
            page = r_json["query"]["pages"][id_key]

            if id_key != "-1":
                return {"id": int(page["pageid"]), "title": str(page["title"]), "length": int(page["length"]), "exists": True}
            else:
                return {"id": -1, "title": str(page["title"]), "length": int(-1), "exists": False}

        elif len(list(r_json["query"]["pages"])) > 1:
            pages = r_json["query"]["pages"]
            return_dict = {}
            for key, page in pages.items():
                if key[0] != "-":
                    return_dict[str(page["title"])] = {"id": int(page["pageid"]), "title": str(page["title"]), "length": int(page["length"]), "exists": True}
                else:
                    return_dict[str(page["title"])] = {"id": -1, "title": str(page["title"]), "length": int(-1), "exists": False}

            return return_dict

    def get_text(self, page: str, plain_text: bool, exs_format: str = "wiki") -> str:
        """Fetches text for the given page(s)

        Args:
            page (str): the page name(s)
            plain_text (bool): whether to format as plain text
            exs_format (str): the exsectionformat

        Returns:
            The raw text of the page in wikitable format
        """

        r_params = {
            "action": "query",
            "prop": "extracts",
            "exsectionformat": exs_format,
            "titles": page,
            "format": "json",
            "redirects": "true"
        }

        if plain_text:
            r_params["explaintext"] = "true"

        r_json = self.wiki.session.post(config.api_url, data=r_params).json()
        id_key = list(r_json["query"]["pages"])[0]
        page = r_json["query"]["pages"][id_key]

        if id_key != "-1":
            return str(page["extract"])
        else:
            return "DNE"

    def get_categories(self, page: str) -> Union[List[str], Dict[str, List[str]]]:
        """Fetches categories for the given page(s)

        Args:
            page (str): the page name(s)

        Returns:
            Either a list of categories or a dict mapping a page name (key), to a list of categories (value)
        """

        r_params = {
            "action": "query",
            "prop": "categories",
            "titles": page,
            "format": "json",
            "redirects": "true"
        }

        skip_categories = [
            "Category:Pages using DynamicPageList parser function",
            "Category:Pages with broken file links",
            "Category:Stubs"
        ]

        r_json = self.wiki.session.post(config.api_url, data=r_params).json()

        if len(list(r_json["query"]["pages"])) == 1:
            id_key = list(r_json["query"]["pages"])[0]
            if id_key != "-1":
                page = r_json["query"]["pages"][id_key]

                if "categories" in page:
                    categories = page["categories"]
                    category_list = []

                    for c in categories:
                        if c["title"] not in skip_categories:
                            category_list.append(c["title"])

                    return category_list
                else:
                    return []
            else:
                return []

        elif len(list(r_json["query"]["pages"])) > 1:
            pages = r_json["query"]["pages"]
            return_dict = {}
            for key, page in pages.items():
                if key[0] != "-":
                    if "categories" in page:
                        categories = page["categories"]
                        category_list = []

                        for c in categories:
                            if c["title"] not in skip_categories:
                                category_list.append(c["title"])

                        return_dict[str(page["title"])] = category_list
                    else:
                        return_dict[str(page["title"])] = []
                else:
                    return_dict[str(page["title"])] = []

            return return_dict
