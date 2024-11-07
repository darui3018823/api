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

# デバイスリストの取得
url = 'https://api.switch-bot.com/v1.0/devices'
response = requests.get(url, headers=headers)

# レスポンスの表示
if response.status_code == 200:
    data = response.json()
    device_list = data['body']['deviceList']
    
    # 各デバイスの状態を取得
    for device in device_list:
        device_id = device['deviceId']
        device_name = device['deviceName']
        
        print(f"デバイス名: {device_name}, デバイスID: {device_id}")
        
        # プラグデバイスやメーターの状態を取得
        if device['deviceType'] == "Plug Mini (JP)":
            # プラグデバイスの状態を取得する
            status_url = f'https://api.switch-bot.com/v1.0/devices/{device_id}/status'
            status_response = requests.get(status_url, headers=headers)
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                if 'body' in status_data:
                    power_status = status_data['body'].get('power', '不明')
                    wattage = status_data['body'].get('watt', '不明')
                    print(f"電源状態: {power_status}, 消費電力: {wattage}W")
                else:
                    print("ステータス情報の取得に失敗しました")
            else:
                print("ステータス情報の取得に失敗しました")
        
        elif device['deviceType'] == "Meter":
            # 温湿度計の情報を取得する
            meter_url = f'https://api.switch-bot.com/v1.0/devices/{device_id}/status'
            meter_response = requests.get(meter_url, headers=headers)
            
            if meter_response.status_code == 200:
                meter_data = meter_response.json()
                if 'body' in meter_data:
                    temperature = meter_data['body'].get('temperature', '不明')
                    humidity = meter_data['body'].get('humidity', '不明')
                    print(f"温度: {temperature}°C, 湿度: {humidity}%")
                else:
                    print("温湿度情報の取得に失敗しました")
            else:
                print("温湿度情報の取得に失敗しました")
        
        print("------------------------------")
else:
    print(f"デバイス情報の取得に失敗しました: {response.status_code}")
