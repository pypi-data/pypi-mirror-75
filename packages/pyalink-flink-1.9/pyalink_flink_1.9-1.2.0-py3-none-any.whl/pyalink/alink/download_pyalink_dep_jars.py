#!/usr/bin/env python

import os
import sys

import requests
from tqdm import tqdm

all_configs = {
    'OSS': {
        'package_name_template': 'shaded_flink_oss_fs_hadoop-{version}-0.2.jar',
        'versions': [
            '1.10.0'
        ],
        'default-version': '1.10.0',
        'url_path': 'https://alink-release.oss-cn-beijing.aliyuncs.com/deps-files/oss/'
    },
    'Hadoop': {
        'package_name_template': 'flink-shaded-hadoop-2-uber-{version}-10.0.jar',
        'versions': [
            '2.4.1', '2.6.5', '2.7.5', '2.8.3'
        ],
        'default-version': '2.8.3',
        'url_path': 'https://alink-release.oss-cn-beijing.aliyuncs.com/deps-files/hadoop/'
    },
    'Hive': {
        'package_name_template': 'hive-deps-{version}.jar',
        'versions': [
            '2-0-v0.1', '2-1-v0.1', '2-2-v0.1', '2-3-v0.1', '3-1-v0.1'
        ],
        'url_path': 'https://alink-release.oss-cn-beijing.aliyuncs.com/deps-files/hive/'
    },
}


def download_file(save_path, url):
    print('Begin to download {} to {}:'.format(url, save_path))
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(save_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")


def query_download_option(name, package_name_template: str, versions, url_path):
    while True:
        ans = input("Download {} dependency jars: [Y]/[N]\n".format(name)).lower()
        if ans in ['y', 'n']:
            break
    if ans == 'n':
        print("Will not download {} dependency jars".format(name))
        return
    option = 0
    if len(versions) > 1:
        options_str = []
        for index, version in enumerate(versions):
            options_str.append('' + str(index + 1) + ') ' + version)
        all_option_str = ', '.join(options_str)
        while True:
            ans = input("Choose from the following versions: {}\n".format(all_option_str))
            try:
                option = int(ans) - 1
            except ValueError:
                continue
            if (option >= 0) and (option < len(versions)):
                break
    package_name = package_name_template.replace("{version}", versions[option])
    return package_name, url_path + package_name


def collect_download_files(use_default=False):
    filelist = []

    for key in all_configs.keys():
        name = key
        config = all_configs[name]
        package_name_template = config['package_name_template']
        versions = config['versions']
        url_path = config['url_path']
        if use_default:
            if 'default-version' in config:
                default_version = config['default-version']
                package_name = package_name_template.replace("{version}", default_version)
                url = url_path + package_name
            else:
                continue
        else:
            ret = query_download_option(name, package_name_template, versions, url_path)
            if ret is None:
                continue
            (package_name, url) = ret
        filelist.append((package_name, url))

    return filelist


def get_alink_lib_path():
    import pyalink
    alink_path = pyalink.__path__[0]
    alink_lib_path = os.path.join(alink_path, 'lib')
    return alink_lib_path


def download_dep_jars(*args):
    alink_lib_path = get_alink_lib_path()

    if not os.access(alink_lib_path, os.R_OK | os.W_OK):
        print("You have no permission in {}. Please run with correct permissions.".format(alink_lib_path))
        return

    print("Jar files will be downloaded into " + alink_lib_path + "\n")
    use_default = False
    if len(args) > 1 and args[1] == '-d':
        use_default = True

    for package_name, url in collect_download_files(use_default):
        save_path = os.path.join(alink_lib_path, package_name)
        download_file(save_path, url)


def main():
    download_dep_jars(*sys.argv)


if __name__ == '__main__':
    main()
