from telethon.sync import TelegramClient
import csv
import os

api_id = api_id 
api_hash = 'api_hash'

session_name = 'my_session'
channel_username = 'kpszsu' 


if not os.path.exists('daily_data'):
    os.makedirs('daily_data')


with TelegramClient(session_name, api_id, api_hash) as client:
    print(f"Останні 20 повідомлень з каналу @{channel_username}...")
    
    messages = client.get_messages(channel_username, limit=20)
    

    file_path = 'daily_data/telegram_news.csv'
    with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Text']) 
        
        for msg in messages:
            if msg.text: 
                writer.writerow([msg.date, msg.text])

print(f"Дані збережено: {file_path}")