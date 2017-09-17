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
local_repogitry = './repogitories/'
local_results = './results/'
# TODO:repogitry_nameはpathから取得できるようにする
repogitry_path = ""
repogitry_name = ""

def main():
    if len(sys.argv) > 1:
        i = 1
        # 引数解析
        while i < len(sys.argv):
            s = sys.argv[i]
            i = i + 1
            if s == "--repo":       repogitry_path = sys.argv[i]
            if s == "--name":       repogitry_name = sys.argv[i]
            elif (s == "--help") or (s=="/?"):
                                    return
            else:                   continue
            i = i + 1
    #
    print('Test: repogitry=nginx')
    repogitry_path = "https://github.com/nginx/nginx.git"
    repogitry_name = "nginx"

    getRepogitry(repogitry_path, repogitry_name)

# リポジトリを取得する
def getRepogitry(repogitry_path, repogitry_name):
    # リポジトリパスが空
    if len(repogitry_path)==0:
        print("A repogitry PATH is Empty.")
        return
    if len(repogitry_name)==0:
        print("A repogitry NAME is Empty.")
        return

    local_repogitry = os.path.join(local_repogitry + repogitry_name)
    try:
        # 存在してたら消す
        if os.path.isdir(local_repogitry):
            shutil.rmtree(local_repogitry)
        # ディレクトリを作る
        os.makedirs(local_repogitry)
        # cloneしてくる
        git.Repo.clone_from(repogitry_path, local_repogitry)
    except:
        import traceback
        traceback.print_exc()

#
def stat(repogitry_name):
    local_results = os.path.join(local_results + repogitry_name)
    try:
        # 存在してたら消す
        if os.path.isdir(local_repogitry):
            shutil.rmtree(local_repogitry)
        # ディレクトリを作る
        os.makedirs(local_repogitry)

        # リビジョン
    except:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ret = main()

