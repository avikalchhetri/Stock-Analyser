
# coding: utf-8

# In[ ]:


import pandas as pd
import os
import quandl
import time

auth_tok = open('auth.txt','r').read()
path = '/intraQuarter/'

def Stock_Prices():
    df = pd.DataFrame()
    statspath = path+'/_KeyStats/'
    stocks_list = [x[0] for x in os.walk(statspath)]
    print(statspath)
    try:
        for each_dir in stocks_list[1:]:
            ticker = each_dir.split('/')[-1]
            name = 'WIKI/'+ticker.upper()
            print(name)
            data = quandl.get(name,trim_start = '2000-12-12',
                             trim_end = '2012-12-13',
                             authtoken = auth_tok)
            data[ticker.upper()] = data['Adj. Close']
            df = pd.concat([df,data[ticker.upper()]], axis = 1)
            
    except Exception as e:
        print(str(e))

    df.to_csv('stock_prices.csv')

