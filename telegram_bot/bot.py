import datetime
from aiogram import Bot, Dispatcher, executor, types
from db import add_telegram_user, telegram_user_exist
from config import API_TOKEN


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def send_notification(telegram_id: int, order_num: int, price: float, price_rub: float,
                            delivery_time: datetime.date):
    await bot.send_message(telegram_id, f'Заказ №{order_num} на сумму {price}$ ({price_rub}₽) '
                                        f'прибыл {delivery_time.strftime("%d.%m.%Y")}')


@dp.message_handler(commands=['start', 'help'])
async def check_subscription(message: types.Message):
    telegram_id = message.chat.id
    if telegram_user_exist(telegram_id):
        await bot.send_message(telegram_id, 'Я уже записал тебя на рассылку!')
    else:
        add_telegram_user(telegram_id)
        await bot.send_message(telegram_id, "Привет!\nЯ буду присылать тебе прибывшие поставки.")


def start_telegram_bot():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    start_telegram_bot()
