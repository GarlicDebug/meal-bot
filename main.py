import os
import asyncio
import datetime
import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime

# Discord API token is stored in un-versioned .env file for safety
load_dotenv()
token = os.environ.get("discord-token")

# Dictionary for storing and easily referencing Discord channel IDs
channelDict = {
    'general': 811076981986557982,
    'testing': 809200134533283900,
    'breakfast': 811076422806011914,
    'brunch': 811076467764756481,
    'lunch': 811076467764756481,
    'dinner': 809190205416013876,
    'weather': 812464306599624714,
}

cleaningDict = {
    'Upon Request': '^ Vegan/GF option available',
    'Build Your Own Fruit Salad Bar': 'Fruit',
    'Whole Grain Brown Rice': 'Brown Rice',
    'Whole Grain Brown Rice and Beans': 'Brown Rice and Beans',
    'Build Your Own Salad Bar with Assorted Salad Dressings': 'Salad',
    'Chef\'s Choice Beans': 'Beans',
    'Chef\'s Choice Soup': 'Soup',
    'Carlson Arbogast Black Beans': 'Black Beans',
    'Carlson Arbogast White Beans': 'White Beans',
    'Carlson Arbogast Cranberry Beans': 'Cranberry Beans',
    'Old Fashion Rolled Oats': 'Rolled Oats',
}

client = discord.Client()

bot = commands.Bot("!")


def getmeal(mealname, num_entries, ping):
    """
    Pulls menu items from cafe website and adds them to a string for posting.
    :param mealname: string
        Name of the meal
    :param num_entries: int
        Number of entries to add to string
    :return: string
        Meal entries separated by newlines.
    """

    URL = 'https://andrews-university.cafebonappetit.com/cafe/terrace-cafe/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    meal = soup.find(id=mealname)

    meal_items = meal.find_all(class_="h4 site-panel__daypart-item-title")

    menu_string = "Today's " + mealname + " options are: \n\n"

    for meal_item in meal_items[:num_entries]:
        meal_item = meal_item.text.strip()
        if meal_item in cleaningDict:
            meal_item = cleaningDict[meal_item]
        menu_string += meal_item + "\n"

    if ping is True:
        menu_string = "@everyone\n\n" + menu_string
    print(menu_string)
    return menu_string

# TODO: indicate that multiples are vegan
# TODO: Move or document helper info

@tasks.loop(minutes=15)
async def timeloop():
    """
    Checks every 15 minutes if the time matches a set time for posting a meal menu and acts accordingly
    :return:
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    print("Meal loop time =", current_time)

    day_of_week = datetime.today().weekday()

    if day_of_week < 5:  # weekdays
        if current_time == '06:30:00':
            await post_food('breakfast')
        if current_time == '10:30:00':
            await post_food('lunch')
        if current_time == '16:30:00':
            await post_food('dinner')

    if day_of_week == 5:  # saturday
        if current_time == '12:00:00':
            await post_food('lunch')

    if day_of_week == 6:  # sunday
        if current_time == '10:30:00':
            await post_food('brunch')
        if current_time == '16:30:00':
            await post_food('dinner')


@timeloop.before_loop
async def before_timeloop():
    minutes_to_sleep = 15 - datetime.now().minute % 15  # minutes we need to wait to reach a multiple of 15 min
    seconds_to_sleep = 60 - datetime.now().second  # seconds we need to wait until the next whole minute
    # sleep until the next 15 min increment then start loop
    await asyncio.sleep((minutes_to_sleep * 60) + seconds_to_sleep - 60)


async def post_food(meal):
    """
    Sends a message to the appropriate channel with the menu info for a given meal
    :param meal: str
        The name of the meal. Referenced for name of channel in channelDict
    :return:
    """
    channel = client.get_channel(channelDict[meal])
    food = getmeal(meal, num_entries=11, ping=True)
    await channel.send(food)


async def test_food(meal):
    """
    A debugging function that sends menu info for a meal to the testing channel.
    :param meal: str
        The name of the meal.
    :return:
    """
    channel = client.get_channel(channelDict['testing'])
    food = getmeal(meal, num_entries=11, ping=False)
    await channel.send(food)


@tasks.loop(seconds=10)
async def clock():
    """
    A debugging function that displays the system time every 10 seconds
    :return:
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Clock Time =", current_time)


@clock.before_loop
async def before_clock():
    """
    A helper function that delays the debugging clock until a multiple of 10 seconds
    :return:
    """
    print('Starting debug clock')
    seconds_to_sleep = 10 - (datetime.now().second % 10)
    print(seconds_to_sleep)
    await asyncio.sleep(seconds_to_sleep)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    timeloop.start()
    # await test_food("breakfast")

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
        food = getmeal("dinner", num_entries=10)
        await channel.send(food)


client.run(token)
