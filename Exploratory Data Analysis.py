import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# define directory
directory = r'\\finnhudson\shared\James Upstate Reform\Professional\Certs\Coursera\IBM Data Science\Local Project\Courses\Capstone'

# Read in data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
df = pd.read_csv(url)
print(f"Columns in df: {df.columns.tolist()}")

# Visualize flight number & launch site
sns.catplot(data=df, x='FlightNumber', y='LaunchSite', hue='Class', aspect=2)
plt.title('Flight Number vs Launch Site')
plt.xlabel('Flight Number')
plt.ylabel('Launch Site')
plt.show()

# Visualize payload mass & launch site
sns.catplot(data=df, x='PayloadMass', y='LaunchSite', hue='Class', aspect=2)
plt.title('Payload Mass vs Launch Site')
plt.xlabel('Payload Mass (kg)')
plt.ylabel('Launch Site')
plt.show()

# Visualize success rate by orbit type
success_rate = df.groupby('Orbit')['Class'].mean().reset_index()
success_rate.columns = ['Orbit', 'SuccessRate']
sns.barplot(x='Orbit', y='SuccessRate', data=success_rate)
plt.title('Success Rate of Each Orbit Type')
plt.xlabel('Orbit Type')
plt.ylabel('Success Rate')
plt.xticks(rotation=45)
plt.show()

# Visualize flight number by orbit type
sns.scatterplot(data=df, x='FlightNumber', y='Orbit', hue='Class')
plt.title('Flight Number vs Orbit')
plt.xlabel('Flight Number')
plt.ylabel('Orbit')
plt.show()

# Visualize Payload Mass & orbit type
sns.scatterplot(data=df, x='PayloadMass', y='Orbit', hue='Class')
plt.title('Payload Mass vs Orbit')
plt.xlabel('Payload Mass (kg)')
plt.ylabel('Orbit')
plt.show()

# Task 6: Visualize the launch success yearly trend
def Extract_year(dataframe):
    df['Year'] = pd.DatetimeIndex(df['Date']).year

# Plot a line chart with x axis to be the extracted year and y axis to be the success rate
Extract_year(df)
yearly_success = df.groupby('Year')['Class'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=yearly_success, x='Year', y='Class')
plt.title('Yearly Success Rate')
plt.xlabel('Year')
plt.ylabel('Success Rate')
plt.show()

# Features Engineering
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()

# Task 7: Create dummy variables for categorical columns
features_one_hot = pd.get_dummies(features, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])

# Task 8: Cast all numeric columns to float64
features_one_hot = features_one_hot.astype('float64')

# Save the processed dataframe to a CSV file
features_one_hot.to_csv(os.path.join(directory, 'Data Files', 'Exploratory Data Analysis.csv'), index=False)
