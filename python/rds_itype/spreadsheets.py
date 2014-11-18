#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import gspread
from rds_cost_dict import rds_cost_dict
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
    wks.update_cell(1, 1, "Name")
    wks.update_cell(1, 2, "Instance Type")
    wks.update_cell(1, 3, "Storage Type")
    wks.update_cell(1, 4, "Storage")
    wks.update_cell(1, 5, "IOPS")
    wks.update_cell(1, 6, "hourly")
    wks.update_cell(1, 7, "daily")
    wks.update_cell(1, 8, "monthly")


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


# dataをgoogle spreadsheetへアップ
def update_sheet(spreadsheet, worksheet, rds_name, rds_itype, rds_storage, rds_iops):
    # 日付を入れる
    d = datetime.now()
    d = d.strftime('%Y/%m/%d')

    # シート情報を取得
    wks = open_sheet(spreadsheet, worksheet)
    col_num = len(wks.col_values(1)) + 1

    # 各データをシートへアップ
    for i,name in enumerate(rds_name):
        print rds_name[i]
        if rds_iops[i] == 'None':
            storage_type = "Magnetic"
        else:
            storage_type = "PIOPS"

        column_num = col_num + i

        wks.update_cell(column_num, 1, rds_name[i])
        wks.update_cell(column_num, 2, rds_itype[i])
        wks.update_cell(column_num, 3, storage_type)
        wks.update_cell(column_num, 4, rds_storage[i])
        wks.update_cell(column_num, 5, rds_iops[i])
        wks.update_cell(column_num, 6, '=VLOOKUP(B%(column)s, RDS_COST!A10:B24, 2, FALSE)+IF(C%(column)s="Magnetic", 0.12*D%(column)s/30.5/24 ,\
                0.15*D%(column)s/30.5/24)+IF(E%(column)s="None",\
                0,\
                E%(column)s/1000*120/30.5/24)' % { 'column':str(column_num) } )


# RDSの単価シートを作成
def rds_costsheet_update(spreadsheet, worksheet):
    # シート情報を取得
    wks = open_sheet(spreadsheet, worksheet)
    col_num = len(wks.col_values(1)) + 1

    # 各データをシートへアップ
    #for type,cost in rds_cost_dict.keys(),rds_cost_dict.values():
    for i,type in enumerate(rds_cost_dict.keys()):
        print type
        column_num = col_num + i
        wks.update_cell(column_num, 1, type)
        wks.update_cell(column_num, 2, rds_cost_dict[type])

