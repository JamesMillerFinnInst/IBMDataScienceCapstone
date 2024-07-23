import pandas as pd
import numpy as np
import requests
import datetime
import os

# Define Directory
directory = r'\\someserver\shared\Courses\Capstone'
################################################## Define Functions ####################################################
########## Define functions to Call the SpaceX API #########
# Uses the rocket column of df to append rocket data to a list
def getBoosterVersion(data):
    for x in data['rocket']:
       if x:
        response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
        BoosterVersion.append(response['name'])

# Uses the launchpad column of df to append rocket data to a list
def getLaunchSite(data):
    for x in data['launchpad']:
       if x:
         response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
         Longitude.append(response['longitude'])
         Latitude.append(response['latitude'])
         LaunchSite.append(response['name'])

# Uses the payload column of df to append rocket data to a list
def getPayloadData(data):
    for load in data['payloads']:
       if load:
        response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])

# Uses the cores column of df to append rocket data to a list
def getCoreData(data):
    for core in data['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            else:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)
            Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            Flights.append(core['flight'])
            GridFins.append(core['gridfins'])
            Reused.append(core['reused'])
            Legs.append(core['legs'])
            LandingPad.append(core['landpad'])
########################################################################################################################
########## Read in Data ##########
url = r"https://api.spacexdata.com/v4/launches/past"

response = requests.get(url)
if response.status_code == 200:
    df = pd.json_normalize(response.json())
else:
    print(f"Exception encountered in web request")
    raise Exception

########## Process Data ##########
# Index to columns of interest
df = df[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# Remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters
# Remove rows that have multiple payloads in a single rocket.
df = df[df['cores'].map(len)==1]
df = df[df['payloads'].map(len)==1]

# Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
df['cores'] = df['cores'].map(lambda x: x[0])
df['payloads'] = df['payloads'].map(lambda x: x[0])

# Filter by date
df['date'] = pd.to_datetime(df['date_utc']).dt.date
df = df[df['date'] <= datetime.date(2020, 11, 13)]

# Initialize empty lists for API calls
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

# Call API functions
getBoosterVersion(df)
getLaunchSite(df)
getPayloadData(df)
getCoreData(df)

# Create new dataframe
launch_dict = {'FlightNumber': list(df['flight_number']),
                'Date': list(df['date']),
                'BoosterVersion':BoosterVersion,
                'PayloadMass':PayloadMass,
                'Orbit':Orbit,
                'LaunchSite':LaunchSite,
                'Outcome':Outcome,
                'Flights':Flights,
                'GridFins':GridFins,
                'Reused':Reused,
                'Legs':Legs,
                'LandingPad':LandingPad,
                'Block':Block,
                'ReusedCount':ReusedCount,
                'Serial':Serial,
                'Longitude': Longitude,
                'Latitude': Latitude}
df = pd.DataFrame(launch_dict)

# Filter out Falcon 1 launches
len_before = len(df)
df = df[df['BoosterVersion'] != 'Falcon 1']
if len(df) == len_before:
    print(f"Failed to filter, len still at: {len_before}")

# Handle missing values
df['PayloadMass'] = df['PayloadMass'].fillna(df['PayloadMass'].mean())

# Examine output
pd.set_option('display.max_columns', None)
# print(df.describe(include = 'all'))

# Write out data
df.to_csv(os.path.join(directory, 'Data Files', 'Launch Data API.csv'), index=False)
