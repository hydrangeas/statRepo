#!/usr/bin/env python
#
# usage:
"""
"""

import git
import os
import shutil
import sys

def getRepogitry(repogitry_path, repogitry_name):
    # リポジトリパスが空
    if len(repogitry_path)==0:
        print("A repogitry PATH is Empty.")
        return
    if len(repogitry_name)==0:
        print("A repogitry NAME is Empty.")
        return

    save_path = os.path.join('./results/' + repogitry_name)
    try:
        # 存在してたら消す
        if os.path.isdir(save_path):
            shutil.rmtree(save_path)
        # ディレクトリを作る
        os.makedirs(save_path)
        # cloneしてくる
        git.Repo.clone_from(repogitry_path, save_path)
    except:
        import traceback
        traceback.print_exc()


def main():
    # TODO:repogitry_nameはpathから取得できるようにする
    repogitry_path = ""
    repogitry_name = ""

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
    getRepogitry(repogitry_path, repogitry_name)

if __name__ == "__main__":
    ret = main()
