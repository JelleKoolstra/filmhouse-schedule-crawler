import asyncio
import telegram

from .config import BOT_TOKEN, CHAT_IDS

async def send_document_file(html_file):
    bot = telegram.Bot(token=BOT_TOKEN)
    for chat_id in CHAT_IDS:
        with open(html_file, "rb") as document:
            response = await bot.send_document(chat_id=chat_id, document=document)
            print(f"Telegram API response for chat_id {chat_id}: {response}")

def send_document(html_file):
    asyncio.run(send_document_file(html_file))
