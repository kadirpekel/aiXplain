from typing import Dict, Union, Text
from aixplain.assets.base import BaseAsset


class Model(BaseAsset):
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
