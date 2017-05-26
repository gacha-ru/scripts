#!/usr/bin/python
# coding: utf8
import boto
import boto.ec2

# google spreadsheet操作系関数
import spreadsheets


def ec2_get_instance_type(app_name, aws_access_key,
                          aws_secret_access_key, region, filter_word):
    # boto.ec2への認証
    conn = boto.ec2.connect_to_region(region, aws_access_key_id=aws_access_key,
                                      aws_secret_access_key=aws_secret_access_key)

    # filter_word * is OK,but [0-9] is NG.
    filter_instance = conn.get_all_instances(
        filters={'tag-key': 'Name', 'tag-value': filter_word})

    ec2_dict = {}
    for reservation in filter_instance:
        for instance in reservation.instances:
            if instance.state == 'running':
                server_name = instance.__dict__['tags']["Name"]
                i_type = instance.instance_type
                print server_name + '\t' + i_type
                ec2_dict[server_name] = i_type

    # spreadsheet名
    spreadsheet = app_name + "_cost_" + "2017"
    # worksheet名
    worksheet = "now_instances"

    # google spreadsheetへ書き込み
    spreadsheets.update_sheet(spreadsheet, worksheet, ec2_dict, filter_word)
