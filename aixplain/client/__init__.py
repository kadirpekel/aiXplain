from typing import Any, Dict

import requests
from requests.adapters import HTTPAdapter, Retry
from urllib.parse import urljoin


class AixplainClient:
    RETRY_BACKOFF_FACTOR = 0.1
    RETRY_STATUS_FORCELIST = [500, 502, 503, 504]

    def __init__(self, base_url: str,
                 api_key: str = None,
                 team_api_key: str = None,
                 max_retries: int = 5,
                 retry: Retry = None):
        """
        Initialize AixplainClient with authentication and retry configuration.

        :param base_url: The base URL for the API
        :param api_key: The individual API key
        :param team_api_key: The team API key
        :param max_retries: The maximum number of retries for a request
        :param retry: Custom Retry configuration
        """
        self.base_url = base_url
        self.team_api_key = team_api_key
        self.api_key = api_key
        self.max_retries = max_retries
        self.retry = retry
        self.reset_session()

        if not (self.api_key or self.team_api_key):
            raise ValueError(
                'Either `api_key` or `team_api_key` should be set')

        default_retry = Retry(total=self.max_retries,
                              backoff_factor=self.RETRY_BACKOFF_FACTOR,
                              status_forcelist=self.RETRY_STATUS_FORCELIST)
        adapter = HTTPAdapter(max_retries=self.retry or default_retry)
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['x-api-key'] = self.team_api_key
        else:
            headers['x-aixplain-key'] = self.api_key
        session = requests.Session()
        session.headers.update(headers)
        session.mount(self.base_url, adapter)
        self.session = session

    def request(self, method: str, path: str, **kwargs: Any) -> Dict:
        """
        Send an HTTP request.

        :param method: HTTP method (e.g. 'GET', 'POST')
        :param path: URL path
        :param kwargs: Additional keyword arguments for the request
        :return: JSON response as a dictionary
        """
        url = urljoin(self.base_url, path)
        response = self.session.request(method=method, url=url, **kwargs)
        response.raise_for_status()  # Handle error where you call request
        return response.json()

    def get(self, path: str, **kwargs: Any) -> Dict:
        """
        Send an HTTP GET request.

        :param path: URL path
        :param kwargs: Additional keyword arguments for the request
        :return: JSON response as a dictionary
        """
        return self.request('GET', path, **kwargs)
