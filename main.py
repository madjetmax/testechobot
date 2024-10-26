from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
import asyncio

BOT_TOKEN = '7300396047:AAFGX8tkQVz22Mk8MUiPfJwOJucniVaOiIY'


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)


async def main():
    print('bot launched')
    await dp.start_polling(bot, skip_updates=True)
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bot stoped!")