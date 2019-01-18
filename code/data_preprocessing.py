
# coding: utf-8

# In[3]:


import pandas as pd
import os
import time
from datetime import datetime
from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use("dark_background")
import re


# In[4]:


path = '/Users/avikalchhetri/Desktop/DAT210x/stocks_analyser/intraQuarter/'


# In[25]:


# This function is to segerate source data and pick only the Stock a.k.a Company name along with respective
#Feature
def Key_Stats(gather=["Total Debt/Equity",
                      'Trailing P/E',
                      'Price/Sales',
                      'Price/Book',
                      'Profit Margin',
                      'Operating Margin',
                      'Return on Assets',
                      'Return on Equity',
                      'Revenue Per Share',
                      'Market Cap',
                      'Enterprise Value',
                      'Forward P/E',
                      'PEG Ratio',
                      'Enterprise Value/Revenue',
                      'Enterprise Value/EBITDA',
                      'Revenue',
                      'Gross Profit',
                      'EBITDA',
                      'Net Income Avl to Common ',
                      'Diluted EPS',
                      'Earnings Growth',
                      'Revenue Growth',
                      'Total Cash',
                      'Total Cash Per Share',
                      'Total Debt',
                      'Current Ratio',
                      'Book Value Per Share',
                      'Cash Flow',
                      'Beta',
                      'Held by Insiders',
                      'Held by Institutions',
                      'Shares Short (as of',
                      'Short Ratio',
                      'Short % of Float',
                      'Shares Short (prior month)']):
    
    statspath = path+'/_KeyStats/'
    stock_list = [x[0] for x in os.walk(statspath)]
    df = pd.DataFrame(columns = ['Date',
                                 'Unix',
                                 'Ticker',
                                 'Price',
                                 'stock_p_change',
                                 'SP500',
                                 'sp500_p_change',
                                 'Difference',
                                 ##############
                                 'Total Debt/Equity',
                                 'Trailing P/E',
                                 'Price/Sales',
                                 'Price/Book',
                                 'Profit Margin',
                                 'Operating Margin',
                                 'Return on Assets',
                                 'Return on Equity',
                                 'Revenue Per Share',
                                 'Market Cap',
                                 'Enterprise Value',
                                 'Forward P/E',
                                 'PEG Ratio',
                                 'Enterprise Value/Revenue',
                                 'Enterprise Value/EBITDA',
                                 'Revenue',
                                 'Gross Profit',
                                 'EBITDA',
                                 'Net Income Avl to Common ',
                                 'Diluted EPS',
                                 'Earnings Growth',
                                 'Revenue Growth',
                                 'Total Cash',
                                 'Total Cash Per Share',
                                 'Total Debt',
                                 'Current Ratio',
                                 'Book Value Per Share',
                                 'Cash Flow',
                                 'Beta',
                                 'Held by Insiders',
                                 'Held by Institutions',
                                 'Shares Short (as of',
                                 'Short Ratio',
                                 'Short % of Float',
                                 'Shares Short (prior month)',                                
                                 ##############
                                 'Status']) # 
                                    #Status is for measuring performance
    sp500_df = pd.DataFrame.from_csv('/Users/avikalchhetri/Desktop/DAT210x/stocks_analyser/MULTPL-SP500_DIV_YIELD_MONTH.csv')
    
    ticker_list = []
    
    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split('/')[-1] #ticker is stock name
        ticker_list.append(ticker)
        
        starting_stock_value = False #To calcuate % change in stock value, to be used in stock_p_change
        starting_sp500_value = False ##To calcuate % change in SP 500 value, to be used in sp500_p_change

        if len(each_file) > 0:
            for file in each_file:
                if (file.find('.html') != -1): #Only take timestamp for file with .html
                    date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                    unix_time = time.mktime(date_stamp.timetuple())
                    #print(date_stamp , unix_time)
                
                full_file_path = each_dir+'/'+file
                if (full_file_path.find('.html') != -1): #As full_file_path returns directory and file name, we only
                    #need the file name and hence filtering using .find('.html') to just find files
                    source = open(full_file_path,'r').read() #Returns the page source code
                    #Use try catch block to avoid "list index out of range" error.  the reason for that error is HTML markup elements 
                    #in different html files. so you need to handle multiple conditions while splitting markup data.
                    try:
                        #Spliting the page source code to extract the value of Total Debt/Equity (mrq) and storing 
                        #in value
                        value_list = []
                        for each_data in gather:
                            try:
                                #Below is the regex to handle the numeric values in the data
                                regex = re.escape(each_data) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>'
                                value = re.search(regex, source)
                                value = (value.group(1))
                                
                                if 'B' in value: #B is Billion
                                    value = float(value.replace('B',''))*1000000000
                                elif 'M' in Value: #M in Million
                                    value = float(value.replace('M',''))*1000000
                                    
                                value_list.append(value)
                                
                                #value = float(source.split(gather+'</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                            except Exception as e:
                                value = 'N/A'
                                value_list.append(value)
                                #The below except clause is to capture the data where the source code has a new line
                                # after </td>
                                    #try:
                                        #value = float(source.split(gather+'</td>\n<td class="yfnc_tabledata1">')[1].split('</td>')[0])
                                    #except Exception as e:
                                        #pass
                                    #print(str(e), ticker, file)
                                    #time.sleep(15)
                                    
                        try:
                            sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                            row = sp500_df[(sp500_df.index == sp500_date)]
                            sp500_value = float(row['Value'])
                        except:
                            #259200 is for covering past 3 days. As the data from Yahoo might contain data not
                            #available for weekends
                            sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
                            row = sp500_df[(sp500_df.index == sp500_date)]
                            sp500_value = float(row['Value'])
                        
                        try:
                            stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                        except Exception as e:
                            try:
                                stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                                stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
                                stock_price = float(stock_price.group(1))
                                #print(stock_price)
                                #sleep(10)
                            except Exception as e:
                                stock_price = (source.split('<span class = "time_rtq_ticker">')[1].split('</span>')[0])
                                stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
                                stock_price = float(stock_price.group(1))
                                print('Latest: ',stock_price)
                                
                        if not starting_stock_value:
                            starting_stock_value = stock_price
                        if not starting_sp500_value:
                            starting_sp500_value = sp500_value
                        
                        #Calculate the change in Stock price and SP 500 values
                        stock_p_change = ((stock_price - starting_stock_value)/starting_stock_value)*100
                        sp500_p_change  = ((sp500_value - starting_sp500_value)/starting_sp500_value)*100
                        difference = stock_p_change - sp500_p_change
                        
                        if difference > 0:
                            status = 'Outperform'
                        else:
                            status = 'Underperform'
                        
                        if value_list.count('N/A') > 10:
                            pass
                        else:
                            df = df.append({'Date':date_stamp,
                                            'Unix':unix_time,
                                            'Ticker':ticker,
                                            'Price':stock_price,
                                            'stock_p_change':stock_p_change,
                                            'SP500':sp500_value,
                                            'sp500_p_change':sp500_p_change,
                                            'Difference':difference,
                                            'Total Debt/Equity':value_list[0],
                                            #'Market Cap':value_list[1],
                                            'Trailing P/E':value_list[1],
                                            'Price/Sales':value_list[2],
                                            'Price/Book':value_list[3],
                                            'Profit Margin':value_list[4],
                                            'Operating Margin':value_list[5],
                                            'Return on Assets':value_list[6],
                                            'Return on Equity':value_list[7],
                                            'Revenue Per Share':value_list[8],
                                            'Market Cap':value_list[9],
                                            'Enterprise Value':value_list[10],
                                            'Forward P/E':value_list[11],
                                            'PEG Ratio':value_list[12],
                                            'Enterprise Value/Revenue':value_list[13],
                                            'Enterprise Value/EBITDA':value_list[14],
                                            'Revenue':value_list[15],
                                            'Gross Profit':value_list[16],
                                            'EBITDA':value_list[17],
                                            'Net Income Avl to Common ':value_list[18],
                                            'Diluted EPS':value_list[19],
                                            'Earnings Growth':value_list[20],
                                            'Revenue Growth':value_list[21],
                                            'Total Cash':value_list[22],
                                            'Total Cash Per Share':value_list[23],
                                            'Total Debt':value_list[24],
                                            'Current Ratio':value_list[25],
                                            'Book Value Per Share':value_list[26],
                                            'Cash Flow':value_list[27],
                                            'Beta':value_list[28],
                                            'Held by Insiders':value_list[29],
                                            'Held by Institutions':value_list[30],
                                            'Shares Short (as of':value_list[31],
                                            'Short Ratio':value_list[32],
                                            'Short % of Float':value_list[33],
                                            'Shares Short (prior month)':value_list[34],
                                            'Status':status},
                                           ignore_index=True)

                    except Exception as e:
                        pass
                        #print(str(e))
                        #value = float('nan')
                    #print(ticker+':',value)
                else:
                    break
                    
    #Plot Difference of stocks
    for each_ticker in ticker_list:
        try:
            plot_df = df[(df['Ticker'] == each_ticker)]
            plot_df = plot_df.set_index(['Date'])
            
            if plot_df['Status'][-1] == 'Underperform':
                color = 'r'
            else:
                color = 'g'
            plot_df['Difference'].plot(label = each_ticker, color = color)
            plt.legend()
        except:
            pass
    
    plt.show()
    df = df.to_csv('key_stats.csv')


# In[26]:


Key_Stats()

