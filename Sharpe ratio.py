import ssl
from functools import wraps
def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar
ssl.wrap_socket = sslwrap(ssl.wrap_socket)
#Technique used to determine weights: Sharpe ratio
#Data source: Yahoo finance
#Monte Carlo simulations to assign random weights to the stocks and calculate volatility
#Start dateeis taken as Jan 1,2016

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt

#list of stocks in portfolio
stocks = ['ASHOKLEY.NS','GBTC','GC=F']
#requests.post(url, data=payload, headers=headers, verify=False) 
#download daily price data for each of the stocks in the portfolio
data = web.DataReader(stocks,data_source='yahoo',start='01/01/2016')['Adj Close']
 
#convert daily stock prices into daily returns
returns = data.pct_change()
 
#calculate mean daily return and covariance of daily returns
mean_daily_returns = returns.mean()
cov_matrix = returns.cov()
 
#set number of runs of random portfolio weights
num_portfolios = 3000
 
#set up array to hold results
#Array to hold weight for each stock
results = np.zeros((4+len(stocks)-1,num_portfolios))
 
for i in xrange(num_portfolios):
    #select random weights for portfolio holdings
    weights = np.array(np.random.random(3))
    #rebalance weights to sum to 1
    weights /= np.sum(weights)
 
    #calculate portfolio return and volatility(standard deviation)
    portfolio_return = np.sum(mean_daily_returns * weights) * 252
    portfolio_std_dev = np.sqrt(np.dot(weights.T,np.dot(cov_matrix, weights)))*np.sqrt(252)
 
    #store results in results array
    results[0,i] = portfolio_return
    results[1,i] = portfolio_std_dev
    #store Sharpe Ratio (return / volatility) - risk free rate element excluded for simplicity
    results[2,i] = ( results[0,i] )/ (results[1,i] )
    #iterate through the weight vector and add data to results array
    for j in range(0,3):
        results[j+3,i] = weights[j]
 
results_frame = pd.DataFrame(results.T, columns=['ret','stdev','sharpe',stocks[0], stocks[1], stocks[2]])
#locate position of portfolio with highest Sharpe Ratio
maxsp = results_frame.iloc[results_frame[['sharpe']].idxmax()]
#locate positon of portfolio with minimum standard deviation
minvp = results_frame.iloc[results_frame['stdev'].idxmin()]
print results_frame
#create scatter plot coloured by Sharpe Ratio
plt.scatter(results_frame.stdev,results_frame.ret,c = results_frame.sharpe,cmap='RdYlBu')
plt.xlabel('Volatility')
plt.ylabel('Returns')
plt.colorbar()
weights = weights*100
print ("Weights to invest in 'ASHOKLEY.NS','GBTC','GC=F' respectively are")
print weights