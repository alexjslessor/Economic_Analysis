import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use(['bmh','ggplot'])

df1 = pd.read_csv('206-0011-nonfam2015.csv')
# print(df1.head(), df1.info())

df2 = pd.read_csv('206-0021-fam2015.csv')
# print(df2.head(), df2.info())

df3 = pd.read_csv('206-0021-nonfam2015.csv')
# print(df3.head(), df3.info())

# df4 = pd.read_csv('avgretprices_for_gas_more_complete.csv')
# print(df4.head(), df4.info())

df5 = pd.read_csv('houseprices.csv')
# print(df5.head(), df5.info())

df6 = pd.read_csv('population.csv')
# print(df6.head(), df6.info())

df6 = pd.read_csv('rate.csv')
# print(df6.head(), df6.info())

'''Format time series datasets with pandas.'''
df1['Date'] = pd.date_range(start='1976-12-31', end='2015-12-31', freq='A')
# print(df1.head(),df1.tail(), df1.info())

df2['Date'] = pd.date_range(start='1976-12-31', end='2015-12-31', freq='A')
df2['govtransferamount'] = df2['gtranspopamountx1k'] * 1000
df2 = df2.drop(['gtranspopamountx1k'], 1)
df2['retirementpopulation'] = df2['retpopamountx1k'] * 1000
df2 = df2.drop(['retpopamountx1k'], 1)
print(df2.head(),df2.tail(), df2.info())


