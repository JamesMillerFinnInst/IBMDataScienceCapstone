from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from folium.features import DivIcon
import pandas as pd
import folium
import os

# define directory
directory = r'\\someserver\shared\Courses\Capstone'

# Read in data
url = r'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
df = pd.read_csv(url)

# Drill down to launch site coordinates
spacex_df = df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
print(f"Launch sites: \n{launch_sites_df['Launch Site'].value_counts()}\n")

# Initialize map centered on NASA in Houston
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))

# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,

    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)

# Add launch sites to the map
for idx, row in launch_sites_df.iterrows():
    lat = row['Lat']
    long = row['Long']
    launch_site = row['Launch Site']

    # Create a circle for the launch site
    circle = folium.Circle([lat, long], radius=1000, color='#d35400', fill=True).add_child(folium.Popup(launch_site))

    # Create a marker for the launch site
    marker = folium.map.Marker(
        [lat, long],
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % launch_site,
        )
    )

    site_map.add_child(circle)
    site_map.add_child(marker)

site_map.save(os.path.join(directory, 'Maps', 'Launch Sites Map.html'))
site_map

# Create a marker cluster
marker_cluster = MarkerCluster()


# Function to set marker color based on class
def set_marker_color(class_val):
    if class_val == 1:
        return 'green'
    else:
        return 'red'


# Add markers for each launch record
for index, record in spacex_df.iterrows():
    lat = record['Lat']
    long = record['Long']
    class_val = record['class']
    marker_color = set_marker_color(class_val)

    marker = folium.Marker(
        location=[lat, long],
        icon=folium.Icon(color=marker_color),
        popup=f'Class: {class_val}'
    )
    marker_cluster.add_child(marker)

site_map.add_child(marker_cluster)
site_map.save(os.path.join(directory, 'Maps', 'Launch Sites with Outcomes Map.html'))
site_map


# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)
site_map

from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

coastline_lat = 28.56367
coastline_lon = -80.57163
launch_site_lat = 28.5623 
launch_site_lon = -80.5774

# Calculate the distance
distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)
print(f"Distance to coastline: {distance_coastline:.2f} km")

# Add a marker for the coastline
distance_marker = folium.Marker(
    [coastline_lat, coastline_lon],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
    )
)
site_map.add_child(distance_marker)

# Draw a line between the launch site and the coastline
lines = folium.PolyLine(locations=[[launch_site_lat, launch_site_lon], [coastline_lat, coastline_lon]], weight=1)
site_map.add_child(lines)

site_map.save(os.path.join(directory, 'Maps', 'Launch Sites with Ditances Map.html'))
site_map


