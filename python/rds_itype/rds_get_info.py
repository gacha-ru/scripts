#!/usr/bin/python
# coding: utf8
import boto
import boto.rds

# google spreadsheet操作系関数
import spreadsheets


def rds_get_info(app_name, aws_access_key,
        aws_secret_access_key, region):
    #region connect
    conn = boto.rds.connect_to_region(
        region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key)

    # filter_word * is OK,but [0-9] is NG.
    rds_instance = conn.get_all_dbinstances()

    rds_name = []
    rds_itype = []
    rds_storage = []
    rds_iops = []
    count = 0
    for instance in rds_instance:
        if instance.status == 'available':
            server_name = instance.id
            itype = instance.instance_class
            storage = str(instance.allocated_storage)
            iops = str(instance.iops)
            rds_name.append(server_name)
            rds_itype.append(itype)
            rds_storage.append(storage)
            rds_iops.append(iops)

            print rds_name[count] + '\t' + \
                    rds_itype[count] + '\t' + \
                    rds_storage[count] + '\t' + \
                    rds_iops[count]
            count += 1

    # spreadsheet名
    spreadsheet = app_name + "_cost"
    # worksheet名
    worksheet = "RDS_instances"

    # google spreadsheetへ書き込み
    # 単価用シート
    spreadsheets.rds_costsheet_update(spreadsheet, "RDS_COST")
    # DBデータ用シート
    spreadsheets.update_sheet(spreadsheet, worksheet, rds_name, rds_itype, rds_storage, rds_iops)
