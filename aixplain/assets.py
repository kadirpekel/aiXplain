import json
from typing import Dict, Any, Type, Optional, Union, Text

from aixplain import config
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


class Model(Asset):
    asset_path = 'models'

    def run_async(self, data: Union[Text, Dict], name: Text = "model_process",
                  parameters: Dict = {}) -> Dict:

        data = FileFactory.to_link(data)
        if isinstance(data, dict):
            payload = data
        else:
            try:
                payload = json.loads(data)
                if isinstance(payload, dict) is False:
                    if isinstance(payload, int) is True or isinstance(payload, float) is True:
                        payload = str(payload)
                    payload = {"data": payload}
            except Exception as e:
                payload = {"data": data}
        payload.update(parameters)
        payload = json.dumps(payload)

        call_url = f'{config.MODELS_RUN_URL}/{self.id}'
        return self.client.request('POST', call_url, data=payload)
