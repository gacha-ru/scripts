python
======================

pythonスクリプト置き場
------
### 使用準備 ###
####app.cfg_sampleをコピーしapp.cfgを作成
```
$ cp app.cfg_sample app.cfg
```

app.cfg書き方
```
# なるべくIAMで権限しぼったユーザーを作成し、そのユーザーのキーを使用する

[name] <= 下記キーを使用するための名前
AWS_ACCESS_KEY = アクセスキー
AWS_SECRET_ACCESS_KEY = シークレットアクセスキー
```


####account.jsonを用意する
※ ユーザー名・パスワードでのログインは不可となった為、OAuthログイン
  用意の手順は下記リンク参照
http://gspread.readthedocs.org/en/latest/oauth2.html

ダウンロードしたJSONキーをこのフォルダにaccount.jsonとして置く。
