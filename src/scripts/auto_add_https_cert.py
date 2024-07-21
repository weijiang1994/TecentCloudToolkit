"""
coding:utf-8
file: auto_add_https_cert.py
@time: 2024/6/22 18:51
@desc: 自动添加HTTPS证书
"""
import argparse
import json
import time
import os

from src.tencent_cloud.ssl import TencentCloudSSL
from src.tencent_cloud.dns import TencentCloudDNS
from src.utils.constants import SSLStatus
from src.utils.file import FileUtil
from src.utils.log import LogUtil
from src.utils import basedir, cfg

tc_ssl = TencentCloudSSL()
logger = None
save_path = None
args = None


def get_current_cert_info(domain):
    result = []
    res = tc_ssl.get_cert_list(domain=domain)
    if res.get('TotalCount') == 0:
        logger.write_log(f"{domain}未添加证书")
        return result
    cert_infos = res.get('Certificates')
    for cert_info in cert_infos:
        remote_domain = cert_info.get('Domain')
        if remote_domain != domain:
            continue
        result.append(dict(
            cert_id=cert_info.get('CertificateId'),
            domain=remote_domain,
            status=cert_info.get('Status'),
            status_name=cert_info.get('StatusName'),
            cert_expire_time=cert_info.get('CertEndTime')
        ))
    return result


def add_cert(domain):
    new_cert_info = tc_ssl.add_free_ssl_cert(auth_type='DNS_AUTO', domain=domain)
    cert_id = new_cert_info.get('CertificateId')
    # 获取证书详情信息
    cert_info = tc_ssl.get_ssl_cert_info(cert_id)
    remote_dv_auth = cert_info.get('DvAuthDetail', {}).get('DvAuths')
    if not remote_dv_auth:
        logger.write_log(f"添加证书失败,错误信息:{cert_info.get('Response', {}).get('Error', {}).get('Message')}")
        return
    remote_dv_auth = remote_dv_auth[0]
    dv_auth_key = remote_dv_auth.get('DvAuthSubDomain')
    dv_auth_value = remote_dv_auth.get('DvAuthValue')
    dv_auth_type = remote_dv_auth.get('DvAuthVerifyType')

    # 添加DNS解析
    dns = TencentCloudDNS()
    dns.add_dns_record(
        domain=args.domain,
        sub_domain=dv_auth_key,
        record_type=dv_auth_type,
        value=dv_auth_value,
        record_line='默认'
    )
    logger.write_log(f"添加证书成功,证书ID:{cert_id},证书状态:{cert_info.get('StatusName')},证书到期时间:{cert_info.get('CertEndTime')}")

    retry_times = 0
    cert_content = {}
    while True:
        try:
            # 验证证书
            verification_content = tc_ssl.complete_cert_verification(cert_id=cert_id)
            logger.write_log(f'验证证书成功: {verification_content}')
            # 下载证书
            cert_content = tc_ssl.download_ssl_cert(cert_id)
            break
        except Exception as e:
            # 签发需要一段时间，这里等待300秒
            logger.write_log(f"下载证书失败,错误信息:{e.args},正在重试...")
            retry_times += 1
            if retry_times > 5:
                logger.write_log("下载证书失败,重试次数过多,请手动下载证书")
                break
            time.sleep(60)

    # 保存证书
    if cert_content:
        download_cert(cert_content, domain, save_path)
    else:
        logger.write_log("下载证书失败,请手动下载证书")


def download_cert(cert_content, domain, save_path):
    save_path = os.path.join(save_path, f'{domain}.zip')
    FileUtil.bs64_to_zip(cert_content.get('Content'), save_path)
    logger.write_log(f"下载证书成功,证书已保存到{save_path}")
    FileUtil.unzip(save_path)


def main(arg, log, path):
    global logger
    logger = log
    global save_path
    save_path = path
    global args
    args = arg
    current_valid_certs = get_current_cert_info(args.target)
    for current_valid_cert in current_valid_certs:
        if current_valid_cert.get('status') == SSLStatus.PASS.value:
            logger.write_log(
                f"{args.target}证书状态正常,证书到期时间:{current_valid_cert.get('cert_expire_time')}"
            )
            if not args.force:
                return
        download_cert(tc_ssl.download_ssl_cert(current_valid_cert.get('cert_id')), args.target, save_path)
        return
    else:
        add_cert(args.target)
