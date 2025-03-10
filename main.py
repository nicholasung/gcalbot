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

async def discordEventFromName(name: str, guild: discord.guild): #untest
    list = await guild.fetch_scheduled_events()
    result = None
    for event in list:
        if event.name == name:
            result = event
    return result


def gcalAdd(name: str, start: datetime, end: datetime, location: str): #adds an event to google Calendar with checks for prexisiting 
    event = gcalEventFromName(name)
    if event is None:
        if not location:
            location = " " 
    if(event == None):
        event = Event(summary=name, start=start, end=end, location=location)
        event = gc.add_event(event)
        print("added " + event.summary )
    else:
        event.summary = name
        event.start = start
        event.end = end
        event.location = location
        event = gc.update_event(event) 
        print("updated " + event.summary )

async def discordAdd(name: str, start: datetime, end: datetime, guild: discord.guild, location: str):
    event = await discordEventFromName(name=name, guild=guild)
    if event is None:
        if not location:
            location = " " 
    if(event == None):
        await guild.create_scheduled_event(name=name, start_time=start, end_time=end, location=location, entity_type=discord.EntityType.external, privacy_level= discord.PrivacyLevel.guild_only)
        print("added " + name )
    else:
        await event.edit(name=name, start_time=start, end_time=end, location=location) 
        print("updated " + event.name )

@tree.command(name="status", description="Check the bot's status")
async def status(interaction: discord.Interaction):
     await interaction.response.send_message('master manipulator is up', ephemeral=True)
     print(interaction.user.name + " requested status")

@tree.command(name="push", description="add discord events to gcal")
async def push(interaction:discord.Interaction):
    reply = "Pushed: \n"
    await interaction.response.defer()
    list = await interaction.guild.fetch_scheduled_events()
    for plan in list:
        reply += plan.name
        reply += '\n\n'
        gcalAdd(name=plan.name, start=plan.start_time, end=plan.end_time, location=plan.location)
    await interaction.followup.send(reply, ephemeral = False)

@tree.command(name="pull", description="add gcal events to discord")
async def pull(interaction:discord.Interaction):
    reply = "Pulled: \n"
    await interaction.response.defer()
    list = calendar.get_events()
    for plan in list:
        reply += plan.summary
        reply += '\n\n'
        await discordAdd(name=plan.summary, start=plan.start, end=plan.end, location=plan.location, guild=interaction.guild)
    await interaction.followup.send(reply, ephemeral = False)
         

@tree.command(name="events", description="list all the current events in the server")
async def events(interaction:discord.Interaction):
    reply = ""
    await interaction.response.defer()
    list = await interaction.guild.fetch_scheduled_events()
    print(interaction.user.name + " requested events")
    for plan in list:
        print(plan.name)
        reply = reply + plan.name + '\n\n'
    await interaction.followup.send(reply, ephemeral = False)

@bot.event
async def on_ready():
    await tree.sync()
    print('We have logged in and synced')
    print('Synced commands:')
    for command in tree.walk_commands():
        print(f"- {command.name}: {command.description}")

bot.run(token)

