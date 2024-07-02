"""
coding:utf-8
file: file.py
@time: 2024/6/30 23:34
@desc:
"""
import base64
import zipfile


class FileUtil:
    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write_file(file_path, content):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def append_file(file_path, content):
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def read_file_lines(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()

    @staticmethod
    def bs64_to_zip(bs64_str, zip_path):
        """
        base64字符串转zip文件

        :param bs64_str: base64字符串
        :param zip_path: zip文件保存路径
        :return: None
        """
        print(bs64_str)
        zip_str = base64.b64decode(bs64_str, validate=False)
        with open(zip_path, 'wb') as f:
            f.write(zip_str)

    @staticmethod
    def unzip(zip_path):
        """
        解压zip文件

        :param zip_path: zip文件路径
        :return: None
        """
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(zip_path.replace('.zip', ''))
