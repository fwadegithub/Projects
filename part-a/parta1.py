import pandas as pd
import argparse
import numpy as np

### sub task 1

# import the full covid dataframe and create the dataframe for the relevant covid data
covid_data = pd.read_csv('owid-covid-data.csv', encoding = 'ISO-8859-1')

relevant_data = covid_data[['location','date','new_cases','new_deaths']]

# convert the date string to an integer representing the month it is in.
dates = []
bad_index = []
for i in relevant_data.index:
    if relevant_data.date[i][-4:] != '2020':
        bad_index.append(i)
        continue
    month_index = int(relevant_data.date[i][-7:-5])
    dates.append(month_index)

relevant_data = relevant_data.drop(bad_index)
relevant_data.index = list(range(len(relevant_data)))
relevant_data['date'] = dates

# create a dictionary of the indexes corresponding to each location
location_dic = {}
for i in range(len(relevant_data.index)):
    if relevant_data.location[i] not in location_dic:
        location_dic[relevant_data.location[i]] = [i]
    else:
        location_dic[relevant_data.location[i]].append(i)

# create a new data frame with the monthly new case and new death data for each location

months = ['January','February','March','April','May','June','July','August','September','October','November','December']
full_data = [];

# retrieving the monthly data for each location and adding to the full data list
for location in location_dic:
    location_data = {}
    
    for index in location_dic[location]:

        month = months[relevant_data.date[index]-1]
        new_cases = relevant_data.new_cases.values[index]
        new_deaths = relevant_data.new_deaths.values[index]
        if np.isnan(new_cases):
            new_cases = 0;
        if np.isnan(new_deaths):
            new_deaths = 0;

        if month not in location_data.keys():
            location_data[month] = [int(new_cases), int(new_deaths)]
        else:
            location_data[month][0] += int(new_cases)
            location_data[month][1] += int(new_deaths)
    for month in location_data.keys():
        if location_data[month] != [0,0]:
            month_list = [location, month, location_data[month][0], location_data[month][1]]
            full_data.append(month_list)

monthly_covid_data = pd.DataFrame(full_data, columns = ['location', 'month','new_cases','new_deaths'])

# make new location dictionary of indexes relevant to each location in the new Data Frame
location_dic2 = {}
for i in range(len(monthly_covid_data.index)):
    if monthly_covid_data.location[i] not in location_dic2:
        location_dic2[monthly_covid_data.location[i]] = [i]
    else:
        location_dic2[monthly_covid_data.location[i]].append(i)

# retrieve the data for monthly total cases and deaths and add it to the Data Frame
total_deaths = []
total_cases = []
for location in location_dic2.keys():
    start = location_dic2[location][0]
    end = location_dic2[location][-1] + 1
    cases = list(monthly_covid_data.new_cases[start:end].cumsum())
    deaths = list(monthly_covid_data.new_deaths[start:end].cumsum())
    for i in range(len(cases)):
        total_deaths.append(deaths[i])
        total_cases.append(cases[i])
        
monthly_covid_data['total_cases'] = total_cases
monthly_covid_data['total_deaths'] = total_deaths

### sub task 2

# find the case fatality rate and add it to the data frame
fatality_rates = []
for index in monthly_covid_data.index:
    fatality_rate = monthly_covid_data.new_deaths[index]/monthly_covid_data.new_cases[index]
    fatality_rates.append(fatality_rate)
    
monthly_covid_data['case_fatality_rate'] = fatality_rates

# put the columns in the correct order
# rearranging the columns
column_names = ['location','month','case_fatality_rate','total_cases','new_cases','total_deaths','new_deaths']
monthly_covid_data = monthly_covid_data.reindex(columns = column_names)

# export as csv and print the first 5 rows
print(monthly_covid_data.head())
monthly_covid_data.to_csv(r'owid-covid-data-2020-monthly.cvs', index=False, header=True)
