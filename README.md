# family

## main program
 - main.py
 - run on gcp cloudfunctions
 - py37

## birthday data
 - saved in gcp datastore
 - kind(table): t_family
 - add new data: 
    - birthday(solar)
    - div("solar" or "lunar")
      - "solar": 阳历
      - "lunar": 农历
    - name
  - age,id,lunar_date,remind_date为程序生成

## send mail
 - first google accountで 2 段階認証
   - https://support.google.com/accounts/answer/185833?hl=ja
 - second アプリ パスワードを作成
 - third account, pass save to gcp datastore
 - from_mail: ttml0122@gmail.com
 - to_mail: bilifans@yahoo.co.jp
 - cc_mail: let8607@yahoo.co.jp

## gcp cloudfuncitons
 - 日本時間に変更したいfunctionの編集画面に行き、下記指定して保存すれば完了
   - 名前：TZ
   - 値：Asia/Tokyo

