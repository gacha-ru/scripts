#!/usr/bin/env python
# coding: utf8
# pylint: disable-msg=C0103

# botoで情報取得
from rds_boto3 import Rds

# google spreadsheet操作系関数
import spreadsheets

import sys
import ConfigParser
from sys import argv

'''
[main function]
'''
if __name__ == "__main__":

    argvs = sys.argv
    argc = len(argvs)

    if not argc == 3:
        print u'Usage: python %s app_name filter_word' % argv[0]
        quit()

    # app.cfgから読み取る情報の選択
    appname = argvs[1]
    # NameTag検索用文字列
    filter_word = argvs[2]
    region = "ap-northeast-1"

    r = Rds()
    rds_info = r.get_info(r.connection(appname, region), filter_word)

    print rds_info
    elements = len(rds_info[0])
    for count in range(0, len(rds_info)):
        for element in range(1, elements):
            if element != (elements - 1):
                print str(rds_info[count][element]) + '\t',
            else:
                print str(rds_info[count][element])

    # spreadsheet名
    sheet_name = appname + "_cost_" + "2017"
    # worksheet名
    ws_name = "RDS_instances"
    # google spreadsheetへ書き込み
    # 単価用シート
    #spreadsheets.rds_costsheet_update(spreadsheet, "RDS_COST", region)
    # DBデータ用シート
    spreadsheets.update_sheet(sheet_name, ws_name, rds_info)
