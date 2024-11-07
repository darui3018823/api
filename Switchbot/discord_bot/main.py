import discord
from discord.ext import commands
from discord import Embed, app_commands
from imports.PlugMini import fetch_plugmini_data
from imports.Room_Temp import fetch_room_temp_data
from imports.devicelist import get_device_list  # 作成した非同期関数をインポート
import os

# DiscordのBotトークンを取得
discord_token = os.getenv('Switchbot_API_discordbot')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot is Ready.")
    print("Used Switchbot API v1")
    
    await bot.change_presence(activity=discord.CustomActivity("Checking Switchbot API..."))
    
    # スラッシュコマンドを同期
    try:
        synced = await bot.tree.sync()  
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
        
@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000  # bot.latencyは秒単位なので、ミリ秒に変換
    await ctx.send(f'Pong! Latency: {latency:.2f} ms')

@bot.tree.command(name="devicelist", description="daruのTokenから取得できるデバイスリストを送信します。")
async def devicelist(interaction: discord.Interaction):
    try:
        # device_info.pyの非同期関数を呼び出して、デバイス情報を取得
        Deviceid = await get_device_list()

        # Embedの作成
        embed = discord.Embed(
            title="Device List", 
            description="daru's House Switchbot devices", 
            color=0x00ff00 # 色はお好みで変更できます
        )

        # デバイスごとにデバイスタイプをリスト化し、デバイスごとにフィールドを追加
        device_types = {}
        
        # デバイスリストをループしてタイプ別に情報を収集
        for device_id, device_info in Deviceid.items():
            device_name = device_info['name']
            device_type = device_info['type']
            
            if device_type not in device_types:
                device_types[device_type] = []

            device_types[device_type].append({
                'device_id': device_id,
                'device_name': device_name
            })
        
        # デバイスタイプごとにデバイス情報をEmbedに追加
        for device_type, devices in device_types.items():
            embed.add_field(
                name=f"{device_type} (総数: {len(devices)})", 
                value="\n".join([
                    f"デバイス名: {device['device_name']}\nデバイスタイプ: {device_type}" 
                    for device in devices
                ]),
                inline=False
            )
        
        # メッセージを送信
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"Error: {str(e)}")
        
@bot.tree.command(name="room_temp", description="室温湿度計の情報を取得します")
async def room_temp(interaction: discord.Interaction):
    # Room_Temp.pyから取得した非同期関数でEmbedメッセージを生成
    embed = await fetch_room_temp_data()

    if embed:
        # インタラクションを返してEmbedメッセージを送信
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("APIの呼び出しに失敗しました。")
        
@bot.tree.command(name="plugmini", description="Plug Miniデバイスの情報を取得します")
@app_commands.describe(device="Device Last 2txt. e.g, 6A, B6, 6E")
async def plugmini(interaction: discord.Interaction, device: str):
    # deviceパラメータでデバイスIDを指定
    device_mapping = {
        '6A': 'DCDA0CDC436A',
        'B6': 'DCDA0CDC4DB6',
        '6E': 'DCDA0CDA956E'
    }

    # 入力されたデバイスIDがマッピングに存在するかチェック
    if device in device_mapping:
        device_id = device_mapping[device]
        embed = await fetch_plugmini_data(device_id)

        if embed:
            # インタラクションを返してEmbedメッセージを送信
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("APIの呼び出しに失敗しました。")
    else:
        await interaction.response.send_message("無効なデバイスIDが指定されました。")

bot.run(discord_token)
