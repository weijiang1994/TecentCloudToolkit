"""
coding:utf-8
file: __init__.py.py
@time: 2024/6/18 16:32
@desc:
"""
import json

from tencentcloud.dnspod.v20210323 import dnspod_client, models

from src.tencent_cloud import TCLRequest


class TencentCloudDNS(TCLRequest):
    def __init__(self):
        super(TencentCloudDNS, self).__init__()
        self.client = dnspod_client.DnspodClient(self.cred, "", self.client_profile)

    def add_dns_record(
            self,
            domain: str,
            sub_domain: str,
            record_type: str,
            value: str,
            record_line: str = '默认',
            **kwargs
    ):
        """
        添加DNS记录

        :param sub_domain: 子域名记录值
        :param value: DNS记录值
        :param record_line: 记录线路
        :param domain: 域名
        :param record_type: 记录类型
        :return: DNS记录信息
        """
        req = models.CreateRecordRequest()
        params = {
            'Domain': domain,
            'RecordType': record_type,
            'Value': value,
            'RecordLine': record_line,
            'SubDomain': sub_domain
        }
        params.update(kwargs)
        print(params)
        req.from_json_string(json.dumps(params))
        resp = self.client.CreateRecord(req)
        return json.loads(resp.to_json_string())

    def get_dns_record_list(
            self,
            domain
    ):
        """
        获取DNS记录列表

        :param domain: 域名
        :return: DNS记录列表
        """
        return self.http.get({'Domain': domain})
