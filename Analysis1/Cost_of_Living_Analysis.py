import pandas as pd
import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.models import LinearAxis, Range1d, HoverTool
import matplotlib.pyplot as plt
from matplotlib import style
style.use(['bmh','ggplot'])
''' Import csv files. '''
df1 = pd.read_csv('206-0011-nonfam2015.csv')
# print(df1.head(), df1.info())

df2 = pd.read_csv('206-0021-fam2015.csv')
# print(df2.head(), df2.info())

df3 = pd.read_csv('206-0021-nonfam2015.csv')
# print(df3.head(), df3.info())

df4 = pd.read_csv('avgretprices_for_gas_more_complete.csv', encoding='cp863')
# print(df4.head(), df4.info())

df5 = pd.read_csv('houseprices.csv')
# print(df5.head(), df5.info())

df6 = pd.read_csv('population.csv')
# print(df6.head(), df6.info())

df7 = pd.read_csv('rate.csv', parse_dates=True)
# print(df6.head(), df6.info())

'''Format dataframes for time series analysis.'''
df1['Date'] = pd.date_range(start='1976-12-31', end='2015-12-31', freq='A')
df1.set_index('Date', inplace=True)
# print(df1.head(), df1.info())

df2['Date'] = pd.date_range(start='1976-12-31', end='2015-12-31', freq='A')
df2.set_index('Date', inplace=True)
# print(df2.head(), df2.info())

df3['Date'] = pd.date_range(start='1976-12-31', end='2015-12-31', freq='A')
df3.set_index('Date', inplace=True)
# print(df3.head(), df3.info())

df4['Date'] = pd.date_range(start='1979-01-01', end='2017-11-01', freq='MS')
df4.set_index('Date', inplace=True)
df4 = df4.resample('A').mean()
df4 = df4.fillna(0)
# print(df4.head(), df4.info())

df5['Date'] = pd.date_range(start='1974-12-31', end='2016-12-31', freq='A')
df5.set_index('Date', inplace=True)
# print(df5.head(), df5.info())

df6['Date'] = pd.date_range(start='1971-12-31', end='2017-12-31', freq='A')
df6.set_index('Date', inplace=True)
# print(df6.head(), df6.info())

df7['Date'] = pd.date_range(start='1944-01-01', end='2017-04-01', freq='MS')
df7.set_index('Date', inplace=True)
df7 = df7.resample('A').mean()
# print(df7.head(), df7.info())

''' Merge all dataframes into largest datetimeindex, Rate and create new csv file. '''
df = df7.merge(df1, how='left', left_index=True, right_index=True)
df = df.merge(df2, how='left', left_index=True, right_index=True)
df = df.merge(df3, how='left', left_index=True, right_index=True)
df = df.merge(df4, how='left', left_index=True, right_index=True)
df = df.merge(df5, how='left', left_index=True, right_index=True)
df = df.merge(df6, how='left', left_index=True, right_index=True)	
# df.to_csv('merged_dataframes.csv')

''' Read in new csv file merged_dataframes.csv. '''
df = pd.read_csv('merged_dataframes.csv', parse_dates=True)
df['Date'] = pd.to_datetime(df['Date'])
date = df['Date']

''' Feature engineer new columns '''
df['Average_Income'] = (df['avgtotalincome'] + df['averageincome_y']) / 2

df['Fuel_Cost_Average'] = (df['stjohngas'] + df['StJohns_Heating_Fuel'] + df['Charlottetown_Summerside_Regular_Gas'] +\
		df['Charlottetown_Summerside_Heating_Fuel'] + df['Halifax_Regular_Gas'] + df['Halifax_Heating_Fuel'] + df['Saint_John_Regular_Gas'] +\
		df['Saint_John_Heating_Fuel'] + df['Quibec_Regular_Gas'] + df['Quibec_Heating_Fuel'] + df['Montreal_Regular_Gas'] + df['Montreal_Heating_Fuel'] +\
		df['Ottawa_Gatineau_Regular_Gas'] + df['Ottawa_Gatineau_Heating_Fuel'] + df['Toronto_Regular_Gas'] + df['Toronto_Heating_Fuel'] +\
		df['Thunder_Bay_Regular_Gas'] + df['Thunder_Bay_Heating_Fuel'] + df['Winnipeg_Regular_Gas'] + df['Winnipeg_Heating_Fuel'] + df['Regina_Regular_Gas'] +\
		df['Regina_Heating_Fuel'] + df['Saskatoon_Regular_Gas'] + df['Saskatoon_Heating_Fuel'] + df['Edmonton_Regular_Gas'] +\
		df['Calgary_Regular_Gas'] + df['Vancouver_Regular_Gas'] + df['Vancouver_Heating_Fuel'] + df['Victoria_Regular_Gas'] +\
		df['Victoria_Regular_Gas.1'] + df['Victoria_Diesel_Fuel'] + df['Victoria_Heating_Fuel']) / 32

''' Drop feature engineered source columns '''
df = df.drop(['stjohngas', 'StJohns_Heating_Fuel', 'Charlottetown_Summerside_Regular_Gas',\
       'Charlottetown_Summerside_Heating_Fuel', 'Halifax_Regular_Gas',\
       'Halifax_Heating_Fuel', 'Saint_John_Regular_Gas',\
       'Saint_John_Heating_Fuel', 'Quibec_Regular_Gas',\
       'Quibec_Heating_Fuel', 'Montreal_Regular_Gas',\
       'Montreal_Heating_Fuel', 'Ottawa_Gatineau_Regular_Gas',\
       'Ottawa_Gatineau_Heating_Fuel', 'Toronto_Regular_Gas',\
       'Toronto_Heating_Fuel', 'Thunder_Bay_Regular_Gas',\
       'Thunder_Bay_Heating_Fuel', 'Winnipeg_Regular_Gas',\
       'Winnipeg_Heating_Fuel', 'Regina_Regular_Gas',\
       'Regina_Heating_Fuel', 'Saskatoon_Regular_Gas',\
       'Saskatoon_Heating_Fuel', 'Edmonton_Regular_Gas',\
       'Calgary_Regular_Gas', 'Vancouver_Regular_Gas',\
       'Vancouver_Heating_Fuel', 'Victoria_Regular_Gas',\
       'Victoria_Regular_Gas.1', 'Victoria_Diesel_Fuel',\
       'Victoria_Heating_Fuel', 'avgtotalincome',\
       'averageincome_y', 'population_receiving_govtransfers',\
       'medianincome.1', 'gtransavgincome_y',\
       'gtransmedincome_y'], 1)
# print(df.info())

''' Rename columns with descriptive labels '''
df = df.rename(columns={'averageincome_x':'Family_Average_Income', 'medianincome':'Family_Median_Income', 'inv_avg_income':'Family_Average_Investment_Income',\
		'inv_med_income':'Family_Median_Investment_Income', 'ret_avg_income':'Family_Retirement_Average_Income', 'ret_med_income':'Family_Retirement_Median_Income',\
		'gtransavingincome_x':'Family_avgIncome_Receiving_Transfer_Payments', 'gtransmedincome_x':'Family_medIncome_Receiving_Transfer_Payments',\
		'avggovtransfer':'Individual_avgIncome_Receiving_Transfer_Payments', 'medtotalincome':'Individual_Median_Income',\
		'avgtotalincometax':'Individual_Average_Income_Tax', 'medtotalincometax':'Individual_Median_Income_Tax', 'avgaftertaxincome':'Individual_Avg_After_Tax_Income',\
		'medaftertaxincome':'Individual_Med_After_Tax_Income', 'gtransavgincome_x':'Family_avgIncome_Receiving_Transfer_Payments',\
		'govtransferamount':'Population_Receiving_Gov_Transfers', 'retirementpopulation':'Retirement_Aged_Population_Size', 'inv_avg_income.1':'Individual_Avg_Retirement_Investment_Income',\
		'inv_med_income.1':'Individual_Med_Retirement_Investment_Income', 'ret_Avg_income':'Individual_Avg_Retirement_Income', 'ret_Med_income':'Individual_Med_Retirement_Income',\
		'population_with_investments':'Population_Size_with_Investments'})
print(df.info())

''' EDA with bokeh and matplotlib '''
p1 = figure(x_axis_type='datetime', title='Ontario Average House Prices to Income', y_range=(0, 500000), toolbar_sticky=False)
p1.title.text_color = 'black'
p1.title.text_font = 'times'
p1.title.text_font_style = 'bold'
p1.grid.grid_line_alpha = 1.0
p1.xaxis.axis_label = '1944 - 2017'
p1.yaxis.axis_label = 'Price in 100\'s of Thousands'

p1.line(date, df['Ontario_Avg_Price'], line_width=3, color='#A6CEE3', legend='Ontario Average Home Price')
p1.circle(date, df['Ontario_Avg_Price'], fill_color='#A6CEE3', size=8)

p1.line(date, df['Individual_Median_Income'], line_width=3, color='#B2DF8A', legend='Individual Median Income')
p1.circle(date, df['Individual_Median_Income'], fill_color='#B2DF8A', size=8)

p1.extra_y_ranges = {'Rate':Range1d(start=0, end=40)}
p1.add_layout(LinearAxis(y_range_name='Rate', axis_label='BoC Rate'), 'right')

p1.line(date, df['Rate'], line_width=3, y_range_name='Rate', color='#FB9A99', legend='BoC Rate')
p1.circle(date, df['Rate'], y_range_name='Rate', fill_color='#FB9A99', size=8)
p1.legend.location = 'top_left'
output_file('pricetoincome.html', title='costofliving')
show(p1)

p2 = figure(x_axis_type='datetime', title='Ontario Average House Prices to Income', y_range=(0, 2500000), toolbar_sticky=False)
p2.title.text_color = 'black'
p2.title.text_font = 'times'
p2.title.text_font_style = 'bold'
p2.grid.grid_line_alpha = 1.0
p2.xaxis.axis_label = '1944 - 2017'
p2.yaxis.axis_label = 'Price in 100\'s of Thousands'

p2.line(date, df['Retirement_Aged_Population_Size'], line_width=3, color='#A6CEE3', legend='Retirement Aged Population Size')
p2.circle(date, df['Retirement_Aged_Population_Size'], fill_color='#A6CEE3', size=8)

p2.line(date, df['GTA_Avg_Price'], line_width=3, color='#B2DF8A', legend='GTA Average Home Price')
p2.circle(date, df['GTA_Avg_Price'], fill_color='#B2DF8A', size=8)

p2.extra_y_ranges = {'Rate':Range1d(start=0, end=40)}
p2.add_layout(LinearAxis(y_range_name='Rate', axis_label='BoC Rate'), 'right')

p2.line(date, df['Rate'], line_width=3, y_range_name='Rate', color='#FB9A99', legend='BoC Rate')
p2.circle(date, df['Rate'], y_range_name='Rate', fill_color='#FB9A99', size=8)
p2.legend.location = 'top_left'
output_file('other.html', title='other')
show(p2)






