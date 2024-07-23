import pandas as pd
import sqlalchemy
import sqlite3
import os

# define directory
directory = r'\\someserver\shared\Courses\Capstone'

# Read in data
url = r"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"
df = pd.read_csv(url)
print(f"Columns: {df.columns.tolist()}")
for column in df.columns:
    print(f"\nColumn {column} values: \n{df[column].value_counts()}")

# Establish connection to database
con = sqlite3.connect(os.path.join(directory, 'Data Files', "Launch Analysis Database.db"))
cur = con.cursor()

# Write data into database
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")

# Craete table
cur.execute("DROP TABLE IF EXISTS SPACEXTABLE")
cur.execute("create table SPACEXTABLE as select * from SPACEXTBL where Date is not null")


##### Execute Queries #####
# Query unique launch site names
cur.execute('SELECT DISTINCT(Launch_Site) FROM SPACEXTABLE')
print(f"Unique launch site names: \n{cur.fetchall()}\n")

# Query launch sites beginning with "CCA"
cur.execute('SELECT DISTINCT(Launch_Site) FROM SPACEXTABLE WHERE Launch_Site LIKE "CCA%"')
print(f"Launch sites beginning with 'CCA': \n{cur.fetchall()}\n")

# Query total payload mass carried by boosters launched by NASA
cur.execute('SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTABLE WHERE Customer = "NASA (CRS)"')
print(f"Total payload mass carried by NASA: \n{cur.fetchall()}\n")

# Query average payload mass carried by booster version F9 v1.1
cur.execute('SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTABLE WHERE Booster_Version = "F9 v1.1"')
print(f"Average payload mass carried by Version 'F9 v1.1': \n{cur.fetchall()}\n")

# Query average payload mass carried by booster version F9 v1.1
cur.execute('SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTABLE WHERE Booster_Version = "F9 v1.1"')
print(f"Average payload mass carried by Version 'F9 v1.1': \n{cur.fetchall()}\n")

# Query first successful ground pad landing date
cur.execute('SELECT Date FROM SPACEXTABLE WHERE Landing_Outcome = "Success (ground pad)"')
print(f"First successful landing on a ground pad was on: \n{cur.fetchall()}\n")

# Query boosters with success in drone ship and have payload mass between 4000 & 6000
cur.execute('SELECT Booster_Version FROM SPACEXTABLE WHERE Landing_Outcome = "Success (drone ship)" AND '
            'PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000')
print(f"Boosters landed on drone ship and between 4000 & 6000 payload mass: \n{cur.fetchall()}\n")

# Query Successful missions and failed missions
cur.execute('SELECT COUNT(Mission_Outcome) FROM SPACEXTABLE WHERE Landing_Outcome LIKE "Success"')
print(f"Successful missions: \n{cur.fetchall()}\n")
cur.execute('SELECT COUNT(Mission_Outcome) FROM SPACEXTABLE WHERE Landing_Outcome LIKE "Failure"')
print(f"Failed missions: \n{cur.fetchall()}\n")

# Query boosters that have carried the maximum payload mass
cur.execute('SELECT Booster_Version FROM SPACEXTABLE WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTABLE)')
print(f"Boosters that have carried the max payload: \n{cur.fetchall()}\n")

# Query landing outcomes in drone ship by month in 2015
cur.execute("""SELECT 
    CASE 
        WHEN substr(Date, 6, 2) = '01' THEN 'January'
        WHEN substr(Date, 6, 2) = '02' THEN 'February'
        WHEN substr(Date, 6, 2) = '03' THEN 'March'
        WHEN substr(Date, 6, 2) = '04' THEN 'April'
        WHEN substr(Date, 6, 2) = '05' THEN 'May'
        WHEN substr(Date, 6, 2) = '06' THEN 'June'
        WHEN substr(Date, 6, 2) = '07' THEN 'July'
        WHEN substr(Date, 6, 2) = '08' THEN 'August'
        WHEN substr(Date, 6, 2) = '09' THEN 'September'
        WHEN substr(Date, 6, 2) = '10' THEN 'October'
        WHEN substr(Date, 6, 2) = '11' THEN 'November'
        WHEN substr(Date, 6, 2) = '12' THEN 'December'
    END AS Month,
    Booster_Version,
    Launch_Site,
    Landing_Outcome
FROM SPACEXTABLE
WHERE substr(Date, 0, 5) = '2015'
  AND Landing_Outcome LIKE '%Failure%'
  AND Landing_Outcome LIKE '%drone ship%'""")
print(f"Failed landing outcomes in drone ship by month in 2015: \n{cur.fetchall()}\n")

# Query landing outcomes between 2010-06-04 and 2017-03-20, in descending order
cur.execute('SELECT Landing_Outcome, Date FROM SPACEXTABLE WHERE Date BETWEEN "2010-06-04" AND "2017-03-20" ORDER BY Date DESC')
print(f"Landing outcomes between dates: \n{cur.fetchall()}\n")
