"""
!/usr/bin/env python
# -*- coding: utf-8 -*-
@Time    : 2023/6/8 16:57
@Author  : 派大星
@Site    : 
@File    : util.py
@Software: PyCharm
@desc:
"""
import os
import shutil
import subprocess
import requests
import configparser


ROOT_FILE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_config(section, option):
    """获取配置文件"""
    config = configparser.ConfigParser()
    config.read(os.path.join(ROOT_FILE_DIR, "config.ini"), encoding="utf-8")
    _value = config.get(section, option)
    return _value


def git_download(root_path):
    """从git上下载项目"""
    # 设置访问令牌和用户名
    GITHUB_ACCESS_TOKEN = get_config('access_token', 'GITHUB_ACCESS_TOKEN')
    GITEE_ACCESS_TOKEN = get_config('access_token', 'GITEE_ACCESS_TOKEN')
    USERNAME = get_config('username', 'USERNAME')  # 目标用户用户名
    for username in USERNAME:
        print(f"在gitee上查找用户{username}的项目...")
        # 发送获取仓库列表的 API 请求
        url = f"https://gitee.com/api/v5/users/{username}/repos"
        params = {"access_token": GITEE_ACCESS_TOKEN, "username": username, "type": "all", "sort": "full_name", "page": 1,
                  "per_page": 100}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # 获取仓库列表
            repos = response.json()
            platform_username = username + "_gitee"
            project_path = os.path.join(root_path, platform_username)
            if os.path.exists(project_path):
                shutil.rmtree(project_path)
            os.makedirs(platform_username, exist_ok=True)  # 创建一个目录用于存放下载的项目
            # 遍历仓库列表，下载每个仓库的内容
            for repo in repos:
                # 使用 git clone 命令来下载仓库
                repo_name = repo["name"]
                repo_url = repo["html_url"]
                repo_path = os.path.join(project_path, repo_name)
                subprocess.run(["git", "clone", repo_url, repo_path])

        print(f"在github上查找用户{username}的项目...")
        github_url = f"https://api.github.com/users/{username}/repos"
        headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
                   "X-GitHub-Api-Version": "2022-11-28"}
        response = requests.get(github_url, headers=headers)
        if response.status_code == 200:
            # 获取仓库列表
            repos = response.json()
            platform_username = username + "_github"
            project_path = os.path.join(root_path, platform_username)
            if os.path.exists(project_path):
                shutil.rmtree(project_path)
            os.makedirs(platform_username, exist_ok=True)  # 创建一个目录用于存放下载的项目
            # 遍历仓库列表，下载每个仓库的内容
            for repo in repos:
                # 使用 git clone 命令来下载仓库
                repo_name = repo["name"]
                repo_url = repo["html_url"]
                repo_path = os.path.join(project_path, repo_name)
                subprocess.run(["git", "clone", repo_url, repo_path])


if __name__ == '__main__':
    ROOT_FILE_DIR = os.path.dirname(__file__)
    git_download(ROOT_FILE_DIR)
