"""
获取npm包信息
"""

import requests
import tarfile
import io
import os

NPM_REGISTRY_URL = 'https://registry.npmjs.org'


def fetch_package_info(package_name):
    """
    获取npm包信息
    :param package_name:
    :return:
    """
    res = requests.get(
        NPM_REGISTRY_URL + '/' + package_name
    )

    if res.status_code == 200:
        return list(res.json()['versions'].keys()).pop()
    return ''


def is_scoped_package_name(package_name):
    return package_name[0] == '@'


def unzip_file(file):
    """
    解压文件
    :param file:
    :return:
    """
    z = tarfile.open(
        fileobj=io.BytesIO(file.content)
    )
    z.extractall()


def show_files(path='./package'):
    """
    整理文件到列表
    :param path:
    :return:
    """
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(
                os.path.join(root[10:], file)
            )
    return file_list


def fetch_package_files(package_name):
    """
    获取所有的文件
    :param package_name:
    :return:
    """
    version = fetch_package_info(package_name)
    if not version:
        return []
    tarballName = package_name
    if is_scoped_package_name(package_name):
        tarballName = package_name.split('/')[1]

    tarballURL = '{}/{}/-/{}-{}.tgz'.format(NPM_REGISTRY_URL, package_name, tarballName, version)
    res = requests.get(tarballURL)
    if res.status_code == 200:
        unzip_file(res)
        return show_files()
    else:
        return []


if __name__ == '__main__':
    fetch_package_files('vue')
