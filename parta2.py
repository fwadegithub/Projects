import pandas as pd
import argparse
import matplotlib.pyplot as plt

monthly_data = pd.read_csv('owid-covid-data-2020-monthly.csv', encoding = 'ISO-8859-1')

# create new data frame with the confirmed new cases and case fatality rate of each location

plot_data = []
locations = set(monthly_data['location'])

for location in locations:
    relevant_data = monthly_data.loc[monthly_data['location'] == location]
    confirmed_cases = relevant_data['total_cases'].max()
    deaths = relevant_data['total_deaths'].max()
    fatality_rate = deaths/confirmed_cases
    location_data = [location, confirmed_cases, fatality_rate]
    plot_data.append(location_data)
    
plot_data = pd.DataFrame(plot_data, columns = ['location','confirmed_cases','fatality_rate'])

# identify the plot names from the given inputs
parser = argparse.ArgumentParser()
parser.add_argument("scatterA")
parser.add_argument("scatterB")
args = parser.parse_args()

# plot this data frame as a scatter plot
plt.scatter(plot_data.iloc[:,1], plot_data.iloc[:,2])
plt.ylabel("case_fatality_rate")
plt.xlabel("confirmed new cases")
plt.grid(True)
plt.savefig(args.scatterA)
plt.show()

# plot this data frame as a scatter plot with a log scale in the x axis
plt.scatter(plot_data.iloc[:,1], plot_data.iloc[:,2])
plt.xscale('log')
plt.ylabel("case_fatality_rate")
plt.xlabel("confirmed new cases")
plt.grid(True)
plt.savefig(args.scatterB)
plt.show()