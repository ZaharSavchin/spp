from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from id_token import admin_id, token, urls
from parser import main_funck
import id_token


router = Router()

bot = Bot(token=token, parse_mode='HTML')


@router.message(CommandStart())
async def process_start_command(message: Message):
    if message.from_user.id in admin_id:
        while True:
            try:
                await message.answer('цикл парсинга запущен')
                await main_funck(urls_=urls, message=message)
            except Exception as err:
                await message.answer('что-то пошло не так')
                print(err)


@router.message(Command(commands='list'))
async def process_help_command(message: Message, urls_=urls):
    print(urls)
    await message.answer('следующие ссылки для парсинга:')
    for url in urls:
        await message.answer('\n\n'.join(url))


@router.message(lambda message: isinstance(message.text, str))
async def get_urls(message: Message):
    global urls
    if message.from_user.id in admin_id:
        urls.clear()
        url_groups = [item.strip() for item in message.text.split(';')]
        for group in url_groups:
            urls_g = [item.strip() for item in group.split(',')]
            urls.append(urls_g)

        # urls = [item.strip() for item in message.text.split(',')]
        await message.answer('Добавлены следующие ссылки для парсинга:')
        for url in urls:
            await message.answer('\n\n'.join(url))




