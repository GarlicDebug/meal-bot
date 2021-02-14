import asyncio

import discord, datetime, threading
from datetime import datetime
# import schedule
from mealFinder import MealFinder
from discord.ext import commands, tasks
from datetime import datetime, timedelta

# Discord API token is stored in unversioned .env file for safety
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("discord-token")

client = discord.Client()


# bot = commands.Bot("!")

# @tasks.loop(minutes=1)
# async def my_task():
#     channel = client.get_channel(809200134533283900)
#     await channel.send(MealFinder.getmeal("dinner", numEntries=10))

# @my_task.before_loop
# async def before_my_task():
#     hour = 17
#     minute = 47
#     await bot.wait_until_ready()
#     now = datetime.now()
#     future = datetime.datetime(now.year, now.month, now.day, hour, minute)
#     if now.hour >= hour and now.minute > minute:
#         future += timedelta(days=1)
#     await asyncio.sleep((future-now).seconds)

# my_task.start()


async def checkTime():
    # This function runs periodically every 1 second
    threading.Timer(1, checkTime).start()

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    day_of_week = datetime.today().weekday()

    if day_of_week < 5:  # weekdays
        if current_time == '06:30:00':
            post_food('breakfast')
        if current_time == '10:30:00':
            post_food('lunch')
        if current_time == '04:30:00':
            post_food('dinner')

    if day_of_week == 5:  # saturday
        if current_time == '12:00:00':
            post_food('lunch')

    if day_of_week == 6:  # sunday
        if current_time == '10:30:00':
            post_food('brunch')
        if current_time == '04:30:00':
            post_food('dinner')
        if current_time == '03:21:00':  # check if matches with the desired time
            await post_food('dinner')
        if current_time == '03:21:30':  # check if matches with the desired time
            await post_food('dinner')

    if current_time == '02:52:00':  # check if matches with the desired time
        print('check 1')

    if current_time == '02:52:30':  # check if matches with the desired time
        print('check 2')


def between_check():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(checkTime())
    loop.close()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # await checkTime()
    _thread = threading.Thread(target=between_check())
    _thread.start()
    # MealFinder.getmeal("lunch", numEntries=10)
    activity = discord.Activity(name='the cafe menu', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)


@client.event
async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$beep'):
        await message.channel.send('boop!')


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    # if message.author.id == self.user.id:
    #     return

    if message.content.startswith('!hello'):
        await message.reply('!hello', mention_author=True)

    if message.content.startswith('!hello2'):
        await message.reply('!hello2', mention_author=True)

    if message.content.startswith('!hello3'):
        await message.reply('!hello3', mention_author=True)

    if message.content.startswith('!pain'):
        await message.reply('!pain', mention_author=True)

    if message.content.startswith('!dinner'):
        channel = client.get_channel(809190205416013876)
        food = MealFinder.getmeal("dinner", numEntries=10)
        await channel.send(food)


async def post_food(meal):
    channel = client.get_channel(809190205416013876)
    food = MealFinder.getmeal(meal, numEntries=10)
    await channel.send(food)


client.run(token)

# async def send_channel():
#     try:
#         await active_channel.send('daily text here')
#     except Exception:
#         active_channel_id = None
#         active_channel = None
#
# async def timer():
#     while True:
#         schedule.run_pending()
#         await asyncio.sleep(3)
#         schedule.every().day.at("21:57").do(await send_channel())
#
# @bot.event
# async def on_ready():
#     print("Logged in as")
#     print(bot.user.name)
#     print(bot.user.id)
#     print("------")
#
#     bot.loop.create_task(timer())
#
#
#
#
# @tasks.loop(hours=24)
# async def send_channel():
#     pass
#
