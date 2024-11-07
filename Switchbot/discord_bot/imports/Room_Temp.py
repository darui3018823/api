# ./imports/Room_Temp.py

import discord
import requests
import os

# TokenとSecretは環境変数から取得します
token = os.getenv('Switchbot_User_Token')
secret = os.getenv('Switchbot_Secret_Token')

async def fetch_room_temp_data():
    Deviceid = {}

    # APIリクエストのヘッダー設定
    url = 'https://api.switch-bot.com/v1.0/devices/D03234356C31/status'  # 室温湿度計のデバイスIDを指定

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'charset': 'utf8'
    }

    # APIからのレスポンスを取得
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        device_id = data['body']['deviceId']
        device_type = data['body']['deviceType']
        hub_device_id = data['body']['hubDeviceId']
        temperature = data['body']['temperature']
        humidity = data['body']['humidity']
        status_message = data['message']

        # Embedメッセージを作成
        embed = discord.Embed(
            title="室温湿度計",
            description="現在の室温湿度情報です。",
            color=0x00ff00  # 任意の色に変更可能
        )

        # 室温湿度の情報をEmbedに追加
        embed.add_field(
            name="室温湿度:",
            value=f"室温: {temperature}℃\n湿度: {humidity}%\n",
            inline=False
        )

        # 詳細情報をEmbedに追加
        embed.add_field(
            name="詳細:",
            value=f"Device Type: {device_type}\nHub DeviceID: {hub_device_id}",
            inline=False
        )

        # フッターにステータスメッセージを追加
        embed.set_footer(text=f"Message: {status_message}")

        return embed
    else:
        return None
