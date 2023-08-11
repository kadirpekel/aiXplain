from typing import Dict, Any, Type, Optional, List
from urllib.parse import urlencode, urljoin

from aixplain.env import client as env_client
from aixplain.client import AixplainClient


class BaseAsset:
    client: AixplainClient = env_client

    def __init__(self, obj: Dict[str, Any]):
        self._obj = obj

    def __getattr__(self, key: str) -> Any:
        """Return the value corresponding to the key from the wrapped
        dictionary if found, otherwise raise an AttributeError."""
        if key in self._obj:
            return self._obj[key]
        raise AttributeError(f"Object has no attribute '{key}'")


class GetAssetMixin:

    @classmethod
    def get(cls: Type['BaseAsset'], asset_id: str) -> 'BaseAsset':
        """
        Retrieve an Asset instance by its ID.

        :param asset_id: ID of the asset.
        :return: Instance of the BaseAsset class.
        """
        if cls.asset_path is None:
            raise ValueError(
                "Subclasses of 'BaseAsset' must specify 'asset_path'")
        return cls(cls.client.get(f'sdk/{cls.asset_path}/{asset_id}'))


class ListAssetMixin:

    @classmethod
    def _construct_page_url(cls: Type['BaseAsset'], page_number: int,
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
    def page(cls: Type['BaseAsset'], page_number: int,
             filters: Optional[Dict[str, Any]] = None,
             **kwargs) -> List['BaseAsset']:
        """
        List assets with optional filtering.

        :param page_number: Page number for pagination.
        :param kwargs: Additional filter parameters.
        :return: List of BaseAsset instances.
        """
        url = cls._construct_page_url(page_number, filters=filters)
        payload = cls.client.get(url)
        return [cls(item) for item in payload['items']]

    @classmethod
    def list(cls: Type['BaseAsset'],
             n: int = 1,
             filters: Optional[Dict[str, Any]] = None,
             **kwargs) -> List['BaseAsset']:
        """
        List assets across the first n pages with optional filtering.

        :param n: Optional number of pages to fetch.
        :param kwargs: Additional filter parameters.
        :return: List of BaseAsset instances across n pages.
        """
        assets = []
        for page_number in range(1, n + 1):
            assets += cls.page(page_number, filters=filters, **kwargs)
        return assets
