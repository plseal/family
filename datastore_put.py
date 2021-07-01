from google.cloud import datastore
import datetime

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/bilif/Downloads/gcpKey.json"

# クライアントの設定
client = datastore.Client()


# エンティティ put
key = client.key("t_family")
entity = datastore.Entity(key)
entity['name'] = "宋美文"
entity['id'] = 1
entity['birthday'] = datetime.datetime(1960, 12, 23)
client.put(entity)
