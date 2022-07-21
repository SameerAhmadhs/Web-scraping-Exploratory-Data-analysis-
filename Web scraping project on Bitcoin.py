#!/usr/bin/env python
# coding: utf-8

# # Web scraping project

# ## Bitcoin last 10 year history

# In[1]:


#import the liberarys
import numpy as np
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from pandas import DataFrame

import warnings
warnings.filterwarnings('ignore')

# choose a style option
plt.style.use('bmh')
# sns.set_style('darkgrid')


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'


# ### Create date for website formate

# In[3]:


# Create a list of date from 5may2013 to 6june2022
date = pd.date_range('2013-05-05','2022-06-06',freq = '7D') 

# cleaning date as formated in website
dates = []
for a in date:
    dates.append(str(a).split()[0].replace('-','').replace("'",''))
intdate = []

for i in dates:
    intdate.append(int(i))
    
intdate
    


# In[4]:


#Extracting Data from coinmarketcap website

#blank list
name = []
symbol = []
marketcap = []
price = []
cir_supply = []
chang_1h = []
chang_24h = []
chang_7d = []
dates = []

for i in intdate:
    
    starttime = time.time()
    URL = 'https://coinmarketcap.com/historical/{}/'.format(str(i))
    response = requests.get(URL)
    soup  = BeautifulSoup(response.content,'html.parser')
    
    result = soup.find('tr',attrs={'class':'cmc-table-row'}).get_text().strip()
    
    
        
    #name
    Name = soup.find('a',attrs={'class':'cmc-table__column-name--name cmc-link'}).get_text().strip()
    name.append(Name)

    #symbol
    syb = soup.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__symbol'}).get_text().strip()
    symbol.append(syb)

    #marketcap
    markcap = soup.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap'}).get_text().strip()
    marketcap.append(markcap)
    
    #prie
    price_s = soup.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price'}).get_text().strip()
    price.append(price_s)
    
    #circularsupply
    circursuply = soup.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply'}).get_text().strip()
    cir_supply.append(circursuply)
    
    #1hour change
    chg_1h = soup.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-1-h'}).get_text().strip()
    chang_1h.append(chg_1h)
    
    #24hour change
    chg_24h = soup.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-1-h'}).get_text().strip()
    chang_24h.append(chg_24h)
    
    #7day change
    chg_7d = soup.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-7-d'}).get_text().strip()
    chang_7d.append(chg_7d)
    
    dates.append(i)
    
    endtime = time.time()
    
    print('Extract date {} completed in {} seconds'.format(i, endtime-starttime))
    

    
    

    
    



# In[12]:


#After extracting data from coinmarketcap website then creat datafram 
bitcoin_df = pd.DataFrame({'Name':name,'Symbol':symbol,'Marketcap_in_dollar':marketcap,'Price_in_dollar':price,
                          'Circulating_supply_in_BTC':cir_supply,'1hour_chg_per':chang_1h,'24hour_chg_per':chang_24h,
                          '7day_chg_per':chang_7d,'Date':dates})


# In[13]:


#upload to excel 
bitcoin_df.to_excel(r'C:\Data\Bitcoin_10y.xlsx')


# In[14]:


#Read file
bitcoin_df = pd.read_excel(r'C:\Data\Bitcoin_10y.xlsx')


# In[15]:


bitcoin_df  #Raw DataFrame


# ## Data cleaning

# In[16]:


bitcoin_df['Price_in_dollar']=bitcoin_df.Price_in_dollar.str.replace('$','').str.replace(',','').astype(float)
bitcoin_df['Marketcap_in_dollar']=bitcoin_df.Marketcap_in_dollar.str.replace('$','').str.replace(',','').astype(float)
bitcoin_df['1hour_chg_per']=bitcoin_df['1hour_chg_per'].str.replace('%','').str.replace(',','').astype(float)
bitcoin_df['24hour_chg_per']=bitcoin_df['24hour_chg_per'].str.replace('%','').str.replace(',','').astype(float)
bitcoin_df['7day_chg_per']=bitcoin_df['7day_chg_per'].str.replace('%','').str.replace(',','').astype(float)
bitcoin_df['Circulating_supply_in_BTC']=bitcoin_df['Circulating_supply_in_BTC'].str.replace('BTC','').str.replace(',','').astype(float)



# #### Challenges 
# 1. we have remove symboles like '$' and '%'.
# 2. we have remove commas and some unrelevent thing in datafram.
# 3. After removing all the things from data then converted types of data into float or integer.

# ## 1. Check for duplicate rows

# In[17]:


bitcoin_df.duplicated()
bitcoin_df.duplicated().value_counts()

#NO Duplicates found


# ## 2.Handling missing values

# In[18]:


bitcoin_df.isna().sum() 


# no missing values found

# In[19]:


bitcoin_df.info()


# In[21]:


#removeing unusable colums
bitcoin_df.drop(['Unnamed: 0'],axis=1,inplace=True)


# In[42]:


#storing cleaned data into excel file 
bitcoin1 = pd.read_csv(r'C:\Data\bitcoin_clean_data.csv')


# In[44]:


bitcoin1


# In[45]:


bitcoin1.info()


# In[46]:


bitcoin1.columns


# In[47]:


bitcoin1


# In[48]:


# converting date column into datetype
bitcoin1['Date'] = pd.to_datetime(bitcoin1['Date'],format='%Y%m%d')


# In[ ]:


#shifting date column to first position
first_colm = bitcoin1.pop('Date')
bitcoin1.insert(0,'Date',first_colm)
bitcoin1.drop('Unnamed: 0',axis=1,inplace=True)

# suppress scientific notation in datafram for marketcap
pd.options.display.float_format = '{:.2f}'.format


# In[58]:


bitcoin1.info() #After cleaning data the info of dataframe is looking like....


# In[59]:


#After shifting date colum and suppress scientific notation, stored the data to csv file
bitcoin1.to_csv(r'C:\Data\BITCOIN_TOTAL_CLEAN.csv')


# In[60]:


bitcoin = pd.read_csv(r'C:\Data\BITCOIN_TOTAL_CLEAN.csv')
bitcoin.head()


# In[68]:


bitcoin1.describe() #Describing all the numerical column
bitcoin1.head()
bitcoin1.tail()


# # Data visualization 
# ## Univariate Analysis

# ### 1) Line chart

# In[63]:


# ploting line chart x=Date and y=price
plt.figure(figsize=(10,5))

plt.plot(bitcoin1.Date,bitcoin1.Price_in_dollar,color = '#008000')
plt.title('Price History of Bitcoin(2013-2022)',color='g')
plt.xlabel('Date')
plt.ylabel('Price(in Dollar)')

plt.show();


# In[65]:


# Line chart for 7day change percent in price of bitcoin.
plt.figure(figsize=(15,6), dpi = 100)

plt.plot(bitcoin1.Date,bitcoin1['7day_chg_per'])
plt.title('Percent Change in 7 Days(Bitcoin)',color='b')
plt.xlabel('Date')
plt.ylabel('7 Days Change(in Percent)')
  
plt.show();


# ### 2). Histogram

# In[28]:


## Distribution plot 
#1. Histogram

plt.figure(figsize=(12,5))
plt.hist(bitcoin.Price_in_dollar,edgecolor = 'black',color = 'green',bins =7 ,label='BITCOIN')
plt.title('Total count of price',color='g')
plt.xlabel('Price(In Dollar )')
plt.ylabel('count');


# ### 3). Box plot

# In[23]:


c = 'green'
plt.boxplot(bitcoin.Price_in_dollar, patch_artist = True,
           boxprops=dict(facecolor=c, color=c),
            capprops=dict(color=c),
            whiskerprops=dict(color=c),
            flierprops=dict(color=c, markeredgecolor=c),
            medianprops=dict(color='r'))
plt.title('Box plot(Price of Bitcoin)',color='g')
plt.ylabel('Price(In Dollar)');


# ### 4).Distribution plot

# In[29]:


#4 Distribution plot
plt.figure(figsize=(12,4))
sns.displot(data=bitcoin,x=bitcoin.Price_in_dollar,height=5,aspect=13/5,color='red',kde = True);


# # Bivariate Analysis

# In[25]:


#for getting index no of date of first wave and second wave of covid
print(list(enumerate(bitcoin.Date))) 
# starting date of first wave in world index=380, Timestamp('2020-08-16)
# ending date of first wave in world index=402, Timestamp('2021-01-17)


# starting date of second wave in world index=409, Timestamp('2021-03-07
# ending date of second wave in world index=425, Timestamp('2021-06-27)


# ## 1.Multi Line chart

# In[86]:


#by using index we extracted the data of that date 
first_wave = bitcoin1.loc[378:404]
second_wave = bitcoin1.loc[408:426]


# In[87]:


#first wave of covid datafram
first_wave
#second wave of covid datafram
second_wave


# # 1) Price of bitcoin at the time of first wave and second wave of covid.

# In[88]:


plt.figure(figsize=(15,6),dpi=100)
plt.plot(first_wave.Date,first_wave.Price_in_dollar,label='First wave of covid-19',color = 'b',ls='-',lw=3,marker='.',markersize=15)
plt.plot(second_wave.Date,second_wave.Price_in_dollar,label='Second wave of covid-19',color = 'orange',ls='-',lw=3,marker='.',markersize=15)

plt.title('Bitcoin price at the time of First and Second wave of covid',fontsize=20,color='b')
plt.xlabel('Date')
plt.ylabel('Price(in dollar)')
plt.legend(loc='upper left');


# ## 2. Area chart

# In[39]:


plt.figure(figsize=(15,7),dpi=100)
plt.stackplot(first_wave.Date,first_wave.Price_in_dollar)
plt.stackplot(second_wave.Date,second_wave.Price_in_dollar);


# ## 3) Scatter plot

# In[60]:


plt.figure(figsize=(10,6),dpi=100)
plt.scatter(bitcoin.Date,bitcoin.Price_in_dollar,color='b');


# In[8]:


threedee = plt.figure().gca(projection='3d')
threedee.scatter(bitcoin_df['Circulating_supply_in_BTC'], bitcoin_df['Price_in_dollar'], bitcoin_df['Marketcap_in_dollar'])
threedee.set_xlabel('Index')
threedee.set_ylabel('H-L')
threedee.set_zlabel('Close')
plt.show()


# In[12]:


bitcoindf = pd.read_csv(r'C:\Data\BITCOIN_TOTAL_CLEAN.csv')


# In[13]:


bitcoindf = bitcoindf.drop('Unnamed: 0',axis=1)


# In[16]:


bitcoin_df


# ## 4) Heat map

# In[34]:


correlation = bitcoin.corr()


# In[35]:


plt.figure(figsize=(8,4),dpi=100)
sns.heatmap(correlation,cmap='winter',annot=True);


# ### converting numerical to categorical

# In[89]:


bitcoin1.head()


# In[90]:


bitcoin1.info()


# In[91]:


pd.cut(bitcoin1.Date,bins=10) #making 10 groups of date columns(yearly) 


# In[97]:


# giving name to each group like 2013,2014......
bin_names=['2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']
pd.cut(bitcoin1.Date,bins=10,labels=bin_names)
bitcoin1['Year']=pd.cut(bitcoin1.Date,bins=10,labels=bin_names)


# In[108]:


bitcoin1.info()
bitcoin1.to_csv(r'C:\Data\bitcoin_add_year.csv')


# In[99]:


bitcoin1.Year.value_counts().plot(kind='bar');


# ## 3).Multivariate Visualization

# In[110]:


# After converting numerical to categorical column we have used cat plot
plt.figure(dpi=200,figsize=(20,20))

sns.catplot(data=bitcoin1,x='Year',y='Price_in_dollar',kind='box');


# In[112]:


# count plot()
bitcoin1.Year.count()
bitcoin1.Year.value_counts()


# In[113]:


sns.countplot(data = bitcoin1, x = 'Year');


# ## Pairplot

# In[114]:


plt.figure(dpi = 200)
sns.pairplot(bitcoin1);


# ## subplot

# In[58]:


plt.figure(dpi=200,figsize=(20,20))

plt.subplot(221)
sns.heatmap(bitcoin.corr(),cmap='winter',annot=True)
plt.title('Heat Map')

plt.subplot(222)
sns.boxplot(data=bitcoin,x='year',y='Circulating_supply_in_BTC')
plt.title('Box plot')

plt.subplot(223)
sns.barplot(data=bitcoin,x='year',y='7day_chg_per')
plt.title('Bar plot')

plt.subplot(224)
sns.scatterplot(data=bitcoin,x='year',y='Price_in_dollar')
plt.title('catplot');

