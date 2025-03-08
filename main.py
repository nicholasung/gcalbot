from gcsa.event import Event
from google.oauth2.service_account import Credentials
from gcsa.google_calendar import GoogleCalendar
from dotenv import load_dotenv
# from discord.ext import commands
# from discord import app_commands
# import io
# import discord
import os
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

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
calendar = gc.get_calendar(cal_id)

# Fetch and print events from the specified calendar
events = list(gc.get_events(calendar_id=cal_id))
print(f"Found {len(events)} events in calendar {cal_id}.")

def datetimeToStr(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S')

for event in events:
    print(event.summary + " " + datetimeToStr(event.start))

