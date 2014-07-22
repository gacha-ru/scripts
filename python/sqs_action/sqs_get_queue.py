#!/usr/bin/python
# coding: utf8
import boto
import boto.sqs
from datetime import datetime

import sys
import ConfigParser
from sys import argv

config = ConfigParser.SafeConfigParser()
# ../app.cfgからAWS接続情報を読み取る
config.read('../app.cfg')


# queue_nameからqueueを取得
def sqs_get_queue(aws_access_key, aws_secret_access_key, region, queue_name):
    # boto.ec2への認証
    conn = boto.sqs.connect_to_region(region,
                                      aws_access_key_id=aws_access_key,
                                      aws_secret_access_key=aws_secret_access_key)

    # Create or Get queue
    queue = conn.create_queue(queue_name)
    # Long Polling Setting
    queue.set_attribute('ReceiveMessageWaitTimeSeconds', 20)

    i = 0
    while 1:
        # fetch 10 messages
        msgs = queue.get_messages(10)
        for msg in msgs:
            dt = datetime.today().strftime('%Y/%m/%d %H:%M:%S')
            sys.stderr.write("%s recv%s: %s\n" % (dt, str(i), msg.get_body()))
            i = i + 1

            # delete message
            queue.delete_message(msg)

            # キューのメッセージがcloseであれば終了
            if msg.get_body() == 'close':
                print 'queue close!!'
                quit()

        # Long Pollingが切れたらメッセージ出力してループ
        # ReceiveMessageWaitTimeSeconds間隔
        dt = datetime.today().strftime('%Y/%m/%d %H:%M:%S')
        sys.stderr.write("%s polling...\n" % (dt))

'''
[main function]
'''
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if not argc == 3:
        print u'Usage: python %s app_name filter_word' % argv[0]
        quit()

    # app.cfgから読み取る情報の選択
    app_name = argvs[1]
    # 作成するqueueの名前
    queue_name = argvs[2]

    # region選択(app_nameで判断)
    if app_name in {"usa"}:
        region = "us-west-2"
    else:
        region = "ap-northeast-1"

    # ../app.cfgからキー情報取得
    aws_access_key = config.get(app_name, 'AWS_ACCESS_KEY')
    aws_secret_access_key = config.get(app_name, 'AWS_SECRET_ACCESS_KEY')

    # queue_nameからqueueを取得し続ける
    sqs_get_queue(aws_access_key, aws_secret_access_key, region, queue_name)
