"""
!/usr/bin/env python
# -*- coding: utf-8 -*-
@Time    : 2023/6/7 20:26
@Author  : 派大星
@Site    : 
@File    : core.py
@Software: PyCharm
@desc:
"""
import os
import re


def get_file_path(file_dir):
    """
    获取文件夹下所有文件的路径
    :param file_dir: 文件夹路径
    :return: 文件路径列表
    """
    file_path_list = []
    for root, dirs, files in os.walk(file_dir):
        if 'venv' in dirs:
            dirs.remove('venv')
        if 'pycounter' in dirs:
            dirs.remove('pycounter')
        if '.idea' in dirs:
            dirs.remove('.idea')
        if 'README.md' in files:
            files.remove('README.md')
        # if 'setup.py' in files:
        #     files.remove('setup.py')

        for file in files:
            if not file.endswith('.py') or file == '__init__.py':
                continue
            file_path_list.append(os.path.join(root, file))
    return file_path_list


def get_root_file_path(file_dir):
    """
    获取项目根目录下所有文件夹及文件名（非项目本身文件及文件夹）
    """
    root_file_list = []
    for item in os.listdir(file_dir):
        if item in ['venv', 'pycounter', '.idea', 'README.md', 'setup.py'] or item.startswith('.'):
            continue
        root_file_list.append(item)
    return root_file_list


def count_lines_python(file_path):
    """
    统计python文件的行数
    :param file_path: 文件路径
    :return: 文件行数
    """
    count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # print(line)
            if line in ['\n', '\r\n']:
                continue
            line = line.strip()

            if line.startswith('#') or line.startswith('"""') or line.startswith("'''"):
                continue
            if line.startswith('!/usr/bin/env') or line.startswith('@Time') or line.startswith('@Author') or \
                    line.startswith('@Site') or line.startswith('@File') or line.startswith('@Software') or \
                    line.startswith('@desc'):
                continue
            if not re.search(r'[A-Za-z]+', line):
                continue

            count += 1
    return count


if __name__ == '__main__':
    count_lines_python('/Users/admin/Desktop/PyCodeCounter/xmind2excel_副本/xmind2excel/xmind_to_excel.py')
