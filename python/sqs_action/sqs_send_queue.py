#!/usr/bin/python
# coding: utf8
import boto
import boto.sqs
from boto.sqs.message import Message

import sys
import ConfigParser
from sys import argv

config = ConfigParser.SafeConfigParser()
# ../app.cfgからAWS接続情報を読み取る
config.read('../app.cfg')


def sqs_send_queue(aws_access_key, aws_secret_access_key, region, queue_name, queue_message):
    # boto.sqsへの認証
    conn = boto.sqs.connect_to_region(region,
                                      aws_access_key_id=aws_access_key,
                                      aws_secret_access_key=aws_secret_access_key)

    # Create or Get queue
    queue = conn.create_queue(queue_name)

    # Long Polling Setting
    queue.set_attribute('ReceiveMessageWaitTimeSeconds', 20)

    # send
    queue.write(Message(body=queue_message))


'''
[main function]
'''
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if not argc == 4:
        print u'Usage: python %s app_name filter_word' % argv[0]
        quit()

    # app.cfgから読み取る情報の選択
    app_name = argvs[1]
    # 作成するqueueの名前
    queue_name = argvs[2]
    # queueに入れるメッセージ
    queue_message = argvs[3]

    # region選択(app_nameで判断)
    if app_name in {"usa"}:
        region = "us-west-2"
    else:
        region = "ap-northeast-1"

    # ../app.cfgからキー情報取得
    aws_access_key = config.get(app_name, 'AWS_ACCESS_KEY')
    aws_secret_access_key = config.get(app_name, 'AWS_SECRET_ACCESS_KEY')

    # queue_nameへqueue_messageを送信
    sqs_send_queue(aws_access_key, aws_secret_access_key, region, queue_name, queue_message)
