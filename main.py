from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
import asyncio, uvicorn, sys
from fastapi import FastAPI


BOT_TOKEN = '7300396047:AAFGX8tkQVz22Mk8MUiPfJwOJucniVaOiIY'


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def echo(message: Message):
    await message.answer(message.text)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('bot launched')
    await dp.start_polling(bot, skip_updates=True)
    yield
app = FastAPI(lifespan=lifespan)
