# ./imports/PlugMini.py

import discord
import requests
import os

# TokenとSecretは環境変数から取得します
token = os.getenv('Switchbot_User_Token')
secret = os.getenv('Switchbot_Secret_Token')

# Plug Miniの情報を取得する非同期関数
async def fetch_plugmini_data(device_id):
    # APIリクエストのヘッダー設定
    url = f'https://api.switch-bot.com/v1.0/devices/{device_id}/status'  # デバイスIDに応じたURL

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
        power_status = data['body'].get('power', '不明')
        wattage = data['body'].get('watt', '不明')
        status_message = data['message']

        # Embedメッセージを作成
        embed = discord.Embed(
            title=f"Plug Mini {device_id}",
            description="現在のPlug Miniの情報です。",
            color=discord.Color.blue()  # 任意の色に変更可能
        )

        # 電源状態と消費電力をEmbedに追加
        embed.add_field(
            name="電源状態:",
            value=f"{power_status}",
            inline=False
        )
        embed.add_field(
            name="消費電力:",
            value=f"{wattage}W",
            inline=False
        )

        # フッターにステータスメッセージを追加
        embed.set_footer(text=f"Message: {status_message}")

        return embed
    else:
        return None
