#!/usr/bin/python
# coding: utf8
import sys
import traceback
import re
import boto
import boto.ec2
import datetime

# google spreadsheet操作系関数
import spreadsheets
# サービスのリストを下記ファイルで管理
from service_list import *

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
    sheet_page = "now_instances"

    # google spreadsheetへ書き込み
    spreadsheets.update_sheet( sheet_name, sheet_page, service_cost_list )


def ec2_get_instance_type( 
        app_name, aws_access_key, aws_secret_access_key,
        region, filter_word):

    # boto.ec2への認証
    conn = boto.ec2.connect_to_region( 
            region,aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_access_key)

    # filter_word * is OK,but [0-9] is NG.
    filter_instance = conn.get_all_instances(
        filters={'tag-key': 'Name', 'tag-value': filter_word})

    ec2_dict = {}
    for reservation in filter_instance:
        for instance in reservation.instances:
            server_name = instance.__dict__['tags']["Name"]
            i_type = instance.instance_type
            print server_name + '\t' + i_type
            ec2_dict[server_name] = i_type

    # sheet_nameは"$1"+"_cost"
    sheet_name = app_name + "_cost"
    sheet_page = "now_instances"

    # google spreadsheetへ書き込み
    spreadsheets.update_sheet( sheet_name, sheet_page, ec2_dict )
