#!/usr/bin/env python
# coding: utf-8
# pylint: disable-msg=C0103

import traceback
import sys
from boto3.session import Session


class Rds:
    """rds infomation class"""

    def __init__(self):
        self.profile = "default"
        self.region = "ap-northeast-1"
        self.filter_arg = ""

    # セッション
    def connection(self, profile, region):
        try:
            # default = ~/.aws/credentials内のキーを参照
            session = Session(profile_name=profile)

            # 個別にキーを設定したい場合はこちら
            # session = Session(aws_access_key_id=aws_access_key,
            #                aws_secret_access_key=aws_secret_access_key,
            #                region_name='ap-northeast-1')
        except:
            print "--------------------------------------------"
            print traceback.format_exc(sys.exc_info()[2])
            print "--------------------------------------------"
            sys.exit()

        return session.client('rds')

    # インスタンス情報取得
    def get_info(self, session, filter_arg):
        rds = session
        response = rds.describe_db_instances()

        rds_info = []

        for count in range(len(response['DBInstances'])):
            if response['DBInstances'][count][
                    'DBInstanceIdentifier'].count(filter_arg):
                dbinstance = response['DBInstances'][count]
                status = dbinstance['VpcSecurityGroups']

                sec_group = []
                # セキュリティーグループはリストで
                sgcount = len(dbinstance['VpcSecurityGroups'])

                [sec_group.append(status[sec_count]['VpcSecurityGroupId'])
                 for sec_count in range(0, sgcount)]

                # IopsはPIOPSにしかない。gp2は計算。その他は"none"。
                if dbinstance['StorageType'] == "io1":
                    iops = dbinstance['Iops']
                elif dbinstance['StorageType'] == "gp2":
                    iops = dbinstance['AllocatedStorage'] * 3
                else:
                    iops = "none"

                rds_info.append(
                    [count,
                     dbinstance['DBInstanceIdentifier'],
                     dbinstance['Engine'],
                     dbinstance['EngineVersion'],
                     dbinstance['DBInstanceClass'],
                     dbinstance['StorageType'],
                     str(dbinstance['AllocatedStorage']),
                     str(iops),
                     str(dbinstance['AvailabilityZone']),
                     str(sec_group[:sgcount])]
                )

        return rds_info
