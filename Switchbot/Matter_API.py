import os
import requests
import time
import hashlib
import hmac
import base64
import uuid

# TokenとSecretは適宜設定してください
token = os.getenv('Switchbot_User_Token')
secret = os.getenv('Switchbot_Secret_Token')

# deviceId
deviceId = 'D03234356C31'

# APIリクエストのヘッダー設定
nonce = uuid.uuid4()
t = int(round(time.time() * 1000))
string_to_sign = '{}{}{}'.format(token, t, nonce)

string_to_sign = bytes(string_to_sign, 'utf-8')
secret = bytes(secret, 'utf-8')

sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

# ヘッダー作成
headers = {
    'Authorization': token,
    'Content-Type': 'application/json',
    'charset': 'utf8',
    't': str(t),
    'sign': str(sign, 'utf-8'),
    'nonce': str(nonce)
}

# デバイスのステータス取得
url = f'https://api.switch-bot.com/v1.0/devices/{deviceId}/status'
response = requests.get(url, headers=headers)

# レスポンスの表示
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
