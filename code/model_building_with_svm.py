
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from sklearn import svm
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')


# In[22]:


def Build_Data_Set(features = ['DE Ratio',
                               'Trailing P/E']):
    data_df = pd.DataFrame.from_csv('/Users/avikalchhetri/Desktop/DAT210x/stocks_analyser/key_stats.csv')
    #data_df = data_df[:100] #for testing a fewer rows
    X = np.array(data_df[features].values)
    y = (data_df['Status']
        .replace('underperform',0)
        .replace('outperform',1)
        .values.tolist()) #Status has two values i.e underperform and outperform. This needs to be converted to
                            # numbers
    return X,y

def Analysis():
    X, y = Build_Data_Set()
    clf = svm.SVC(kernel='linear', C=1.0)
    clf.fit(X,y)
    
    #Following is for only graphing purposes
    w = clf.coef_[0]
    a = -w[0]/w[1]
    xx = np.linspace(min(X[:,0]),max(X[:,0]))
    yy = a * xx - clf.intercept_[0] / w[1]
    h0 = plt.plot(xx, yy, 'k-', label = 'non-weighted')
    plt.scatter(X[:,0], X[:,1], c = y)
    plt.ylabel('Trailing PE Ratio')
    plt.xlabel('BE Ratio')
    plt.legend()
    plt.show()


# In[23]:


Analysis()

