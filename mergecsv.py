#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# usage:
"""
"""

import csv
import os
import os.path
import pandas as pd
import sys

def main():
    load_path1 = ""
    load_path2 = ""
    save_path = "merged.csv"

    if len(sys.argv) > 1:
        # 引数解析
        i = 1
        while i < len(sys.argv):
            s = sys.argv[i]
            i = i + 1
            if s == "--l1":     load_path1 = sys.argv[i]
            elif s == "--l2":   load_path2 = sys.argv[i]
            elif s == "--s":    save_path = sys.argv[i]
            elif (s == "--help") or (s == "/?"):
                                #usage()
                                return
            else:               continue
            i = i + 1
    if not os.path.isfile(load_path1):
        print('{0}が存在しません'.format(load_path1))
        return
    if not os.path.isfile(load_path2):
        print('{0}が存在しません'.format(load_path2))
        return

    # CSVファイル読み込み
    df1 = pd.read_csv(load_path1)
    df2 = pd.read_csv(load_path2)

    # nameが同じならLOFを移送
    for i, cccc in df1.iterrows():
        # 関数名だけ抽出
        ccccFunc = cccc['name'].split('(')[0]
        diffFunc = cccc['name'].split('(')[0]
        if ccccFunc == diffFunc:
            df1.ix[i, 'LOF'] = df2.ix[j, 'LOF']

    df1.to_csv(path_or_buf=save_path, index=False, quoting=csv.QUOTE_ALL)

if __name__ == "__main__":
    ret = main()
