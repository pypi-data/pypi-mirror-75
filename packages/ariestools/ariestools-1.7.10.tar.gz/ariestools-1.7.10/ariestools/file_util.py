import os
import re
from typing import List


def write_file(file_path, content, mode='w', encoding='utf-8'):
    """
    写文件. 如果目录存在会自动新建. 默认以覆盖的方式写入.
    :param file_path:
    :param content:
    :param mode:
    :param encoding:
    :return:
    """
    abspath = os.path.abspath(file_path)
    abs_dir = os.path.dirname(abspath)

    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)

    with open(abspath, mode=mode, encoding=encoding) as fp:
        fp.write(content)


def get_all_file_ab_path(path, regex: str = None):
    """
    获取路径下所有文件的绝对路径
    :param path: 文件或文件夹路径
    :param regex 过滤正则
    :return: [文件绝对路径, 文件名]
    """
    file_list = []
    for home, dirs, files in os.walk(path):
        for f in files:
            if regex is not None:
                if re.search(regex, f) is None:
                    continue
            file_list.append(os.path.join(home, f))
    return file_list


if __name__ == '__main__':
    # write_file('./testData/write', '1测试1')
    files_ab_path = get_all_file_ab_path(
        "../build",
        'yaml_util'
    )
    for i in files_ab_path:
        print(i)
