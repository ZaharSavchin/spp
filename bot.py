import asyncio

from aiogram import Bot, Dispatcher

import handler
from id_token import admin_id, token


async def main():

    bot = Bot(token=token, parse_mode='HTML')
    dp = Dispatcher()

    for id_ in admin_id:
        try:
            await bot.send_message(chat_id=id_, text="бот перезапущен")
        except Exception as err:
            print(err)

    dp.include_router(handler.router)

    await dp.start_polling(bot, polling_timeout=30)


if __name__ == '__main__':
    asyncio.run(main())
