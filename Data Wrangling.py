import pandas as pd
import os

# define directory
directory = r'\\finnhudson\shared\James Upstate Reform\Professional\Certs\Coursera\IBM Data Science\Local Project\Courses\Capstone'

# Read in data
df = pd.read_csv(os.path.join(directory, 'Launch Data API.csv'), index_col=False)

# Print out values
print(f"Launces per site: \n{df['LaunchSite'].value_counts()} \n")
print(f"Orbits: \n{df['Orbit'].value_counts()}\n")

landing_outcomes = df['Outcome'].value_counts()
print(f"Oucomes: \n{landing_outcomes}")

# Create bad_outcomes column
bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
df['Landing_Class'] = 1
df.loc[df['Outcome'].isin(bad_outcomes), 'Landing_Class'] = 0

# Print out values
print(f"Outcome class: \n{df['Landing_Class'].value_counts()} \n")
print(f"Mean of landing class: {df['Landing_Class'].mean()}")

df.to_csv(os.path.join(directory, 'Data Files', 'Wrangled Data.csv'), index=False)