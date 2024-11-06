import aiogram, asyncio, logging
import aiogram.filters
from config import *
from aiogram import Bot, Dispatcher, F
from aiogram.types import (Message,
InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery)

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import schedule
import aioschedule
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# from apscheduler.triggers.combining import OrTrigger
# from apscheduler.triggers.cron import CronTrigger

bot = Bot(token=API_KEY)
dp = Dispatcher() 
scheduler = AsyncIOScheduler()

async def send(text):
    await bot.send_message(text=text, chat_id=859261869)


rass_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='+', callback_data='plus'),
     InlineKeyboardButton(text='-', callback_data='minus')
    ],[InlineKeyboardButton(text='start', callback_data='start')]
])

stop_rass_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='stop', callback_data='stop')]
])
class TestState(StatesGroup):
    time = State()


@dp.message(F.text == 'da')
async def start_rozsylka(message: Message, state: FSMContext):
    await message.answer(f'result: 0', reply_markup=rass_keyboard)
    scheduler.add_job(send, 'cron',day_of_week='mon-sat', hour=17, minute=35,second=20, args=('da',), id='jod1')
    
@dp.callback_query()
async def callb(callback: CallbackQuery, state: FSMContext):
    # if callback.data == 'plus':
    #     await state.set_state(TestState.time)
    #     cur_time = await state.get_data()
    #     cur_time = int(cur_time.get('time'))
    #     await state.update_data(time=str(cur_time + 1))
    #     data = await state.get_data()
    #     await callback.message.edit_text(text=f'result {data.get('time')}', reply_markup=rass_keyboard)
    #     await callback.answer('')
    
    
    # if callback.data == 'minus':
        
    #     await state.set_state(TestState.time)
    #     cur_time = await state.get_data()
    #     cur_time = int(cur_time.get('time'))
    #     await state.update_data(time=str(cur_time - 1))
    #     data = await state.get_data()
    #     await callback.message.edit_text(text=f'result {data.get('time')}', reply_markup=rass_keyboard)
    #     await callback.answer('')

    if callback.data == 'plus':
        cur_time = callback.message.text.replace('result: ', '')
        # print(cur_time)
        time = int(cur_time) + 1
        await callback.message.edit_text(text=f'result: {time}', reply_markup=rass_keyboard)
        await callback.answer('')

    if callback.data == 'minus':
        cur_time = callback.message.text.replace('result: ', '')
        # print(cur_time)
        time = int(cur_time) - 1
        await callback.message.edit_text(text=f'result: {time}', reply_markup=rass_keyboard)
        await callback.answer('')
    if callback.data == 'start':
        interval = callback.message.text.replace('result: ', '')
        await callback.message.edit_text(f'started rass with {interval}s interval', reply_markup=stop_rass_keyboard)
        scheduler.add_job(send, 'interval', seconds=int(interval), args=('dadada',), id='job1')

    if callback.data == 'stop':
        scheduler.remove_job('job1')


@dp.message(F.text == 'stop')

async def start_rozsylka(message: Message):
    await message.answer('finished!')
    scheduler.remove_job('job1')


async def main():

    scheduler.start()
    await dp.start_polling(bot)
if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    print('bot launched!')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
    
        print('bot stopped!')
