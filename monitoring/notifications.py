import datetime
import asyncio
from db import need_to_notify_orders, get_telegram_users, order_delivery_completed
from telegram_bot import send_notification
from config import DELIVERY_MONITORING_DELAY


async def delivery_monitoring():
    """Рассылает пользователям телеграм уведомление о доставке"""
    today = datetime.date.today()
    orders_rows = need_to_notify_orders(today)
    telegram_users = get_telegram_users()

    for order_row in orders_rows:
        order_num, price, price_rub, delivery_time = order_row
        for user_row in telegram_users:
            telegram_id = user_row[0]
            await send_notification(telegram_id, order_num, price, price_rub, delivery_time)
    order_delivery_completed([order_row[0] for order_row in orders_rows])


async def start_delivery_monitoring():
    while True:
        try:
            await delivery_monitoring()
        except Exception as e:
            print(e)
        await asyncio.sleep(DELIVERY_MONITORING_DELAY)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_delivery_monitoring())
