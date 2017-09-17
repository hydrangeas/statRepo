#!/usr/bin/env python
#
# usage:
"""
"""

import git
import os
import shutil
import sys

# global variables
repo = None
local_repositry = './repositories/'
local_results = './results/'
# TODO:repositry_nameはpathから取得できるようにする
repositry_path = ""
#repositry_name = ""

def newdir(path):
    # 存在してたら消す
    if os.path.isdir(path):
        shutil.rmtree(path)
    # ディレクトリを作る
    os.makedirs(path)
    return

def main():
    global repositry_path
    if len(sys.argv) > 1:
        i = 1
        # 引数解析
        while i < len(sys.argv):
            s = sys.argv[i]
            i = i + 1
            if s == "--repo":       repositry_path = sys.argv[i]
            if s == "--name":       repositry_name = sys.argv[i]
            elif (s == "--help") or (s=="/?"):
                                    return
            else:                   continue
            i = i + 1
    #
    #30分かかるので注意..
    print('Test: repositry=nginx')
    repositry_path = "https://github.com/nginx/nginx.git"
    repositry_name = "nginx"

    getrepositry(repositry_path, repositry_name)
    stat(repositry_name)

# リポジトリを取得する
def getrepositry(repositry_path, repositry_name):
    # リポジトリパスが空
    if len(repositry_path)==0:
        print("A repositry PATH is Empty.")
        return
    if len(repositry_name)==0:
        print("A repositry NAME is Empty.")
        return

    global local_repositry
    local_repositry = os.path.join(local_repositry, repositry_name)

    global repo
    try:
        if os.path.isdir(local_repositry):
            repo = git.Repo(local_repositry)
            return

        newdir(local_repositry)
        # cloneしてくる
        repo = git.Repo.clone_from(repositry_path, local_repositry, branch='master')
    except:
        import traceback
        traceback.print_exc()

#
def stat(repositry_name):
    global local_results
    local_results = os.path.join(local_results + repositry_name)
    try:
        # 結果用のディレクトリを作成する
        newdir(local_results)

        # リビジョン
        for item in repo.iter_commits('master', max_count=2):
            print('-----')
            print(item.hexsha)
            print(item.stats.files)

            # 一つ前のリビジョンを取得する
            parent = item.parents[0]
            for d in parent.diff(item, create_patch=True):
                print(d.diff.decode('utf-8'))

            hashpath = os.path.join(local_results, item.hexsha)
            newdir(hashpath)
    except:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ret = main()

