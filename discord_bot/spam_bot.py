import discord
from discord.ext import commands
import time




intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} готов к работе!')

@bot.command(name='spam', help='Отправляет указанный текст заданное количество раз')
async def repeat(ctx, count: int, *, message):
    for _ in range(count):
        await ctx.send(message)
        time.sleep(1)
    time.sleep(5)
    ctx.send('Все ебать. Не зашел - гей')



bot.run('TOKEN')