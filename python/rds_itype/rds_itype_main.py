#!/usr/bin/python
# coding: utf8

import sys
#import ConfigParser
from sys import argv

# botoで情報取得
from rds_boto3 import Rds


'''
[main function]
'''
if __name__ == '__main__':
    app_name = "default"
    region = "ap-northeast-1"
    filter_arg = "staging"

    r = Rds()
    r.get_info(r.connection(app_name, region), filter_arg)
