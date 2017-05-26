#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable-msg=C0103
import os
import sys
import json
import traceback
import codecs
from datetime import datetime
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

from rds_cost_dict import rds_tokyo_cost_dict
from rds_cost_dict import rds_oregon_cost_dict


# リダイレクト時のエンコードを"utf8"に
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

# googleアカウントにログイン
# account.jsonからログイン情報を取得する
def login():
    # attempt to log in to your google account
    try:
        base = os.path.dirname(os.path.abspath(__file__))
        jsonfile = base + "/../account.json"
        json_key = json.load(open(jsonfile))
        scope = ['https://spreadsheets.google.com/feeds']

        credentials = SignedJwtAssertionCredentials(
            json_key['client_email'], json_key['private_key'], scope)
        gc = gspread.authorize(credentials)

        print 'log in success!!'
        return gc
    except:
        print 'log in fail'
        print "--------------------------------------------"
        print traceback.format_exc(sys.exc_info()[2])
        print "--------------------------------------------"
        sys.exit()


# worksheet情報を取得。指定したworksheetが無い場合は作成。
def open_sheet(gc, spreadsheet, worksheet):
    print spreadsheet, worksheet
    # シートがあれば開く。無ければ新規追加し、フォーマット作成
    try:
        wks = gc.open(spreadsheet).worksheet(worksheet)
        init_sheet(wks)
    except:
        wks = gc.open(spreadsheet).add_worksheet(worksheet, 50, 50)
        if worksheet == "RDS_COST":
            init_cost_sheet(wks)
        else:
            init_sheet(wks)
    return wks


# sheetのフォーマットを作る
def init_sheet(wks):
    cell_range = 'A1:N1'
    cell_list = wks.range(cell_range)
    format_list = [
        'Name',
        'Engine',
        'Version',
        'Instance Type',
        'Storage Type',
        'Storage',
        'IOPS',
        'AZ',
        'SecurityGroups',
        'BackupWindow',
        'MaintenanceWindow',
        'hourly',
        'daily',
        'monthly'
    ]

    for cnt in range(len(format_list)):
        cell_list[cnt].value = format_list[cnt]

    wks.update_cells(cell_list)


# RDS単価用のsheetのフォーマットを作る
def init_cost_sheet(wks):
    wks.update_cell(1, 1, "Instance Type")
    wks.update_cell(1, 2, "$/h")


# google spreadsheetへアップ
def update_sheet(spreadsheet, worksheet, rds_info):
    # 日付を入れる
    #d = datetime.now()
    #d = d.strftime('%Y/%m/%d')

    # シート情報を取得
    wks = open_sheet(login(), spreadsheet, worksheet)
    #col_num = len(wks.col_values(1)) + 1
    col_num = 2
    cell_len = col_num + len(rds_info)
    cell_range = 'A' + str(col_num) + ':N' + str(cell_len)
    # A~N cellの数
    upcells = 13
    cell_list = []
    cell_list = wks.range(cell_range)

    # 各データを格納
    # for count in enumerate(rds_info):
    for count in range(len(rds_info)):

        column_num = col_num + count

        piops_throughput = 'IF(E%(column)s="PIOPS",F%(column)s*0.12/30.5/24,0)' % {'column': str(column_num)}
        storage_cost = 'IF(E%(column)s="standard", 0.12*F%(column)s/30.5/24 , IF(E%(column)s="gp2",0.138*F%(column)s/30.5/24,0.15*F%(column)s/30.5/24)+%(throughput_if)s)' % {
            'column': str(column_num), 'throughput_if': str(piops_throughput)}

        column_num = col_num + count
        for info_num in range(1, 12):
            cell_list[(count + info_num - 1) + (count * upcells)].value = rds_info[count][info_num]

        cell_list[(count + info_num) + (count * upcells)].value = '=VLOOKUP(D%(column)s, RDS_COST!A2:B24, 2, FALSE)+%(storage_if)s' % {
            'column': str(column_num), 'storage_if': str(storage_cost)}
        cell_list[(count + info_num + 1) + (count * upcells)].value = '=L' + str(column_num) + '*24'
        cell_list[(count + info_num + 2) + (count * upcells)].value = '=M' + str(column_num) + '*30.5'

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
    for i, itype in enumerate(rds_cost_dict.keys()):
        cell_list[(i) + (i * 1)].value = itype
        cell_list[(i + 1) + (i * 1)].value = rds_cost_dict[itype]

    try:
        wks.update_cells(cell_list)
    except Exception as e:
        print 'type:' + str(type(e))
        print 'args:' + str(e.args)
        print 'message:' + str(e.message)
        print 'error:' + str(e)
