rds_itype
======================

用途
------
起動中のRDSインスタンスのインスタンスタイプから、  
1時間、日、月毎の費用を1台ずつGoogleDriveのspreadsheetに記録する。

### 使用準備 ###
1. pythonディレクトリでapp.cfg,account.jsonを用意する。（pythonディレクトリのREADME参照）

2. Pythonモジュール boto,gspread,oauth2clientをインストール
    ```
    pip install boto gspread oauth2client
    ```

3. GoogleDriveのspreadsheetでapp.cfgで設定した"[name]_cost_2016"シートを作成する
   例：app.cfgで[aws]の場合"aws_cost_2016"というシートを作成


### 使用方法 ###
    python rds_itype_main.py [account_name] [region]

+   `account_name` :
    pythonディレクトリのapp.cfgで設定した"name"
    "name"を複数設定しておくことでアカウントの切り替えができる。

+   `region` :
    "ap-northeast-1", "us-west-2"のどちらかしか対応していませんm(__)m
