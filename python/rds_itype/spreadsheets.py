#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import gspread
from rds_cost_dict import rds_tokyo_cost_dict
from rds_cost_dict import rds_oregon_cost_dict
from datetime import datetime

# リダイレクト時のエンコードを"utf8"に
sys.stdout = codecs.getwriter('utf8')(sys.stdout)


# googleアカウントにログイン
# G_USER,G_PASSは環境変数で宣言している
def google_login():
    # attempt to log in to your google account
    try:
        gc = gspread.login(os.environ["G_USER"], os.environ["G_PASS"])
        print('log in success!!')
        return gc
    except:
        print('log in fail')
        sys.exit()


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


# worksheet情報を取得。指定したworksheetが無い場合は作成。
def open_sheet(spreadsheet, worksheet):
    # googleアカウントログイン
    gc = google_login()
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


# google spreadsheetへアップ
def update_sheet(spreadsheet, worksheet, rds_name, rds_itype, rds_storage, rds_iops):
    # 日付を入れる
    d = datetime.now()
    d = d.strftime('%Y/%m/%d')

    # シート情報を取得
    wks = open_sheet(spreadsheet, worksheet)
    col_num = len(wks.col_values(1)) + 1

    cell_len = col_num + len(rds_name)
    cell_range = 'A' + str(col_num) + ':H' + str(cell_len)
    cell_list = []
    cell_list = wks.range(cell_range)

    # 各データを格納
    for i, name in enumerate(rds_name):
        print rds_name[i]
        column_num = col_num + i

        if rds_iops[i] == 'None':
            storage_type = "Magnetic"
            rds_iops[i] = '=IF(C%(column)s="gp2", D%(column)s*3, "None")' % {'column': str(column_num)}
        else:
            storage_type = "PIOPS"

        piops_throughput = 'IF(C%(column)s="PIOPS",E%(column)s*0.12/30.5/24,0)' % {'column': str(column_num)}
        storage_cost = 'IF(C%(column)s="Magnetic", 0.12*D%(column)s/30.5/24 , IF(C%(column)s="gp2",0.138*D%(column)s/30.5/24,0.15*D%(column)s/30.5/24)+%(throughput_if)s)' % {'column': str(column_num), 'throughput_if': str(piops_throughput)}

        column_num = col_num + i
        cell_list[(i) + (i * 7)].value = rds_name[i]
        cell_list[(i + 1) + (i * 7)].value = rds_itype[i]
        cell_list[(i + 2) + (i * 7)].value = storage_type
        cell_list[(i + 3) + (i * 7)].value = rds_storage[i]
        cell_list[(i + 4) + (i * 7)].value = rds_iops[i]
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
