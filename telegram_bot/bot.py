from aiogram import Bot, Dispatcher, executor, types
from db import add_telegram_user, telegram_user_exist
from config import API_TOKEN


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def send_notification(user_id: int):
    bot.send_message(user_id, "hey!")


@dp.message_handler(commands=['start', 'help'])
async def check_subscription(message: types.Message):
    telegram_id = message.chat.id
    if telegram_user_exist(telegram_id):
        await bot.send_message("Я уже записал тебя на рассылку!")
    else:
        add_telegram_user(telegram_id)
        await bot.send_message("Привет!\nЯ буду присылать тебе прибывшие поставки.")


def start_telegram_bot():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    start_telegram_bot()
