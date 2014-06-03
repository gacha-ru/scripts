#!/usr/bin/python
# coding: utf8
import sys
import traceback
import ConfigParser
import re
import boto
import datetime
from sys import argv

# google spreadsheet操作系関数
import spreadsheets
# サービスのリストを下記ファイルで管理
from service_list import *

#config read
config = ConfigParser.SafeConfigParser()
config.read('app.cfg')
'''
[aws_cost_count function]
this function culc each app cost.
'''

def aws_cost_count(
        app_name, aws_access_key, aws_secret_access_key):
    conn = boto.connect_cloudwatch(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_access_key)
    #set variable
    now = datetime.datetime.utcnow()

    service_cost_list = []
    #app_cost
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

    # google spreadsheetへ書き込み
    sheet_name = app_name + "_cost"
    spreadsheets.update_sheet( sheet_name, app_name, service_cost_list )


'''
[main function]
'''
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    print argc
    if not argc == 2:
       print u'Usage: python %s app_name' % argv[0]
       quit()

    # Set Application Name
    app_name = argvs[1]

    #cost_count
    print app_name
    aws_access_key = config.get(app_name, 'AWS_ACCESS_KEY')
    aws_secret_access_key = config.get(app_name, 'AWS_SECRET_ACCESS_KEY')
    aws_cost_count(
        app_name, aws_access_key, aws_secret_access_key)
