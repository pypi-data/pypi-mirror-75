# -*- coding: utf-8 -*-
# @Time : 2019-11-04 09:56 
# @Author : DollarKillerx
# @Description : compression 这里是Zip压缩
import zipfile
import os


def is_zip(dst: str) -> bool:
    """
    当前文件是否是zip
    :param dst: zip文件地址
    :return: true is_zip? false
    """
    return zipfile.is_zipfile(dst)


def unzip(zip_file: str, dst: str):
    """
    解压文件
    :param zip_file: 当前zip地址
    :param dst: 解压到目录
    :return:
    """
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(dst)


def zip_dir(zip_file: str, dst: str):  # zipfilename是压缩包名字，dirname是要打包的目录
    """
    压缩文件夹下所有文件
    :param zip_file: 压缩文件命名
    :param dst: 压缩目标地址
    :return:
    """
    if os.path.isfile(dst):
        with zipfile.ZipFile(zip_file, 'w') as z:
            z.write(dst)
    else:
        with zipfile.ZipFile(zip_file, 'w') as z:
            for root, dirs, files in os.walk(dst):
                for single_file in files:
                    if single_file != zip_file:
                        filepath = os.path.join(root, single_file)
                        z.write(filepath)
