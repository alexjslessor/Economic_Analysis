import pandas as pd
import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.models import LinearAxis, Range1d, HoverTool
import matplotlib.pyplot as plt
from matplotlib import style
style.use(['bmh','ggplot'])

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

'''Format time series datasets with pandas.'''
df1['Date'] = pd.date_range(start='1976-12-31', end='2015-12-31', freq='A')
df1.set_index('Date', inplace=True)
# print(df1.head())

df2['Date'] = pd.date_range(start='1976-12-31', end='2015-12-31', freq='A')
df2['govtransferamount'] = df2['gtranspopamountx1k'] * 1000
df2 = df2.drop(['gtranspopamountx1k'], 1)
df2['retirementpopulation'] = df2['retpopamountx1k'] * 1000
df2 = df2.drop(['retpopamountx1k'], 1)
df2.set_index('Date', inplace=True)
# print(df2.head())

df3['Date'] = pd.date_range(start='1976-12-31', end='2015-12-31', freq='A')
# Feature engineer new columns according to statscan methodology
df3['population_with_investments'] = df3['invpopamountx1k'] * 1000
df3 = df3.drop(['invpopamountx1k'], 1)
df3['population_receiving_govtransfers'] = df3['gtranspopamountx1k'] * 1000
df3 = df3.drop(['gtranspopamountx1k'], 1)
df3.set_index('Date', inplace=True)
# print(df3.head())

df4['Date'] = pd.date_range(start='1979-01-01', end='2017-11-01', freq='MS')
df4.set_index('Date', inplace=True)
df4 = df4.resample('A').mean()
df4 = df4.fillna(0)
# print(df4.head(), df4.tail(), df4.info())

df5['Date'] = pd.date_range(start='1974-12-31', end='2016-12-31', freq='A')
df5.set_index('Date', inplace=True)
# print(df5.head(), df5.tail(), df5.info())

df6['Date'] = pd.date_range(start='1971-12-31', end='2017-12-31', freq='A')
df6.set_index('Date', inplace=True)
# print(df6.head(), df6.tail(), df6.info())


df7['Date'] = pd.date_range(start='1944-01-01', end='2017-04-01', freq='MS')
df7.set_index('Date', inplace=True)
df7 = df7.resample('A').mean()
# print(df7.head(), df7.tail(), df7.info())


df = df7.merge(df1, how='left', left_index=True, right_index=True)
df = df.merge(df2, how='left', left_index=True, right_index=True)
df = df.merge(df3, how='left', left_index=True, right_index=True)
df = df.merge(df4, how='left', left_index=True, right_index=True)
df = df.merge(df5, how='left', left_index=True, right_index=True)
df = df.merge(df6, how='left', left_index=True, right_index=True)	
# df.to_csv('merged_dataframes.csv')

''' Exploratory Data Analysis using bokeh for visualization '''

df = pd.read_csv('merged_dataframes.csv', parse_dates=True)
# df = df.fillna(0)
df['Date'] = pd.to_datetime(df['Date'])

# df.drop(df.index[[1,20]
# oap = df.pop('Ontario_Avg_Price')
# oap.dropna(inplace=True)
# date = pd.date_range(start='1944-12-31', end='2017-12-31', freq='A')

date = df['Date']

p1 = figure(x_axis_type='datetime', title='Average House Prices to Income', y_range=(0, 500000), toolbar_sticky=False)
p1.grid.grid_line_alpha = 1.0
p1.xaxis.axis_label = '1974 - 2016'
p1.yaxis.axis_label = 'Price in 100s of Thousands'

p1.line(date, df['Ontario_Avg_Price'], line_width=3, color='#A6CEE3', legend='Ontario Average Home Price')
p1.circle(date, df['Ontario_Avg_Price'], fill_color='#A6CEE3', size=8)

p1.line(date, df['avgtotalincome'], line_width=3, color='#B2DF8A', legend='Average Income')
p1.circle(date, df['avgtotalincome'], fill_color='#B2DF8A', size=8)

p1.extra_y_ranges = {'Rate':Range1d(start=0, end=40)}
p1.add_layout(LinearAxis(y_range_name='Rate', axis_label='BoC Rate'), 'right')

p1.line(date, df['Rate'], line_width=3, y_range_name='Rate', color='#FB9A99', legend='BoC Rate')
p1.circle(date, df['Rate'], y_range_name='Rate', fill_color='#FB9A99', size=8)
p1.legend.location = 'top_left'

output_file('pricetoincome.html', title='costofliving')
show(p1)




