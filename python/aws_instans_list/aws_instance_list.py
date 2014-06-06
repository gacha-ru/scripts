#!/usr/bin/python
# coding: utf8
import sys
import traceback
import ConfigParser
import re
import boto
import datetime
from sys import argv

# botoで情報取得
from get_instance_list import ec2_get_instance_type

# config read
config = ConfigParser.SafeConfigParser()
# ../app.cfgからAWS接続情報を読み取る
config.read('../app.cfg')


'''
[main function]
'''
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if not argc == 3:
       print u'Usage: python %s app_name' % argv[0]
       quit()

    # Set Application Name
    app_name = argvs[1]
    filter_word = "*" + argvs[2] + "*"

    if app_name in { "usa" }:
        region = "us-west-2"
    else :
        region = "ap-northeast-1"

    #instance_listをgoogle spreadsheetへ入れる
    aws_access_key = config.get(app_name, 'AWS_ACCESS_KEY')
    aws_secret_access_key = config.get(app_name, 'AWS_SECRET_ACCESS_KEY')
    ec2_get_instance_type( app_name, aws_access_key, aws_secret_access_key,
            region, filter_word )
