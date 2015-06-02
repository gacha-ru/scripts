ec2_itype
======================

用途
------
起動中のEC2インスタンスのインスタンスタイプから、  
1時間、日、月毎の費用を1台ずつGoogleDriveのspreadsheetに記録する。

### 使用準備 ###
1. pythonディレクトリでapp.cfgを作成する。（pythonディレクトリのREADME参照）

2. Pythonモジュール boto,gspread,oauth2clientをインストール  
    ```
    pip install boto gspread oauth2client
    ```

3. googleユーザー情報をaccount.jsonというファイル名で用意する      
    ※ ユーザー名・パスワードでのログインは不可となった為、OAuthログイン
      用意の手順は下記リンク参照
    http://gspread.readthedocs.org/en/latest/oauth2.html

4. GoogleDriveのspreadsheetでapp.cfgで設定した"[name]_cost"シートを作成する
   例：app.cfgで[aws]の場合"aws_cost"というシートを作成


### 使用方法 ###
    python ec2_itype_main.py [account_name] [search_words]
 
+   `account_name` :
    pythonディレクトリのapp.cfgで設定した"name"
    "name"を複数設定しておくことでアカウントの切り替えができる。
 
+   `search_words` :
    EC2インスタンスの"Name Tag"から探すワード。部分一致
