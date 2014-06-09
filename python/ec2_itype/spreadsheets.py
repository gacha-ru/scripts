#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import gspread
from ec2_cost_dict import ec2_cost_dict
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
    wks.update_cell(1, 3, "hourly")
    wks.update_cell(1, 4, "daily")
    wks.update_cell(1, 5, "monthly")


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
        init_sheet(wks)
    return wks


# dataをgoogle spreadsheetへアップ
def update_sheet(spreadsheet, worksheet, data, search):
    # 日付を入れる
    d = datetime.now()
    d = d.strftime('%Y/%m/%d')

    # シート情報を取得
    wks = open_sheet(spreadsheet, worksheet)
    col_num = len(wks.col_values(1)) + 1

    # 各データをシートへアップ
    for i, name in enumerate(sorted(data.keys())):
        daily = ec2_cost_dict[data[name]] * 24
        monthly = daily * 30.5
        print name, data[name]
        print "daily_cost   : ", daily
        print "monthly_cost : ", monthly
        wks.update_cell(col_num + i, 1, name)
        wks.update_cell(col_num + i, 2, data[name])
        wks.update_cell(col_num + i, 3, ec2_cost_dict[data[name]])
        wks.update_cell(col_num + i, 4, daily)
        wks.update_cell(col_num + i, 5, monthly)
