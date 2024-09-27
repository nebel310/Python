import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import asyncio

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

client = commands.Bot(command_prefix='!', help_command=None, intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'Бот {client.user} готов к работе')


@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот присоединился к каналу: {channel}')


@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот присоединился к каналу: {channel}')


@client.command()
async def play(ctx, url: str):
    song_there = os.path.isfile('song.mp3')

    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Старый файл удален')
    except PermissionError:
        print('[log] Не удалось найти файл')

    await ctx.send('Пожалуйста, ожидайте')

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('[log] Загружаю музыку...')
            ydl.download([url])

        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                name = file
                print(f'[log] Переименовываю файл: {file}')
                os.rename(file, 'song.mp3')

        voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print(f'[log] {name}, музыка закончила проигрывание'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        song_name = name.rsplit('-', 2)
        await ctx.send(f'Играет: {song_name[0]}')

        while voice.is_playing():
            await asyncio.sleep(1)
        os.remove('song.mp3')  # Удаление файла песни после воспроизведения

    except Exception as e:
        await ctx.send(f'Произошла ошибка: {str(e)}')


@client.command()
async def skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.stop()
        await ctx.send('Музыка пропущена.')
        os.remove('song.mp3')  # Удаление файла песни
    else:
        await ctx.send('Сейчас ничего не играет.')




client.run('TOKEN')
