"""
coding:utf-8
file: constants.py
@time: 2024/6/22 21:24
@desc:
"""
import enum


class BaseEnum(enum.Enum):
    @classmethod
    def values(cls):
        return [e.value for e in cls]

    @classmethod
    def names(cls):
        return [e.name for e in cls]

    @classmethod
    def get_name_by_value(cls, value):
        return cls(value).name

    @classmethod
    def get_value_by_name(cls, name):
        return cls[name].value


class SSLStatus(BaseEnum):
    """
    1. AUDITING 审核中
    2. PASS 审核通过
    3. AUDIT_FAILED 审核未通过
    4. EXPIRED 证书过期
    5. ADDED_DNS 已添加DNS解析
    6. CORP_CERT 企业证书
    7. ORDER_CANCELING 订单取消中
    8. ORDER_CANCELED 订单已取消
    9. SUBMITTED_INFO 信息已提交
    10. BANING 吊销中
    11. BANNED 已吊销
    12. REMAKE 重新颁发
    13. WAIT_UPLOAD_BAN_INFO 等待上传吊销确认函
    14. WAIT_SUBMIT_INFO 等待提交资料
    """
    AUDITING = 0
    PASS = 1
    AUDIT_FAILED = 2
    EXPIRED = 3
    ADDED_DNS = 4
    CORP_CERT = 5
    ORDER_CANCELING = 6
    ORDER_CANCELED = 7
    SUBMITTED_INFO = 8
    BANING = 9
    BANNED = 10
    REMAKE = 11
    WAIT_UPLOAD_BAN_INFO = 12
    WAIT_SUBMIT_INFO = 13
