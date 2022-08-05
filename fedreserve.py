#Load em up
import pandas as pd
import numpy as np
import config
import streamlit as st

# Following these instructions: https://towardsdev.com/fred-api-get-us-economic-data-using-python-e51ac8e7b1cc
import pandas_datareader as pdr # to access fred
import pandas as pd
import requests # data from api
import plotly.express as px # visualize
from datetime import datetime, date
import os
import plotly.express as px
import plotly.figure_factory as ff


# API Key
fred_api_key = config.fred_api_key

# Define function to get data from fred api
def get_fred_data(param_list, start_date, end_date):
  df = pdr.DataReader(param_list, 'fred', start_date, end_date)
  return df.reset_index()

# The Metrics 
#EMPLOYMENT
    #- Unemployment Rate
unemployment_rate = 'UNRATE'
    #- Labor Force Participation Rate
labor_force_participation_rate = 'CIVPART'
    #- Labor Force Particitpation - 55yo & Over
labor_force_participation__55yo_over = 'LNS11324230'
    #- Labor Force Participation - 25-54 years
labor_force_participation__25_52_yo = 'LNS11300060'
    #- Unemployment Rate - High School Graduates, No College
unemployment_highschool_graduates_no_college = 'LNS14027660'

#INFLATION
    #- Oil Prices
crude_oil_prices_westtx = 'DCOILWTICO'
    #- Gas Prices
gas_prices = 'GASREGW'
    #- T5YIE (5-year Breakeven)
breakeven_5_yr = 'T5YIE'
    #- CPI
median_cpi = 'MEDCPIM158SFRBCLE'
    #- Core CPI
sticky_core_cpi= 'CORESTICKM159SFRBATL'

#STOCKS
    #- Long-term Rates Outlook:
long_term_rates = 'FEDTARMDLR'

employment_metrics = [unemployment_rate, labor_force_participation_rate, labor_force_participation__55yo_over, labor_force_participation__25_52_yo, unemployment_highschool_graduates_no_college]
inflation_metrics = [crude_oil_prices_westtx, gas_prices, breakeven_5_yr, median_cpi, sticky_core_cpi]
stocks_metrics = [long_term_rates]

if os.path.isdir('employment_metrics') is False:
    os.mkdir('employment_metrics')
if os.path.isdir('inflation_metrics') is False:
    os.mkdir('inflation_metrics')


# Choose the start and end dates for the data
slide_val = st.slider('Pick the Data Start Year', min_value=1947, max_value=2022, value=2010)
year_start = str(slide_val)
start_date = year_start + '-01-01'
#start_date = pd.to_datetime(sd, format = '%Y-%m-%d')
end_date = '2022-08-05'


for metric in employment_metrics:
    df = get_fred_data(metric, start_date, end_date)
    df.to_csv(f'employment_metrics/{metric}.csv')


for metric in inflation_metrics:
    df = get_fred_data(metric, start_date, end_date)
    df.to_csv(f'inflation_metrics/{metric}.csv')

df = get_fred_data(long_term_rates, start_date, end_date)
df.to_csv(f'{long_term_rates}.csv')
st.header('Employment Metrics')

# Unemployment
ur = pd.read_csv('employment_metrics/UNRATE.csv')
ur = ur.sort_values('DATE', ascending=False)
ur['DATE'] = ur['DATE'].astype('str')

#st.dataframe(ur)
ur_today = ur['UNRATE'].iloc[0]
ur_last = ur['UNRATE'].iloc[1]
ur_change = ((ur_today / ur_last) -1) *100
ur_change = str(round(ur_change, 2)) + ' %'
# Labor Force Participation
lab_par = pd.read_csv('employment_metrics/CIVPART.csv')
lab_par = lab_par.sort_values('DATE', ascending=False)
lab_par['DATE'] = lab_par['DATE'].astype('datetime64[ns]').dt.date
lab_par_today = lab_par['CIVPART'].iloc[0]
lab_par_last = lab_par['CIVPART'].iloc[1]
lab_par_change = ((lab_par_today / lab_par_last) -1) *100
lab_par_change = str(round(lab_par_change, 2)) + ' %'
# Labor Force Participation - 55yo & Over
lab_par_55yo_over = pd.read_csv('employment_metrics/LNS11324230.csv')
lab_par_55yo_over = lab_par_55yo_over.sort_values('DATE', ascending=False)
lab_par_55yo_over['DATE'] = lab_par_55yo_over['DATE'].astype('datetime64[ns]').dt.date
lab_par_55yo_over_today = lab_par_55yo_over['LNS11324230'].iloc[0]
lab_par_55yo_over_last = lab_par_55yo_over['LNS11324230'].iloc[1]
lab_par_55yo_over_change = ((lab_par_55yo_over_today / lab_par_55yo_over_last) -1) *100
lab_par_55yo_over_change = str(round(lab_par_55yo_over_change, 2)) + ' %'
# Unemployment Rate - High School Graduates, No College
unemployment_highschool_graduates_no_college = pd.read_csv('employment_metrics/LNS14027660.csv')
unemployment_highschool_graduates_no_college = unemployment_highschool_graduates_no_college.sort_values('DATE', ascending=False)
unemployment_highschool_graduates_no_college['DATE'] = unemployment_highschool_graduates_no_college['DATE'].astype('datetime64[ns]').dt.date
unemployment_highschool_graduates_no_college_today = unemployment_highschool_graduates_no_college['LNS14027660'].iloc[0]
unemployment_highschool_graduates_no_college_last = unemployment_highschool_graduates_no_college['LNS14027660'].iloc[1]
unemployment_highschool_graduates_no_college_change = ((unemployment_highschool_graduates_no_college_today / unemployment_highschool_graduates_no_college_last) -1) *100
unemployment_highschool_graduates_no_college_change = str(round(unemployment_highschool_graduates_no_college_change, 2)) + ' %'
#

col1, col2, col3 = st.columns(3)
col1.metric('Unemployment Rate',ur_today, ur_change)
col2.metric('Labor Force Participation',lab_par_today, lab_par_change)
col3.metric('Unemployment - No College',unemployment_highschool_graduates_no_college_today, unemployment_highschool_graduates_no_college_change)

fig = px.line(ur, x="DATE", y="UNRATE", title='Unemployment Rate')
st.plotly_chart(fig, use_container_width=False)

fig = px.line(lab_par, x="DATE", y="CIVPART", title='Labor Force Participation')
st.plotly_chart(fig, use_container_width=False)

fig = px.line(unemployment_highschool_graduates_no_college, x="DATE", y="LNS14027660", title='Unemployment - No College')
st.plotly_chart(fig, use_container_width=False)

# ------------------------------- Inflation ------------------------------- #
st.header('Inflation Metrics')
# Load inflation data
cpi = pd.read_csv('inflation_metrics/MEDCPIM158SFRBCLE.csv')
cpi = cpi.sort_values('DATE', ascending=False)
cpi['DATE'] = cpi['DATE'].astype('datetime64[ns]').dt.date
cpi_today = cpi['MEDCPIM158SFRBCLE'].iloc[0].round(2)
cpi_last = cpi['MEDCPIM158SFRBCLE'].iloc[1]
cpi_change = ((cpi_today / cpi_last) -1) *100
cpi_change = str(round(cpi_change, 2)) + ' %'

oil = pd.read_csv('inflation_metrics/DCOILWTICO.csv')
oil = oil.sort_values('DATE', ascending=False)
oil['DATE'] = oil['DATE'].astype('datetime64[ns]').dt.date
oil_today = oil['DCOILWTICO'].iloc[0].round(2)
oil_last = oil['DCOILWTICO'].iloc[1]
oil_change = ((oil_today / oil_last) -1) *100
oil_change = str(round(oil_change, 2)) + ' %'

core_cpi = pd.read_csv('inflation_metrics/CORESTICKM159SFRBATL.csv')
core_cpi = core_cpi.sort_values('DATE', ascending=False)
core_cpi['DATE'] = core_cpi['DATE'].astype('datetime64[ns]').dt.date
core_cpi_today = core_cpi['CORESTICKM159SFRBATL'].iloc[0].round(2)
core_cpi_last = core_cpi['CORESTICKM159SFRBATL'].iloc[1]
core_cpi_change = ((core_cpi_today / core_cpi_last) -1) *100
core_cpi_change = str(round(core_cpi_change, 2)) + ' %'

gas = pd.read_csv('inflation_metrics/GASREGW.csv')
gas = gas.sort_values('DATE', ascending=False)
gas['DATE'] = gas['DATE'].astype('datetime64[ns]').dt.date
gas_today = gas['GASREGW'].iloc[0].round(2)
gas_last = gas['GASREGW'].iloc[1]
gas_change = ((gas_today / gas_last) -1) *100
gas_change = str(round(gas_change, 2)) + ' %'


col1,col2, col3 = st.columns(3)
col1.metric('Gas Prices ($)', gas_today, gas_change)
col2.metric('Core CPI (%)', core_cpi_today, core_cpi_change)
col3.metric('Median CPI (%)', cpi_today, cpi_change)

# Chart the inflation metrics
fig = px.line(gas, x="DATE", y="GASREGW", title='Gas Prices ($)')
st.plotly_chart(fig, use_container_width=False)
fig = px.line(core_cpi, x="DATE", y="CORESTICKM159SFRBATL", title='Core CPI (%)')
st.plotly_chart(fig, use_container_width=False)
fig = px.line(cpi, x="DATE", y="MEDCPIM158SFRBCLE", title='Median CPI (%)')
st.plotly_chart(fig, use_container_width=False)

st.header('Breakeven 5-year Inflation')
st.write('What the market thinks 5-year inflation will be')

breakeven = pd.read_csv('inflation_metrics/T5YIE.csv')
breakeven = breakeven.sort_values('DATE', ascending=False)
breakeven['DATE'] = breakeven['DATE'].astype('datetime64[ns]').dt.date
breakeven_today = breakeven['T5YIE'].iloc[0].round(2)
breakeven_last = breakeven['T5YIE'].iloc[1]
breakeven_change = ((breakeven_today / breakeven_last) -1) *100
breakeven_change = str(round(breakeven_change, 2)) + ' %'

st.metric('', breakeven_today, breakeven_change)
fig = px.line(breakeven, x="DATE", y="T5YIE", title='Breakeven 5-year Inflation')
st.plotly_chart(fig, use_container_width=True)

st.header('Fed Long-Term Funds Rate')
st.write('In my personal opinion, this number is the most important number when considering future stock market returns.')
longterm = pd.read_csv('FEDTARMDLR.csv')
longterm = longterm.sort_values('DATE', ascending=False)
longterm['DATE'] = longterm['DATE'].astype('datetime64[ns]').dt.date
longterm_today = longterm['FEDTARMDLR'].iloc[0].round(2)
longterm_last = longterm['FEDTARMDLR'].iloc[1]
longterm_change = ((longterm_today / longterm_last) -1) *100
longterm_change = str(round(longterm_change, 2)) + ' %'
st.metric('', longterm_today, longterm_change)
fig = px.line(longterm, x="DATE", y="FEDTARMDLR", title='Fed Long-Term Funds Rate')
st.plotly_chart(fig, use_container_width=True)

