#!/usr/bin/env python
# coding: utf8
# pylint: disable-msg=C0103

# botoで情報取得
from rds_boto3 import Rds

# google spreadsheet操作系関数
import spreadsheets

'''
[main function]
'''
if __name__ == "__main__":
    appname = 'default'
    region = "ap-northeast-1"
    filterarg = ""

    r = Rds()
    rds_info = r.get_info(r.connection(appname, region), filterarg)

    elements = len(rds_info[0])
    for count in range(0, len(rds_info)):
        for element in range(1, elements):
            if element != (elements - 1):
                print str(rds_info[count][element]) + '\t',
            else:
                print str(rds_info[count][element])

    # spreadsheet名
    sheet_name = appname + "_cost_" + "2016"
    # worksheet名
    ws_name = "RDS_instances"
    # google spreadsheetへ書き込み
    # 単価用シート
    #spreadsheets.rds_costsheet_update(spreadsheet, "RDS_COST", region)
    # DBデータ用シート
    spreadsheets.update_sheet(sheet_name, ws_name, rds_info)
