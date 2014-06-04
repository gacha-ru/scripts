#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, time, gspread, sys
import spreadsheets,service_list
import codecs
from datetime import datetime,timedelta
from service_list import *

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
    for i in range(len(aws_service_list)):
        wks.update_cell( 2 + i, 1, aws_service_list[i])
    wks.update_cell( 2 + i + 1, 1, "total")


# worksheet情報を取得。指定したworksheetが無い場合は作成。
def open_sheet( sheet_name, sheet_page ):
    # googleアカウントログイン
    gc = google_login()
    print sheet_name,sheet_page
    # シートがあれば開く。無ければ新規追加し、フォーマット作成
    try:
        wks = gc.open( sheet_name ).worksheet( sheet_page )
    except:
        wks = gc.open( sheet_name ).add_worksheet( sheet_page, 32, 20 )
        init_sheet( wks )
    return wks


# dataをgoogle spreadsheetへアップ
def update_sheet( sheet_name, sheet_page, data ):
    # 日付を入れる
    d = datetime.now() + timedelta(days=-1)
    month = d.month
    d = d.strftime('%Y/%m/%d')
    sheet_page = str(month) + u'月'

    # シート情報を取得
    wks = open_sheet( sheet_name, sheet_page )
    row_num = len(wks.row_values(1))

    # 一行目は一日前の日付
    wks.update_cell( 1, row_num + 1, d)
    
    # 各データをシートへアップ
    i = 0
    cost = 0
    for i,cost in enumerate(data):
        wks.update_cell( 2 + i, row_num + 1, cost)
        print i,cost

    # 最終行は合計値を入れる
    wks.update_cell( 2 + i + 1, row_num + 1, sum(data) )
