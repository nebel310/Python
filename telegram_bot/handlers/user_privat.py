from aiogram import types, Router
from aiogram.filters import CommandStart, Command




user_private_router = Router()


@user_private_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer('Бот Expo-v3 запущен.')


@user_private_router.message(Command('help'))
async def cmd_help(message: types.Message):
    GitHub_link = 'https://poshel_nahuy.com'
    await message.answer('Как дела?')


@user_private_router.message(Command('menu'))
async def send_echo(message: types.Message):
    await message.answer('Вот что я могу:')