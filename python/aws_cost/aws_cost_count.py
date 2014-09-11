#!/usr/bin/python
# coding: utf8
import sys
import traceback
import ConfigParser
import re
import boto
import datetime

# google spreadsheet操作系関数
import spreadsheets
from usage import usage
# サービスのリストを下記ファイルで管理
from service_list import *

#config read
config = ConfigParser.SafeConfigParser()
config.read('app.cfg')

'''
[aws_cost_count function]
this function culc each app cost.
'''

def aws_cost_count(app_name, aws_access_key, aws_secret_access_key, result):
    #boto接続
    conn = boto.connect_cloudwatch(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_access_key)

    #時間を設定
    #何日前(select_days)の何時間（select_hours）何分前（select_minutes）
    time_now = datetime.datetime.utcnow() - datetime.timedelta(hours=4)
    time_start = time_now - datetime.timedelta(days = result["--day"], hours = result["--hour"], minutes = result["--minutes"])
    time_end = time_start + datetime.timedelta(hours=4)

    service_cost_list = []

    print time_start
    print time_end
    #app_cost
    for aws_service in aws_service_list:
        app_service_result = conn.get_metric_statistics(
            dimensions   = {
                'ServiceName':aws_service,
                'Currency':'USD'},
            metric_name  = 'EstimatedCharges',
            namespace    = 'AWS/Billing',
            statistics = 'Maximum',
            start_time = time_start,
            end_time = time_end,
            period = 60,
            unit = 'None')

        if len(app_service_result) == 0:
            service_cost = 0
        else:
            service_cost = app_service_result[0]['Maximum']

        print aws_service, int(service_cost)
        service_cost_list.append( service_cost )

    # google spreadsheetへ書き込み
    sheet_name = app_name + "_cost"
    spreadsheets.update_sheet( sheet_name, app_name, service_cost_list, time_end )


'''
[main function]
'''
if __name__ == '__main__':
    # usage + option解析
    result = usage()

    # cost_count
    app_name = "test"
    aws_access_key = config.get(app_name, 'AWS_ACCESS_KEY')
    aws_secret_access_key = config.get(app_name, 'AWS_SECRET_ACCESS_KEY')
    aws_cost_count(app_name, aws_access_key, aws_secret_access_key, result)
