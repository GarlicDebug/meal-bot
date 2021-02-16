import os
import asyncio
import datetime
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from mealFinder import MealFinder
from datetime import datetime

# Discord API token is stored in unversioned .env file for safety
load_dotenv()
token = os.environ.get("discord-token")

channelDict = {
    'general': 811076981986557982,
    'testing': 809200134533283900,
    'breakfast': 811076422806011914,
    'brunch': 811076467764756481,
    'lunch': 811076467764756481,
    'dinner': 809190205416013876,
}

client = discord.Client()

bot = commands.Bot("!")


@tasks.loop(seconds=10)
async def clock():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Clock Time =", current_time)


@clock.before_loop
async def before_clock():
    print('Starting debug clock')
    seconds_to_sleep = 10 - (datetime.now().second % 10)
    print(seconds_to_sleep)
    await asyncio.sleep(seconds_to_sleep)


@tasks.loop(minutes=15)
async def timeloop():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Loop Time =", current_time)
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Meal loop time=", current_time)

    day_of_week = datetime.today().weekday()
    print("Today is " + str(day_of_week))

    if day_of_week < 5:  # weekdays
        if current_time == '06:30:00':
            await post_food('breakfast')
        if current_time == '10:30:00':
            await post_food('lunch')
        if current_time == '04:30:00':
            await post_food('dinner')

    if day_of_week == 5:  # saturday
        if current_time == '12:00:00':
            await post_food('lunch')

    if day_of_week == 6:  # sunday
        if current_time == '10:30:00':
            await post_food('brunch')
        if current_time == '04:30:00':
            await post_food('dinner')


@timeloop.before_loop
async def before_timeloop():
    minutes_to_sleep = 15 - datetime.now().minute % 15
    print(datetime.now().minute)
    seconds_to_sleep = 60 - datetime.now().second
    print((minutes_to_sleep * 60) + seconds_to_sleep - 60)
    print("seconds to launch")
    await asyncio.sleep((minutes_to_sleep * 60) + seconds_to_sleep - 60)


async def post_food(meal):
    channel = client.get_channel(channelDict[meal])
    food = MealFinder.getmeal(meal, numEntries=10)
    await channel.send(food)


async def test_food(meal):
    channel = client.get_channel(channelDict['testing'])
    food = MealFinder.getmeal(meal, numEntries=10)
    await channel.send(food)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    timeloop.start()
    clock.start()
    await test_food('dinner')
    activity = discord.Activity(name='the cafe menu', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)


@client.event
async def on_member_join(member):
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

    if message.content.startswith('!dinner'):
        channel = client.get_channel(809190205416013876)
        food = MealFinder.getmeal("dinner", numEntries=10)
        await channel.send(food)


client.run(token)
