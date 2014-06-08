#!/usr/bin/python
# coding: utf8
import sys
import traceback
import re
import boto
import datetime

# google spreadsheet操作系関数
import spreadsheets
# サービスのリストを下記ファイルで管理
from service_list import *

'''
[aws_cost_count function]
'''

def aws_cost_count( app_name, aws_access_key, aws_secret_access_key ):

    # AWS接続情報
    conn = boto.connect_cloudwatch(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_access_key)

    # 現在時刻取得
    now = datetime.datetime.utcnow()
    service_cost_list = []

    # service_listで定義したサービスのコストを取得し、
    # service_cost_listに入れる
    for aws_service in aws_service_list:
        app_service_result = conn.get_metric_statistics(
            dimensions   = {
                'ServiceName':aws_service,
                'Currency':'USD'},
            metric_name  = 'EstimatedCharges',
            namespace    = 'AWS/Billing',
            statistics = 'Maximum',
            start_time = now-datetime.timedelta(hours=6),
            end_time = now,
            period = 60,
            unit = 'None')

        if len(app_service_result) == 0:
            service_cost = 0
        else:
            service_cost = app_service_result[0]['Maximum']

        print aws_service, int(service_cost)
        service_cost_list.append( service_cost )

    # sheet_nameは"$1"+"_cost"
    sheet_name = app_name + "_cost"

    # google spreadsheetへ書き込み
    spreadsheets.update_sheet( sheet_name, app_name, service_cost_list )
