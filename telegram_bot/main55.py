import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command




# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота и всякие переменные
token = 'TOKEN'
bot = Bot(token=token)

repo_link = 'https://poshel_nahuy.com'

# Диспетчер
dp = Dispatcher()

# Хэндлеры на команды
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Hello!')


@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer('Как дела?')
    

@dp.message()
async def send_echo(message: types.Message):
    await message.answer(message.text)



# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())