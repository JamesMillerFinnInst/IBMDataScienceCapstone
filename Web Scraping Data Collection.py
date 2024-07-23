import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd
import os

# Define directory
directory = r'\\finnhudson\shared\James Upstate Reform\Professional\Certs\Coursera\IBM Data Science\Local Project\Courses\Capstone'
################################################## Define Functions ####################################################
def date_time(table_cells):
    """
    This function returns the data and time from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]


def booster_version(table_cells):
    """
    This function returns the booster version from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i % 2 == 0][0:-1])
    return out


def landing_status(table_cells):
    """
    This function returns the landing status from the HTML table cell
    Input: the  element of a table data cell extracts extra row
    """
    out = [i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0:mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass


def extract_column_from_header(row_text):
    """
    This function returns the landing status from the HTML table cell
    Input: the  element of a table data cell extracts extra row_text
    """
    if row_text.br:
        row_text.br.extract()
    if row_text.a:
        row_text.a.extract()
    if row_text.sup:
        row_text.sup.extract()

    colunm_name = ' '.join(row_text.contents)

    # Filter the digit and empty names
    if not (colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name
########################################################################################################################
# Read in data
url = r"https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content)
else:
    print(f"Exception encountered in web request")
    raise Exception

# Find third table with launc data
tables = soup.find_all('table')
desired_table = tables[2]

# Gather columns from the table html
columns = []
for column_name in desired_table.find_all('th'):
    name = extract_column_from_header(column_name)
    if name is not None and len(name) > 0:
        columns.append(name)
launch_dict= dict.fromkeys(columns)

# Remove an irrelvant column
del launch_dict['Date and time ( )']

# Initialize launch dict with empty lists
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []

# Added some new columns
launch_dict['Version Booster']=[]
launch_dict['Booster landing']=[]
launch_dict['Date']=[]
launch_dict['Time']=[]

extracted_row = 0

# Extract each table
df = pd.DataFrame()
for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):

    # get table row
    for rows in table.find_all("tr"):

        # check to see if first table heading is as number corresponding to launch a number
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False

        # get table element
        row = rows.find_all('td')

        # if it is number save cells in a dictonary
        if flag:
            extracted_row += 1

            # Flight Number value
            launch_dict['Flight No.'] = [flight_number]

            # Date value
            datatimelist = date_time(row[0])
            date = datatimelist[0].strip(',')
            launch_dict['Date'] = [date]

            # Time value
            time = datatimelist[1]
            launch_dict['Time'] = [time]

            # Booster version
            bv = booster_version(row[1])
            if not bv:
                bv = row[1].a.string
            launch_dict['Version Booster'] = [bv]

            # Launch Site
            launch_site = row[2].a.string
            launch_dict['Launch site'] = [launch_site]

            # Payload
            payload = row[3].a.string
            launch_dict['Payload'] = [payload]

            # Payload Mass
            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'] = [payload_mass]

            # Orbit
            orbit = row[5].a.string
            launch_dict['Orbit'] = [orbit]

            # Customer
            try:
                customer = row[6].a.string
            except AttributeError:
                customer = ''
            launch_dict['Customer'] = [customer]

            # Launch outcome
            launch_outcome = list(row[7].strings)[0]
            launch_dict['Launch outcome'] = [launch_outcome]

            # Booster landing
            booster_landing = landing_status(row[8])
            launch_dict['Booster landing'] = [booster_landing]
            df = pd.concat([df, pd.DataFrame(launch_dict)], ignore_index=True)

# Examine output
pd.set_option('display.max_columns', None)
print(df.describe(include = 'all'))

df.to_csv(os.path.join(directory, 'Data Files', 'Launch Data Scraped.csv'), index=False)