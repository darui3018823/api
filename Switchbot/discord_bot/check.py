import os

# 環境変数の取得
discord_token = os.getenv('Switchbot_API_discordbot')
user_token = os.getenv('Switchbot_User_Token')
secret_token = os.getenv('Switchbot_Secret_Token')

print(discord_token, user_token, secret_token)  # 確認のために出力（本番では不要）
