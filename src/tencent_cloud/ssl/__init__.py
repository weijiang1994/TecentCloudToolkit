"""
coding:utf-8
file: __init__.py.py
@time: 2024/6/17 23:17
@desc:
"""
import json
import enum
from typing import List, Union

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ssl.v20191205 import ssl_client, models

from src.tencent_cloud import TCLRequest
from src.utils import cfg
from src.utils.constants import SSLStatus


class TencentCloudSSL(TCLRequest):
    def __init__(self):
        super().__init__("ssl.tencentcloudapi.com")
        self.client = ssl_client.SslClient(self.cred, "", self.client_profile)

    def add_free_ssl_cert(
            self,
            auth_type,
            domain
    ):
        """
        申请免费证书

        :param auth_type: 认证类型(DNS_AUTO|DNS)
        :param domain: 域名
        :return:
        """
        req = models.ApplyCertificateRequest()
        req.from_json_string(json.dumps(
            {
                'DvAuthMethod': auth_type,
                'DomainName': domain
            }
        ))
        resp = self.client.ApplyCertificate(req)
        return json.loads(resp.to_json_string())

    def get_ssl_cert_info(
            self,
            cert_id
    ):
        """
        获取证书详情信息

        :param cert_id: 证书ID
        :return: 证书详情信息
        """
        req = models.DescribeCertificateRequest()
        req.from_json_string(json.dumps({'CertificateId': cert_id}))
        resp = self.client.DescribeCertificate(req)
        return json.loads(resp.to_json_string())

    def download_ssl_cert(
            self,
            cert_id
    ):
        """
        下载证书

        :param cert_id: 证书ID
        :return: 证书内容
        """
        req = models.DownloadCertificateRequest()
        req.from_json_string(json.dumps({'CertificateId': cert_id}))
        resp = self.client.DownloadCertificate(req)
        return json.loads(resp.to_json_string())

    def get_cert_list(
            self,
            limit: int = 100,
            offset: int = 0,
            domain: str = '',
            status=None
    ):
        """
        获取证书列表,如果不传status则默认获取正常状态的证书

        :param status: 证书状态
        :param limit: 限制数量
        :param offset: 偏移量
        :param domain: 域名
        :return: 证书列表
        """
        if status is None:
            status = [SSLStatus.PASS.value]
        req = models.DescribeCertificatesRequest()
        params = {
            'Offset': offset,
            'Limit': limit,
            'SearchKey': domain,
        }
        # 证书状态(1: 证书正常, 2: 证书过期, 3: 证书吊销, 4: 证书被吊销, 5: 证书审核中, 6: 证书审核不通过)
        if status:
            params['CertificateStatus'] = status

        req.from_json_string(json.dumps(params))
        resp = self.client.DescribeCertificates(req)
        return json.loads(resp.to_json_string())

    def complete_cert_verification(self, cert_id: str):
        """
        完成证书验证

        :param cert_id: 证书id
        :return: 响应内容
        """

        req = models.CompleteCertificateRequest()
        req.from_json_string(json.dumps({
            'CertificateId': cert_id,
        }))
        resp = self.client.CompleteCertificate(req)
        return json.loads(resp.to_json_string())

    def auth_dns_cert(
            self,
            domain: str,
            record_type: str,
            value: str,
            record_line: str = '默认',
            **kwargs
    ):
        """
        添加DNS记录

        :param value: DNS记录值
        :param record_line: 记录线路
        :param domain: 域名
        :param record_type: 记录类型
        :return: DNS记录信息
        """
        return self.http.post({
            'Domain': domain,
            'RecordType': record_type,
            'RecordLine': record_line,
            'Value': value,
            **kwargs
        })