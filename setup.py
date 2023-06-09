"""
!/usr/bin/env python
# -*- coding: utf-8 -*-
@Time    : 2023/6/7 20:26
@Author  : 派大星
@Site    : 
@File    : setup.py
@Software: PyCharm
@desc:
"""
import os
from collections import defaultdict

from pycounter.core import get_file_path, get_root_file_path, count_lines_python
from pycounter.util import git_download


ROOT_FILE_DIR = os.path.dirname(__file__)


def count_code_lines_by_project():
    """统计项目代码行数"""
    root_file_name = get_root_file_path(ROOT_FILE_DIR)
    file_path_list = get_file_path(ROOT_FILE_DIR)
    file_path_list.remove(os.path.join(ROOT_FILE_DIR, 'setup.py'))  # 移除根目录下setup.py文件，其他目录下的setup.py文件需要统计
    root_file_dict = defaultdict(int)

    for root_file in root_file_name:  # 遍历项目根目录下的文件夹及文件
        for file_path in file_path_list:  # 遍历项目下所有文件
            if root_file in file_path:
                root_file_dict[root_file] += count_lines_python(file_path)  # 统计每个项目的代码行数
    # for project, lines in root_file_dict.items():
    #     print('项目***{}***代码行数为：─{}─'.format(project, lines))

    """以下是ChatGPT产物，仅为了输出美观而使用"""
    # 计算输出中最长的项目名称和行数
    max_project_len = max([len(project) for project in root_file_dict.keys()])
    max_lines_len = len(str(max(root_file_dict.values())))

    # 输出表头
    print("┌{:─^{width1}}┬{:─^{width2}}┐".format("", "", width1=max_project_len+2, width2=max_lines_len+7))
    print(" {:^{width1}}    {:^{width2}} ".format("项目", "代码行数", width1=max_project_len-1, width2=max_lines_len))
    print("├{:─^{width1}}┼{:─^{width2}}┤".format("", "", width1=max_project_len+2, width2=max_lines_len+7))

    # 输出每个项目的行数
    for project, lines in root_file_dict.items():
        print("  {:<{width1}}   {:>{width2}}  ".format(project, lines, width1=max_project_len+2, width2=max_lines_len+2))

    # 输出表尾
    print("└{:─^{width1}}┴{:─^{width2}}┘".format("", "", width1=max_project_len+2, width2=max_lines_len+7))


if __name__ == '__main__':
    git_download(ROOT_FILE_DIR)  # 下载项目
    count_code_lines_by_project()
