#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
import gspread
import json
from ec2_cost_dict import ec2_cost_dict
from datetime import datetime
from oauth2client.client import SignedJwtAssertionCredentials

# リダイレクト時のエンコードを"utf8"に
sys.stdout = codecs.getwriter('utf8')(sys.stdout)


# googleアカウントにログイン
# G_USER,G_PASSは環境変数で宣言している
def google_login():
    # attempt to log in to your google account
    try:
        json_key = json.load(open('../account.json'))
        scope = ['https://spreadsheets.google.com/feeds']

        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
        gc = gspread.authorize(credentials)

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

    cell_len = col_num + len(data.keys()) - 1
    cell_range = 'A' + str(col_num) + ':E' + str(cell_len)
    cell_list = []
    cell_list = wks.range(cell_range)

    # 各データを格納
    for i, name in enumerate(sorted(data.keys())):
        daily = ec2_cost_dict[data[name]] * 24
        monthly = daily * 30.5

        cell_list[(i) + (i * 4)].value = name
        cell_list[(i + 1) + (i * 4)].value = data[name]
        cell_list[(i + 2) + (i * 4)].value = ec2_cost_dict[data[name]]
        cell_list[(i + 3) + (i * 4)].value = daily
        cell_list[(i + 4) + (i * 4)].value = monthly

    # シートへ一括アップ
    wks.update_cells(cell_list)
