from bs4 import BeautifulSoup
import requests
from datetime import datetime, timezone, timedelta
import os
from twilio.rest import Client

# Reading from The Empire State Building website to determine lights information 
url = "https://www.esbnyc.com/about/tower-lights"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

my_element = soup.select("div.is-today")[0]
today_empire_state_bldg_color = my_element.text.strip().replace("Share", "")
print(today_empire_state_bldg_color)

# Code to determine NYC sunset time
sunset_url = f'https://api.sunrise-sunset.org/json?lat=40.748817&lng=-73.985428'
sunset_response = requests.get(sunset_url)
sunset_data = sunset_response.json()
sunset_time = sunset_data['results']['sunset']

# Create a datetime object from the sunset time string
time_obj = datetime.strptime(sunset_time, '%I:%M:%S %p')

# Convert UTC time to EST time
est_tz = timezone(timedelta(hours=-4))
est_time = time_obj.replace(tzinfo=timezone.utc).astimezone(est_tz)

# Setting up Twilio notification
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_nyc = os.environ['TWILIO_NUMBER']
recipient = os.environ['RECIPIENT_NUMBER']

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Hello from by The Empire State Building",
                     from_=twilio_nyc,
                     to=recipient
                 )

print(message.sid)

