#!/usr/bin/env python
#-*- coding: utf-8 -*-
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

# ref from http://qiita.com/suin/items/cdef17e447ceeff6e79d
def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)

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
        diffheader = '"LOF","name"\n'

        # 履歴を取得する
        for item in repo.iter_commits('master', max_count=10000):

            # 一つ前が存在しない場合は終了する
            if (len(item.parents) == 0):
                break

            # 一つ前のリビジョンを取得する
            parent = item.parents[0]

            # ハッシュ値を元にディレクトリを作成する
            hashpath = os.path.join(local_results, item.hexsha)
            newdir(hashpath)

            # 一つ前と現在のリビジョンの差分を取得する
            diffcsv = diffheader
            for d in parent.diff(item, create_patch=True, paths='*.c'):
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
                    elif s.find('@@') == 0 and len(s.split('@@ ')) > 2:
                        diffcsv = diffcsv + '"{0}","{1}"\n'.format(changed_line, s.split('@@ ')[2])
                        changed_line = 0

            # TODO: 差分用ファイルを変更できるようにする
            difffile = os.path.join(hashpath, 'diff.csv')
            # ファイル書き込み
            f = open(difffile, 'w')
            f.write(diffcsv)
            f.close()

            # 一つ前のリビジョンに戻す
            repo.git.checkout(parent.hexsha, force=True)

            # CCCC対象ファイルを探す
            cfiles = []
            for file in find_all_files(local_repositry):
                # Cファイルのみ対象とする
                # TODO: ヘッダファイルの解析を検討する
                if file.endswith('.c'):
                    cfiles.append(file)
            # CCCC実行
            ccccdir = os.path.join(hashpath, 'cccc')
            command = 'cccc {0} --outdir={1} >/dev/null 2>&1'
            os.system(command.format(' '.join(cfiles), ccccdir))

            # CCCC結果 XML->CSV
            ccccfile = os.path.join(ccccdir, 'cccc.csv')
            command = 'python3 cccc2csv.py --l {0} --s {1} >/dev/null 2>&1'
            os.system(command.format(ccccdir, ccccfile))

            mergedfile = os.path.join(hashpath, 'merged.csv')
            command = 'python3 {0} --l1 {1} --l2 {2} --s {3} >/dev/null 2>&1'
            os.system(command.format('mergecsv.py', ccccfile, difffile, mergedfile))

            print('{0}..Done'.format(item.hexsha))

        # リビジョンをmasterに戻す
        # master以外は考慮しない
        repo.git.checkout('master', force=True)
    except:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ret = main()

