import datetime
import os

from google.cloud import datastore
from zhdate import ZhDate
from dateutil.relativedelta import relativedelta
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/work/Github/family_service_key.json"
"""
Datastore	RDB
Kind	    Table
Entity  	Row
Property	Field
Key	        Primary Key
"""
# クライアントの設定
client = datastore.Client()

# エンティティ
table = client.query(kind="t_family")

# filter：　要素名、演算子、値の順に指定
# result = table.add_filter("id", "=", 1)
# result = table.add_filter("id", "=", 1)
for one_record in table.fetch():
    old_remind_date = one_record['remind_date'].strftime("%Y/%m/%d")
    # 过农历生日
    if one_record["div"] == "lunar":
        print(one_record["id"])
        print(one_record["name"])
        str_birthday = one_record["birthday"].strftime("%Y/%m/%d")
        print(f"阳历：{str_birthday}")
        date_birthday = datetime.datetime.strptime(str_birthday, '%Y/%m/%d')
        # 阳历⇒农历
        zh_date = ZhDate.from_datetime(date_birthday)
        lunar_date = datetime.datetime(
            zh_date.lunar_year, zh_date.lunar_month, zh_date.lunar_day)
        print(f"农历：{lunar_date}")

        date_today = datetime.date.today()

        for one_year in range(100):
            lunar_new_date = lunar_date + relativedelta(years=one_year)
            # 农历⇒阳历
            new_zh_date = ZhDate(lunar_new_date.year,
                                 lunar_new_date.month, lunar_new_date.day)
            solar_new_date = new_zh_date.to_datetime()
            # print(f"solar_new_date:{solar_new_date}")
            remind_date = solar_new_date.date()
            if date_today <= remind_date:
                print(f"one_year:{one_year}")
                print(f"remind_date:{remind_date}")
                one_record['lunar_date'] = lunar_new_date
                one_record['remind_date'] = datetime.datetime(
                    remind_date.year, remind_date.month, remind_date.day)
                one_record['age'] = one_year
                break
        if old_remind_date != one_record['remind_date'].strftime("%Y/%m/%d"):
            print("remind_date update , put it")
            client.put(one_record)
    # 过阳历生日
    else:
        print(one_record["id"])
        print(one_record["name"])
        str_birthday = one_record["birthday"].strftime("%Y/%m/%d")
        print(f"阳历：{str_birthday}")
        date_birthday = datetime.datetime.strptime(str_birthday, '%Y/%m/%d')

        date_today = datetime.date.today()

        for one_year in range(100):
            solar_new_date = date_birthday + relativedelta(years=one_year)
            remind_date = solar_new_date.date()
            if date_today <= remind_date:
                print(f"remind_date:{remind_date}")
                one_record['lunar_date'] = ""
                one_record['remind_date'] = datetime.datetime(
                    remind_date.year, remind_date.month, remind_date.day)
                one_record['age'] = one_year
                break
        if old_remind_date != one_record['remind_date'].strftime("%Y/%m/%d"):
            print(f"old_remind_date:{old_remind_date}")
            print(f"remind_date:{one_record['remind_date']}")
            print("remind_date update , put it")
            client.put(one_record)
