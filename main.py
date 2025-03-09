from gcsa.event import Event
from google.oauth2.service_account import Credentials
from gcsa.google_calendar import GoogleCalendar
from dotenv import load_dotenv
# from discord.ext import commands
# from discord import app_commands
# import io
# import discord
import os
from datetime import datetime, timezone, date, time, timedelta

# Load environment variables from .env file
load_dotenv()
token = os.getenv('TOKEN')
cal_id = os.getenv('CAL_ID')
print(token)
print(cal_id)

#authenticate
credentials_path = ".credentials/credentials.json"
credentials = Credentials.from_service_account_file(credentials_path)

#get calendar
gc = GoogleCalendar(credentials=credentials)
gc.default_calendar=cal_id
calendar = gc #.get_calendar(cal_id)

# Fetch and print events from the specified calendar
events = list(gc.get_events())
print(f"Found {len(events)} events in calendar {cal_id}.")

def datetimeToStr(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S')

for event in events:
    print(event.summary + " " + datetimeToStr(event.start))
    if event.summary == "test":
        update = event

# year = 2025
# month = 3
# day = 9
# hour = 13
# min = 25
# hour_duration = 2.5

# start = datetime(year, month, day, hour, min)
# end = start + timedelta(hours=hour_duration)
# event = Event('test', start, end)

# print(event.summary + " " + datetimeToStr(event.start) + " end at " + datetimeToStr(event.end))
# response = gc.add_event(event)
# print(response)


update.location = "OVER HERE"

response = gc.update_event(update)
print(response)

