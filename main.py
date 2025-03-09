from gcsa.event import Event
from google.oauth2.service_account import Credentials
from gcsa.google_calendar import GoogleCalendar
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
import io
import discord
import os
from datetime import datetime, timezone, date, time, timedelta

# Load environment variables from .env file
load_dotenv()
token = os.getenv('TOKEN')
cal_id = os.getenv('CAL_ID')
print(token)
print(cal_id)

# authenticate
credentials_path = ".credentials/credentials.json"
credentials = Credentials.from_service_account_file(credentials_path)

# get calendar
gc = GoogleCalendar(credentials=credentials)
gc.default_calendar=cal_id
calendar = gc

# Discord bot init 
intents = discord.Intents.default()
intents.guild_messages = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Fetch and print events from the specified calendar
events = list(gc.get_events())
print(f"Found {len(events)} events in calendar {cal_id}.")


def datetimeToStr(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S')

def eventFromName(name):
    for event in list(gc.get_events()):
            if event.summary == name:
                result = event
    return result

@tree.command(name="status", description="Check the bot's status")
async def status(interaction: discord.Interaction):
     await interaction.response.send_message('master manipulator is up', ephemeral=True)
     print(interaction.user.name + " requested status")

@tree.command(name="events", description="list all the current events in the server")
async def events(interaction:discord.Interaction):
    reply = ""
    await interaction.response.defer()
    list = await interaction.guild.fetch_scheduled_events()
    print(interaction.user.name + " requested events")
    for thing in list:
        print(thing.name)
        reply = reply + thing.name + " | "
    await interaction.followup.send(reply, ephemeral = False)

@bot.event
async def on_ready():
    await tree.sync()
    print('We have logged in and synced')
    print('Synced commands:')
    for command in tree.walk_commands():
        print(f"- {command.name}: {command.description}")

bot.run(token)

