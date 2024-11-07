# device_info.py

import uuid
import time
import base64
import hmac
import hashlib
import os
import requests

# TokenとSecretは適宜設定してください

async def get_device_list():
    token = os.getenv('Switchbot_User_Token')
    secret = os.getenv('Switchbot_Secret_Token')

    print(f"User_Token: {token}")
    print(f"Secret_Token: {secret}")
    
    Deviceid = {}

    # APIリクエストのヘッダー設定
    nonce = uuid.uuid4()
    t = int(round(time.time() * 1000))
    string_to_sign = '{}{}{}'.format(token, t, nonce)

    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(secret, 'utf-8')

    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'charset': 'utf8',
        't': str(t),
        'sign': str(sign, 'utf-8'),
        'nonce': str(nonce)
    }

    # デバイスリストの取得
    url = 'https://api.switch-bot.com/v1.0/devices'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        device_list = data['body']['deviceList']
        
        # 各デバイスの状態を取得
        for device in device_list:
            device_id = device['deviceId']
            device_name = device['deviceName']
            device_type = device['deviceType']
            
            # デバイス情報をDeviceid辞書に追加
            Deviceid[device_id] = {
                'name': device_name,
                'type': device_type
            }

    return Deviceid
