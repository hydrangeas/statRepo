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
        diffheader = '"LOF", "name"\n'

        # 履歴を取得する
        for item in repo.iter_commits('master', max_count=2):

            # 一つ前のリビジョンを取得する
            parent = item.parents[0]
            # ハッシュ値を元にディレクトリを作成する
            hashpath = os.path.join(local_results, item.hexsha)
            newdir(hashpath)

            # 一つ前と現在のリビジョンの差分を取得する
            diffcsv = diffheader
            for d in parent.diff(item, create_patch=True):
                # 差分文字列を逆順で処理する
                diffstr = d.diff.decode('utf-8')
                diffstr = diffstr.splitlines()
                diffstr.reverse()

                # '+':変更行数をカウント
                # '@':関数とマッピング
                changed_line = 0
                for s in diffstr:
                    if s.find('+') == 0:
                        changed_line = changed_line + 1
                    elif s.find('@@') == 0:
                        #print("{0},{1}".format(changed_line, s.split('@@ ')[2]))
                        diffcsv = diffcsv + '"{0}","{1}"\n'.format(changed_line, s.split('@@ ')[2])

            # TODO: 差分用ファイルを変更できるようにする
            difffile = os.path.join(hashpath, 'diff.csv')
            # ファイル書き込み
            f = open(difffile, 'w')
            f.write(diffcsv)
            f.close()

    except:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ret = main()

