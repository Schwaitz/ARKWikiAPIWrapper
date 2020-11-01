from typing import Any, Dict

import config


class Edit:
    """Performs edit actions

    Attributes:
        wiki (ARKWiki): the ARKWiki object
    """

    def __init__(self, wiki):
        """Inits an Edit

        Args:
            wiki (ARKWiki): the ARKWiki object
        """

        self.wiki = wiki

    def append_to_page(self, page: str, text: str, summary: str, nocreate: bool) -> Dict[str, Any]:
        """Appends text to the end of a page

        Args:
            page (str): a page name
            text (str): the text to append
            summary (str): a summary of the changes
            nocreate (bool): whether to create the page if it doesn't exist

        Returns:
            A dict mapping a str (key), to Any (value)
        """

        r_params = {
            "action": "edit",
            "title": page,
            "minor": "true",
            "bot": "true",
            "appendtext": "\n" + text,
            "summary": summary,
            "format": "json",
            "token": self.wiki.get_csrf_token()
        }

        if nocreate:
            r_params["nocreate"] = "true"

        return self.wiki.session.post(config.api_url, data=r_params).json()

    def create_page(self, page: str, text: str, summary: str) -> str:
        """Appends text to the end of a page

        Args:
            page (str): a page name
            text (str): the text to append
            summary (str): a summary of the changes

        Returns:
            A str of either the edit result, or an error code
        """

        r_params = {
            "action": "edit",
            "title": page,
            "bot": "true",
            "createonly": "true",
            "text": text,
            "summary": summary,
            "format": "json",
            "token": self.wiki.get_csrf_token()
        }

        r_json = self.wiki.session.post(config.api_url, data=r_params).json()
        if "edit" in r_json:
            return str(r_json["edit"]["result"])
        elif "error" in r_json:
            return str(r_json["error"]["code"])
