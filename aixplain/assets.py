from typing import Dict, Any, Type, Optional, Union, Text, List
from urllib.parse import urlencode, urljoin

from aixplain.env import client as env_client
from aixplain.client import AixplainClient


class Asset:
    _client: Optional[AixplainClient] = None

    @classmethod
    def set_client(cls, client: AixplainClient) -> None:
        """Set a shared client for all instances of this class."""
        cls._client = client

    @classmethod
    def _get_client(cls,
                    client: Optional[AixplainClient] = None) -> AixplainClient:
        """Return the provided client or the class-level client or env_client.
        """
        return client or cls._client or env_client

    def __init__(self, obj: Dict[str, Any],
                 client: Optional[AixplainClient] = None):
        self._obj = obj
        self.client = self._get_client(client)

    def __getattr__(self, key: str) -> Any:
        """Return the value corresponding to the key from the wrapped
        dictionary if found, otherwise raise an AttributeError."""
        if key in self._obj:
            return self._obj[key]
        raise AttributeError(f"'Asset' object has no attribute '{key}'")

    @classmethod
    def get(cls: Type['Asset'], asset_id: str,
            client: Optional[AixplainClient] = None) -> 'Asset':
        """
        Retrieve an Asset by its ID.

        :param asset_id: ID of the asset.
        :param client: Optional AixplainClient instance.
                       If not provided, the class-level or env_client will be
                       used.
        :return: Instance of the Asset class.
        """
        if cls.asset_path is None:
            raise ValueError("Subclasses of 'Asset' must specify 'asset_path'")
        client = cls._get_client(client)
        return cls(client.get(f'sdk/{cls.asset_path}/{asset_id}'), client)

    @classmethod
    def _construct_page_url(cls: Type['Asset'], page_number: int,
                            filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Construct a URL to list assets.

        :param page_number: Page number for pagination.
        :param filters: Optional dictionary of additional filter parameters.
        :return: Constructed URL.
        """
        base_url = f'sdk/{cls.asset_path}/'
        query_params = {'pageNumber': page_number}

        if filters:
            query_params.update(filters)

        url_query = urlencode(query_params)
        full_url = urljoin(base_url, f'?{url_query}')

        return full_url

    @classmethod
    def page(cls: Type['Asset'], page_number: int,
             filters: Optional[Dict[str, Any]] = None,
             client: Optional[AixplainClient] = None,
             **kwargs) -> List['Asset']:
        """
        List assets with optional filtering.

        :param page_number: Page number for pagination.
        :param client: Optional AixplainClient instance.
                       If not provided, the class-level or env_client will
                       be used.
        :param kwargs: Additional filter parameters.
        :return: List of Asset instances.
        """
        client = cls._get_client(client)
        url = cls._construct_page_url(page_number, filters=filters)
        payload = client.get(url)
        return [cls(item) for item in payload['items']]

    @classmethod
    def list(cls: Type['Asset'], n: int,
             filters: Optional[Dict[str, Any]] = None,
             client: Optional[AixplainClient] = None,
             **kwargs) -> List['Asset']:
        """
        List assets across the first n pages with optional filtering.

        :param n: Number of pages to fetch.
        :param client: Optional AixplainClient instance.
                       If not provided, the class-level or env_client will
                       be used.
        :param kwargs: Additional filter parameters.
        :return: List of Asset instances across n pages.
        """
        assets = []
        for page_number in range(1, n + 1):
            assets += cls.page(page_number, filters=filters, client=client,
                               **kwargs)
        return assets


class Model(Asset):
    asset_path = 'models'

    def run(self, data: Union[Text, Dict], name: Text = "model_process",
            timeout: float = 300, parameters: Dict = {},
            wait_time: float = 0.5) -> Dict:
        """
        Model specific actions should be performed under instance methods
        """
        raise NotImplementedError()

    def run_async(self, data: Union[Text, Dict], name: Text = "model_process",
                  parameters: Dict = {}) -> Dict:
        """
        Model specific actions should be performed under instance methods
        """
        raise NotImplementedError()
