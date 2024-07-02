"""
coding:utf-8
file: __init__.py.py
@time: 2024/6/17 23:37
@desc:
"""
import json

from src.utils import cfg
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ssl.v20191205 import ssl_client, models


class TCLRequest:
    def __init__(
            self,
            endpoint: str = "ssl.tencentcloudapi.com"
    ):
        self.cred = credential.Credential(
            cfg.get('tencent').get('id'),
            cfg.get('tencent').get('secret')
        )
        http_profile = HttpProfile()
        http_profile.endpoint = endpoint
        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        self.client_profile = ClientProfile()
        self.client_profile.http_profile = http_profile
        self.client = ssl_client.SslClient(self.cred, "", self.client_profile)
