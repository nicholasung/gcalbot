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

def datetimeToStr(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S')

def gcalEventFromName(name: str):
    result = None
    for event in list(gc.get_events()):
            if event.summary == name:
                result = event
    return result

def discordEventFromName(name: str, guild: discord.guild): #untest
    list = guild.fetch_scheduled_events()
    result = None
    for event in list:
        if event.name == name:
            result = event


def gcalAdd(name: str, start: datetime, end: datetime, location="" ): #adds an event to google Calendar with checks for prexisiting 
    event = gcalEventFromName(name)
    if(event == None):
        event = Event(summary=name, start=start, end=end, location=location)
        event = gc.add_event(event)
    else:
        event.summary = name
        event.start = start
        event.end = end
        event.location = location
        event = gc.update_event(event) 

def discordAdd(name: str, start: datetime, end: datetime, guild: discord.guild, location="" ):
    event = discordEventFromName(name=name, guild=guild)
    if(event == None):
        #create
    else:
        #update


         
     

@tree.command(name="status", description="Check the bot's status")
async def status(interaction: discord.Interaction):
     await interaction.response.send_message('master manipulator is up', ephemeral=True)
     print(interaction.user.name + " requested status")

# @tree.command(name="push", description="add discord events to gcal")
# async def push(interaction:discord.Interaction):
#     await interaction.response.defer()
#     list = await interaction.guild.fetch_scheduled_events()
#     for plan in list:
         

@tree.command(name="events", description="list all the current events in the server")
async def events(interaction:discord.Interaction):
    reply = ""
    await interaction.response.defer()
    list = await interaction.guild.fetch_scheduled_events()
    print(interaction.user.name + " requested events")
    for plan in list:
        print(plan.name)
        reply = reply + plan.name + " | "
    await interaction.followup.send(reply, ephemeral = False)



@bot.event
async def on_ready():
    await tree.sync()
    print('We have logged in and synced')
    print('Synced commands:')
    for command in tree.walk_commands():
        print(f"- {command.name}: {command.description}")

bot.run(token)

