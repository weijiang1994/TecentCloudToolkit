"""
coding:utf-8
file: add_cert.py
@time: 2024/7/21 10:39
@desc:
"""
from src.scripts.auto_add_https_cert import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="自动添加HTTPS证书")
    parser.add_argument('-d', '--domain', type=str, required=True, help='主域名')
    parser.add_argument("-t", "--target", type=str, required=True, help="需要添加证书的域名")
    parser.add_argument('-p', '--path', type=str, required=True, help='证书保存路径')
    parser.add_argument('-e', '--expire', type=int, default=7, help='证书剩余有效期(天),默认7天,小于等于该值则自动添加新证书')
    parser.add_argument('-f', '--force', action='store_true', help='是否强制下载证书')

    args = parser.parse_args()
    save_path = args.path

    # 优先使用配置文件中的日志保存路径
    cfg_log_save_path = cfg.get('log').get('save_path')
    if cfg_log_save_path and os.path.exists(cfg_log_save_path):
        log_path = cfg_log_save_path
    else:
        log_path = os.path.join(basedir,  'logs')

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    logger = LogUtil('auto_add_https_cert', os.path.join(log_path, 'auto_add_https_cert.log'))
    main(args, logger, save_path)
