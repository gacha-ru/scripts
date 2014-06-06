#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, time, gspread, sys
import spreadsheets,ec2_cost_dict
import codecs
from datetime import datetime,timedelta
from ec2_cost_dict import *

# リダイレクト時のエンコードを"utf8"に
sys.stdout = codecs.getwriter('utf8')(sys.stdout)


# googleアカウントにログイン
# G_USER,G_PASSは環境変数で宣言している
def google_login():
    #attempt to log in to your google account
    try:
        gc = gspread.login(os.environ["G_USER"], os.environ["G_PASS"])
        print('log in success!!')
        return gc
    except:
        print('log in fail')
        sys.exit()


# sheetのフォーマットを作る
def init_sheet( wks ):
    wks.update_cell( 1, 1, "Service/Date")
    for i in range(len(ec2_cost_dict)):
        wks.update_cell( 2 + i, 1, ec2_cost_dict[i])


# worksheet情報を取得。指定したworksheetが無い場合は作成。
def open_sheet( sheet_name, sheet_page ):
    # googleアカウントログイン
    gc = google_login()
    print sheet_name,sheet_page
    # シートがあれば開く。無ければ新規追加し、フォーマット作成
    try:
        wks = gc.open( sheet_name ).worksheet( sheet_page )
    except:
        wks = gc.open( sheet_name ).add_worksheet( sheet_page, 50, 50 )
        init_sheet( wks )
    return wks


# dataをgoogle spreadsheetへアップ
def update_sheet( sheet_name, sheet_page, data ):
    # 日付を入れる
    d = datetime.now()
    month = d.month
    d = d.strftime('%Y/%m/%d')

    # シート情報を取得
    wks = open_sheet( sheet_name, sheet_page )
    row_num = len(wks.row_values(1))

    # 各データをシートへアップ
    i = 0
    cost = 0
    #print data.keys()
    for i,name in enumerate(data.keys()):
        #wks.update_cell( 2 + i, row_num + 1, cost)
        print i,name,data[name]
