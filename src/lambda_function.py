# vix指数を取得し、discordに通知するlambda関数

import requests
import json
import os
from datetime import datetime
import pytz

def get_vix_index():
    """VIX指数を取得する関数"""
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        current_price = data['chart']['result'][0]['meta']['regularMarketPrice']
        return round(current_price, 2)
    except Exception as e:
        print(f"VIX指数の取得に失敗しました: {str(e)}")
        return None

def send_discord_notification(vix_value):
    """Discordに通知を送信する関数"""
    webhook_url = os.environ['DISCORD_WEBHOOK_URL']
    jst = pytz.timezone('Asia/Tokyo')
    current_time = datetime.now(jst).strftime('%Y-%m-%d %H:%M:%S %Z')
    
    message = {
        "embeds": [{
            "title": "VIX指数通知",
            "description": f"現在のVIX指数: **{vix_value}**",
            "color": 0x00ff00 if vix_value < 20 else 0xff0000,
            "footer": {"text": f"取得時刻: {current_time}"}
        }]
    }
    
    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
        print("Discord通知の送信に成功しました")
    except Exception as e:
        print(f"Discord通知の送信に失敗しました: {str(e)}")

def lambda_handler(event, context):
    """AWS Lambda用のハンドラー関数"""
    vix_value = get_vix_index()
    
    if vix_value is not None:
        send_discord_notification(vix_value)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'VIX指数の取得と通知に成功しました',
                'vix_value': vix_value
            })
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'VIX指数の取得に失敗しました'
            })
        }
