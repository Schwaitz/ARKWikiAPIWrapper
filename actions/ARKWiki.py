import requests
import config
from actions.Edit import Edit
from actions.Query import Query


class ARKWiki:
    """Logs in and sets up session

    Attributes:
        session (requests.sessions.Session): the requests Session
        login_token (str): a login token
        csrf_token (str): a csrf token
        login_result (str): the login result
        query (Query): the Query object
        edit (Edit): the Edit object
    """

    def __init__(self):
        """Inits an ARKWiki"""

        self.session: requests.sessions.Session = requests.Session()
        self.session.headers.update({"user-agent": config.user_agent})

        self.login_token: str = self.get_login_token()
        self.csrf_token: str = self.get_csrf_token()
        self.login_result: str = self.login()

        self.query: Query = Query(self)
        self.edit: Edit = Edit(self)

    def get_login_token(self) -> str:
        """Fetches a login token from the API

        Returns:
            A login token
        """

        return self.session.get(url=config.api_url, params={"action": "query", "meta": "tokens", "type": "login", "format": "json"}).json()["query"]["tokens"]["logintoken"]

    def get_csrf_token(self) -> str:
        """Fetches a csrf token from the API

        Returns:
            A csrf token
        """
        return self.session.get(url=config.api_url, params={"action": "query", "meta": "tokens", "format": "json"}).json()["query"]["tokens"]["csrftoken"]

    def login(self) -> str:
        """Logs in and get the result

        Returns:
            The login result
        """
        login_params = {"action": "login", "lgname": config.bot_username, "lgpassword": config.bot_password, "lgtoken": self.login_token, "format": "json"}
        return self.session.post(config.api_url, data=login_params).json()["login"]["result"]
