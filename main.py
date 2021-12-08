import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

from dateutil.relativedelta import relativedelta
from google.cloud import datastore
from zhdate import ZhDate

if os.name == 'nt':
    print("on windows")
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
t_family = client.query(kind="t_family")

# エンティティ
t_mail = client.query(kind="t_mail")
for one_row in t_mail.fetch():
    _pass = one_row["pass"]
    _send_address = one_row["send_address"]
    print(f"_send_address:{_send_address}")
    _to_address = one_row["to_address"]
    print(f"_to_address:{_to_address}")
    _cc_address = one_row["cc_address"]
    print(f"_cc_address:{_cc_address}")

vip_names = ["诚诚爷爷", "诚诚奶奶", "诚诚姥姥", "诚诚姥爷"]


# ------------------
# send mail
# ------------------


def send_mail(bodyText):
    sendAddress = _send_address
    password = _pass

    subject = '誕生日通知'
    bodyText = bodyText
    print(f"send mail {bodyText}")
    fromAddress = _send_address
    toAddress = _to_address
    ccAddress = _cc_address

    # SMTPサーバに接続
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.starttls()
    smtpobj.login(sendAddress, password)

    # メール作成
    msg = MIMEText(bodyText)
    msg['Subject'] = subject
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg["Cc"] = ccAddress
    msg['Date'] = formatdate()

    # 作成したメールを送信
    smtpobj.send_message(msg)
    smtpobj.close()


# ------------------
# main program
# ------------------
def hello_pubsub(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
            event (dict):  The dictionary with data specific to this type of
            event. The `data` field contains the PubsubMessage message. The
            `attributes` field will contain custom attributes if there are any.
            context (google.cloud.functions.Context): The Cloud Functions event
            metadata. The `event_id` field contains the Pub/Sub message ID. The
            `timestamp` field contains the publish time.
    """
    # filter：　要素名、演算子、値の順に指定
    # result = table.add_filter("id", "=", 1)
    for one_record in t_family.fetch():
        old_remind_date = one_record['remind_date'].strftime("%Y/%m/%d")
        # old_remind_date = ""  # 強制更新
        vip = False
        for vip_name in vip_names:
            if vip_name in one_record['name']:
                vip = True
                break
        # 过农历生日
        if one_record["div"] == "lunar":
            str_birthday = one_record["birthday"].strftime("%Y/%m/%d")
            date_birthday = datetime.datetime.strptime(
                str_birthday, '%Y/%m/%d')
            # 阳历⇒农历
            zh_date = ZhDate.from_datetime(date_birthday)
            lunar_date = datetime.datetime(
                zh_date.lunar_year, zh_date.lunar_month, zh_date.lunar_day)

            date_today = datetime.date.today()

            for one_year in range(100):
                lunar_new_date = lunar_date + relativedelta(years=one_year)
                # 农历⇒阳历
                new_zh_date = ZhDate(lunar_new_date.year,
                                     lunar_new_date.month, lunar_new_date.day)
                solar_new_date = new_zh_date.to_datetime()
                remind_date = solar_new_date.date()
                if date_today <= remind_date:
                    one_record['lunar_date'] = lunar_new_date
                    one_record['remind_date'] = datetime.datetime(
                        remind_date.year, remind_date.month, remind_date.day)
                    one_record['age'] = one_year
                    one_record['vip'] = vip

                    break
            if old_remind_date != one_record['remind_date'].strftime("%Y/%m/%d"):
                print("remind_date update , put it")
                client.put(one_record)
        # 过阳历生日
        else:
            str_birthday = one_record["birthday"].strftime("%Y/%m/%d")
            date_birthday = datetime.datetime.strptime(
                str_birthday, '%Y/%m/%d')

            date_today = datetime.date.today()

            for one_year in range(100):
                solar_new_date = date_birthday + \
                    relativedelta(years=one_year)
                remind_date = solar_new_date.date()
                if date_today <= remind_date:
                    one_record['lunar_date'] = ""
                    one_record['remind_date'] = datetime.datetime(
                        remind_date.year, remind_date.month, remind_date.day)
                    one_record['age'] = one_year
                    one_record['vip'] = vip
                    break
            if old_remind_date != one_record['remind_date'].strftime("%Y/%m/%d"):
                print("remind_date update , put it")
                client.put(one_record)

        # 今日からremind_dateまで日数
        days = (remind_date - datetime.date.today()).days
        print(f"days:{days}")
        name = one_record["name"]
        age = one_record["age"]
        lunar_date = one_record['lunar_date']
        # vip提前一周通知
        if vip and days <= 7:
            if days > 0:
                send_mail(f"{name}の{age}歳誕生日まで{days}日")
            else:
                send_mail(f"今日は{name}の{age}歳誕生日")
        # not vip提前一天通知
        elif not vip and days == 1:
            send_mail(f"{name}の{age}歳誕生日まで{days}日")
        # not vip当天通知
        elif not vip and days == 0:
            send_mail(f"今日は{name}の{age}歳誕生日")


if __name__ == "__main__":
    hello_pubsub({}, {})
    # pass
