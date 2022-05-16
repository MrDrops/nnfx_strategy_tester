# NNFX STRATEGY TESTER
Originally written before 09/2020

## Description
The tester is a market model to test trading strategies based on No-Nonsese Forex Trading Strategy. It uses market data from MetaTrader 5 to test the selected indicators and trade rules that make a specific trading strategy. The market simulator uses Pandas dataframes as dataypes for market data and Numpy to calculate the indicators values and identify the different rules to enter and exit the market. It can test one or many datasets to determine if there is an edge in specific currency pairs or in a broader set of currencies. To test market hypothesis with different indicators, 
indicators are manually pre-selected with another tool and later coded in a separate file which allows any previously coded indicator to be tested in various positions of the NNFX trading algorithm. Results provided are: total trades, win, loss and 0 loss trades, as well as the percentage return based on initial account value for the whole dataset or separated by specific currency pairs. More information on specific trades like percentage of profit vs maximum profit possible is also available in case strategy optimisation was desired.

## Motivation
The year  before I programmed this strategy tester, I discovered the No-Nonsense trading strategy by JP and loved the idea of a combination of indicators (entry, confirmation, volume, baseline, ATR, and rules), because it made it possible to test multiple hypothesis programatically, and evry indicator I could add to the database would allow for more possibilities to find an edge in the market without having to create a whole new strategy. Moreover, the possibilities of further optimisation and the availability of free market data made it an interesting project to work on. 

## Build Status
MVP. It served the purpose of testing a combination of indicators to find an edge to try in live trading. I did not add some of the other minor NNFX rules (like a bridge too far, reentry, etc). It is restricted to the current indicators coded but unlimited indicators could be added to test new strategy combinations if desired.

## Tech used
- Python
- Numpy
- Pandas
