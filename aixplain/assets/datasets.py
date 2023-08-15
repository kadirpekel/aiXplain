from typing import Dict, Any, Type, Optional, List, Callable

from aixplain.assets import BaseAsset, GetAssetMixin, ListAssetMixin


class Dataset(BaseAsset, GetAssetMixin, ListAssetMixin):

    asset_path = 'datasets'

    @classmethod
    def team_page(cls: Type['BaseAsset'], page_number: int,
                  filters: Optional[Dict[str, Any]] = None,
                  **kwargs) -> List['BaseAsset']:
        path = cls._construct_page_path(page_number=page_number,
                                        filters=filters,
                                        subpaths=['team'],
                                        **kwargs)
        return cls._page(path=path, **kwargs)

    @classmethod
    def team_list(cls: Type['BaseAsset'],
                  n: int = 1,
                  filters: Optional[Dict[str, Any]] = None,
                  page_fn: Optional[Callable[[int, Optional[Dict[str, Any]],
                                             Any],
                                             List['BaseAsset']]] = None,
                  **kwargs) -> List['BaseAsset']:
        return cls.list(n=n, filters=filters, page_fn=cls.team_page, **kwargs)

    def download(self, **kwargs):
        return self._action(action_paths=['download'], **kwargs)
