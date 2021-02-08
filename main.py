import discord
from mealFinder import MealFinder
from discord.ext import commands, tasks

# Discord API token is stored in unversioned .env file for safety
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("discord-token")

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    MealFinder.getmeal("dinner", numEntries=10)

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
async def on_message(self, message):
    # we do not want the bot to reply to itself
    if message.author.id == self.user.id:
        return

    if message.content.startswith('!hello'):
        await message.reply('Hello!', mention_author=True)


client.run(token)
