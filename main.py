#coding:utf-8
import logging
import responses as R
import credentials as keys
from rate import ExchangeRate
from generate_random_image import random_image
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import MessageTextIsEmpty
from aiogram.types import InputFile, InlineKeyboardMarkup


API_TOKEN = keys.API_KEY_TEL

# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



#Этот обработчик будет вызываться, когда пользователь отправляет `/start`
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    #обработчик команды /start, когда находится в частном чат
    if message.chat.type == 'private':
        user_sent             = message.chat.username
        options = "/start - запустить бота\n/weather -текущая погода в любом городе\n/rate - Обменный курс\n/photo -случайное изображение животного\n/poll -создать новый опрос"
        await message.reply(f"Hi {user_sent}! Welcome to the bot\n{options}")


    #обработчик команды /start, когда находится в групповом чате
    if message.chat.type == 'supergroup':
        user_sent             = message.chat.username
        options = "/poll -создать новый опрос"
        await message.reply(f"{options}")


#функция будет вызываться, когда пользователь отправляет команду `/photo`
@dp.message_handler(commands=['photo'])
async def photo(message: types.Message):
    if message.chat.type == 'private':
        img = random_image()
        photo = InputFile(img)
        await message.reply_photo(photo=photo)



#Эта функция будет отвечать на вопросы, заданные боту
amount = 0
@dp.message_handler()
async def echo(message: types.Message):
    global amount 

    #управлять ответами, отправленными в приватный чат 
    if message.chat.type == 'private':

        #это обработчик всех ответов в приватном чате для команды /weather 
        text_from_telegram = message.text  
        resp = R.weather_responses(text_from_telegram)
        try:
            await message.answer(resp)
        except MessageTextIsEmpty:
            pass

        #это обработчик всех ответов в приватном чате для команды /rate
        try:
            rate = R.rate_responses(text_from_telegram)
            if isinstance(rate, list) == True:
               amount = rate[0]
               await message.answer("Выберите Валюту", reply_markup=rate[1])
            else:
                try:
                    await message.answer(rate)
                except MessageTextIsEmpty:
                    pass   
        except ValueError:
            pass 

    #это обработчик всех ответов в привате или в групповом чате для команды /poll
    if message.chat.type == 'private' or message.chat.type == 'supergroup':
        text_group = message.text
        poll_resp = R.poll_responses(text_group)
        if isinstance(poll_resp, list) == True:
            question = poll_resp[0]
            options  = poll_resp[1]
            try:
                await bot.send_poll(chat_id=message.chat.id, question=question, options=options)
            except:
                await message.answer("опрос должен иметь как минимум 2 варианта ответа\n отправить /poll для нового вопроса")
        else:
            try:
                await message.answer(poll_resp)
            except MessageTextIsEmpty:
                pass


#этот обработчик обратного вызова для получения значений из предложения кнопки валюты
@dp.callback_query_handler(lambda call:True)
async def callback(call):
    rate =  ExchangeRate()
    data_input = call.data.upper().split('/')
    values = rate.convert(amount, data_input[0], data_input[1])
    await bot.send_message(chat_id=call.message.chat.id, text=f"сумма: {values} \n /rate на новую сумму")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)