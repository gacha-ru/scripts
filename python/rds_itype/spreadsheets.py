#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import gspread
import json
import traceback
from rds_cost_dict import rds_tokyo_cost_dict
from rds_cost_dict import rds_oregon_cost_dict
from datetime import datetime
from oauth2client.client import SignedJwtAssertionCredentials

# リダイレクト時のエンコードを"utf8"に
sys.stdout = codecs.getwriter('utf8')(sys.stdout)


class Google:
    def __init__(self):
        jsonfile = "../account.json"

    # googleアカウントにログイン
    # account.jsonからログイン情報を取得する
    def login(self):
        # attempt to log in to your google account
        try:
            base = os.path.dirname(os.path.abspath(__file__))
            json_key = json.load(open(jsonfile))
            scope = ['https://spreadsheets.google.com/feeds']

            credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
            gc = gspread.authorize(credentials)

            print('log in success!!')
            return gc
        except:
            print('log in fail')
            print "--------------------------------------------"
            print traceback.format_exc(sys.exc_info()[2])
            print "--------------------------------------------"
            sys.exit()


    # worksheet情報を取得。指定したworksheetが無い場合は作成。
    def open_sheet(self, gc, spreadsheet, worksheet):
        print spreadsheet, worksheet
        # シートがあれば開く。無ければ新規追加し、フォーマット作成
        try:
            wks = gc.open(spreadsheet).worksheet(worksheet)
        except:
            wks = gc.open(spreadsheet).add_worksheet(worksheet, 50, 50)
            if worksheet == "RDS_COST":
                init_cost_sheet(wks)
            else:
                init_sheet(wks)
        return wks



# sheetのフォーマットを作る
def init_sheet(wks):
    cell_range = 'A1:H1'
    cell_list = wks.range(cell_range)
    cell_list[0].value = 'Name'
    cell_list[1].value = 'Instance Type'
    cell_list[2].value = 'Storage Type'
    cell_list[3].value = 'Storage'
    cell_list[4].value = 'IOPS'
    cell_list[5].value = 'hourly'
    cell_list[6].value = 'daily'
    cell_list[7].value = 'monthly'
    wks.update_cells(cell_list)


# RDS単価用のsheetのフォーマットを作る
def init_cost_sheet(wks):
    wks.update_cell(1, 1, "Instance Type")
    wks.update_cell(1, 2, "$/h")




# google spreadsheetへアップ
def update_sheet(spreadsheet, worksheet, rds_info):
    # 日付を入れる
    d = datetime.now()
    d = d.strftime('%Y/%m/%d')

    # シート情報を取得
    wks = open_sheet(spreadsheet, worksheet)
    col_num = len(wks.col_values(1)) + 1

    cell_len = col_num + len(rds_info)
    cell_range = 'A' + str(col_num) + ':H' + str(cell_len)
    cell_list = []
    cell_list = wks.range(cell_range)

    # 各データを格納
    for i, name in enumerate(rds_info):
        count = i
        print rds_info[count][1]
        column_num = col_num + i

        piops_throughput = rds_info[count][6]
        print piops_throughput
        storage_cost = 'IF(C%(column)s="Magnetic", 0.12*D%(column)s/30.5/24 , IF(C%(column)s="gp2",0.138*D%(column)s/30.5/24,0.15*D%(column)s/30.5/24)+%(throughput_if)s)' % {'column': str(column_num), 'throughput_if': str(piops_throughput)}

        column_num = col_num + i
        cell_list[(i) + (i * 7)].value = rds_info[count][1]
        cell_list[(i + 1) + (i * 7)].value = rds_info[count][2]
        cell_list[(i + 2) + (i * 7)].value = rds_info[count][3]
        cell_list[(i + 3) + (i * 7)].value = rds_info[count][4]
        cell_list[(i + 4) + (i * 7)].value = rds_info[count][5]
        cell_list[(i + 5) + (i * 7)].value = '=VLOOKUP(B%(column)s, RDS_COST!A2:B24, 2, FALSE)+%(storage_if)s' % {'column': str(column_num), 'storage_if': str(storage_cost)}
        cell_list[(i + 6) + (i * 7)].value = '=F' + str(column_num) + '*24'
        cell_list[(i + 7) + (i * 7)].value = '=G' + str(column_num) + '*30.5'

    # 上記で格納した値を一括アップ
    try:
        wks.update_cells(cell_list)
    except Exception as e:
        print 'type:' + str(type(e))
        print 'args:' + str(e.args)
        print 'message:' + str(e.message)
        print 'error:' + str(e)


# RDSの単価シートを作成
def rds_costsheet_update(spreadsheet, worksheet, region):
    # シート情報を取得
    wks = open_sheet(spreadsheet, worksheet)
    col_num = len(wks.col_values(1)) + 1

    # 既にコスト表がある場合は値を上げない
    if col_num > 2:
        return

    rds_cost_dict = []
    print spreadsheet

    if 'us-west-2' in str(region):
        print "Oregon"
        rds_cost_dict = rds_oregon_cost_dict
    else:
        print "Tokyo"
        rds_cost_dict = rds_tokyo_cost_dict

    cell_len = col_num + len(rds_cost_dict)
    cell_range = 'A' + str(col_num) + ':B' + str(cell_len)
    print cell_range
    cell_list = []
    cell_list = wks.range(cell_range)

    # 各データをシートへアップ
    for i, type in enumerate(rds_cost_dict.keys()):
        cell_list[(i) + (i * 1)].value = type
        cell_list[(i + 1) + (i * 1)].value = rds_cost_dict[type]

    try:
        wks.update_cells(cell_list)
    except Exception as e:
        print 'type:' + str(type(e))
        print 'args:' + str(e.args)
        print 'message:' + str(e.message)
        print 'error:' + str(e)
