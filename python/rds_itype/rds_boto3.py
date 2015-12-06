#!/usr/bin/python
# coding: utf-8

import boto3
from boto3.session import Session
import traceback
import sys

# google spreadsheet操作系関数
from spreadsheets import Google

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
            #session = Session(aws_access_key_id=aws_access_key,
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
        count = 0

        for count in range(0, len(response['DBInstances'])):
            if response['DBInstances'][count]['DBInstanceIdentifier'].count(filter_arg):
                dbinstance = response['DBInstances'][count]
                status = dbinstance['VpcSecurityGroups']

                sec_group = []
                # セキュリティーグループはリストで
                sgcount = len(dbinstance['VpcSecurityGroups'])
                [sec_group.append(status[sec_count]['VpcSecurityGroupId']) for sec_count in range(0, sgcount)]

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
                    str(iops),
                    str(dbinstance['AllocatedStorage']),
                    str(dbinstance['AvailabilityZone']),
                    str(sec_group[:sgcount])
                    ]
                )

        return rds_info


if __name__ == "__main__":
    app_name = "default"
    region = "ap-northeast-1"
    filter_arg = "rep"

    r = Rds()
    rds_info = r.get_info(r.connection(app_name, region), filter_arg)

    elements = len(rds_info[0])
    for count in range(0, len(rds_info)):
        for element in range(1, elements):
            if element != (elements - 1):
                print str(rds_info[count][element]) + '\t' ,
            else:
                print str(rds_info[count][element])

#            print rds_info[count][1] + '\t' + \
#                rds_info[count][2] + '\t' + \
#                rds_info[count][3] + '\t' + \
#                rds_info[count][4] + '\t' + \
#                rds_info[count][5] + '\t' + \
#                rds_info[count][6] + '\t' + \
#                rds_info[count][7] + '\t' + \
#                rds_info[count][8] + '\t' + \
#                rds_info[count][9]
#

#    g = Google()
#    # spreadsheet名
#    spreadsheet = app_name + "_cost"
#    # worksheet名
#    worksheet = "RDS_instances"
#    # google spreadsheetへ書き込み
#    # 単価用シート
#    spreadsheets.rds_costsheet_update(spreadsheet, "RDS_COST", region)
#    # DBデータ用シート
#    spreadsheets.update_sheet(spreadsheet, worksheet, rds_info)
