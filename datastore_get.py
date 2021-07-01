from google.cloud import datastore
import datetime
from zhdate import ZhDate

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/bilif/Downloads/gcpKey.json"

print("処理開始＞＞＞＞")

# クライアントの設定
client = datastore.Client()
dt_now = datetime.datetime.now()


lunar_now = ZhDate.from_datetime(dt_now)  # 阳历→农历
print("現在の旧暦年：", lunar_now.lunar_year)

query = client.query(kind="t_family")
results = list(query.fetch())
if len(results) > 0:
    print(results[0]["id"])
    print(results[0]["name"])
    birthday = results[0]["birthday"].timestamp_pb().ToDatetime()

    lunar_birthday = ZhDate.from_datetime(birthday)  # 从阳历日期转换成农历日期对象
    print("誕生日の旧暦年月日：", str(lunar_birthday.lunar_year) + "年" +
          str(lunar_birthday.lunar_month) + "月" + str(lunar_birthday.lunar_day) + "日")

    remind_date = datetime.datetime(
        lunar_now.lunar_year, lunar_birthday.lunar_month, lunar_birthday.lunar_day)
    print(remind_date)
print("処理終了＞＞＞＞")
