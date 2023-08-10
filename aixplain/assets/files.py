from typing import Union, Text, Optional
from pathlib import Path
from urllib.parse import urlparse

from aixplain.assets.base import BaseAsset
from aixplain.client import AixplainClient, create_retry_session


class File(BaseAsset):
    asset_path = 'file'

    @classmethod
    def upload_to_s3(cls,
                     file_name: Union[Text, Path],
                     content_type: Text = "text/csv",
                     content_encoding: Optional[Text] = None,
                     client: Optional[AixplainClient] = None):
        client = cls._get_client(client)
        payload = client.request('POST',
                                 f'sdk/{cls.asset_path}/upload/temp-url',
                                 json={'contentType': content_type,
                                       'originalName': file_name})
        path = payload['key']
        presigned_url = payload['uploadUrl']

        headers = {'Content-Type': content_type}
        if content_encoding:
            headers['Content-Encoding'] = content_encoding

        content = open(file_name, "rb").read()
        s3_session = create_retry_session()

        s3_response = s3_session.request('PUT',
                                         presigned_url,
                                         headers=headers,
                                         data=content)
        s3_response.raise_for_status()

        bucket_name = urlparse(presigned_url).netloc.split('.')[0]
        return f's3://{bucket_name}/{path}'
