import pandas as pd
import argparse
import numpy as np

# import the full covid dataframe and create the dataframe for the relevant covid data
covid_data = pd.read_csv('owid-covid-data.csv', encoding = 'ISO-8859-1')

## tried here to make index as location but didn't work

# data = full_covid_data[['date','total_cases','new_cases','total_deaths','new_deaths']].values
# columns = ['date','total_cases','new_cases','total_deaths','new_deaths']
# index=full_covid_data['location'].values
# relevant_data = pd.DataFrame(data, columns = columns, index = index)
# relevant_data.index.name = 'location'






#covid_data
