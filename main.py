import logging
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, Update
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp

from contextlib import asynccontextmanager
# from config import *

BOT_TOKEN = "7420378524:AAF4bu7Zz6KYJVLF5esOmHK-7ID7XRAZBoA"
TUNEL_TOKEN = 'https://hm-bot.onrender.com'

WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
WEBHOOK_URL = f"{TUNEL_TOKEN}{WEBHOOK_PATH}"



bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

async def alarm():
    async with aiohttp.ClientSession() as session:
        await session.get(TUNEL_TOKEN)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    scheduler.add_job(alarm, 'interval', minutes=50, seconds=0, id='job1')
    await bot.set_webhook(
        url=WEBHOOK_URL, 
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
   

    yield
    await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)




@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)


@dp.message()
async def statr(message: Message):
    await message.answer(message.text)






# if __name__ == "__main__":
#     try:
#         uvicorn.run(app, host="0.0.0.0", port=8000)
#     except KeyboardInterrupt:
#         print("stoped!")
