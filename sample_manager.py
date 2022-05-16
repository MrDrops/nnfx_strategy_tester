import numpy as np
import matplotlib
import pandas as pd
import math
import datetime as dt
from pandas.tseries.offsets import BDay # BDay(x) x is an int that counts through business days - weekends
import os

#The sample_manager contains all functions responsible for managing the raw data

gbpusd = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/GBPUSDDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
usdchf = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/USDCHFDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
eurusd = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/EURUSDDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
usdjpy = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/USDJPYDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
audusd = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/AUDUSDDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
usdcad = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/USDCADDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
#MINORS 
audcad = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/AUDCADDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
audchf = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/AUDCHFDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
audjpy = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/AUDJPYDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
euraud = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/EURAUDDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
audnzd = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/AUDNZDDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
gbpaud = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/GBPAUDDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
#GBP
eurgbp = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/EURGBPDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
gbpchf = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/GBPCHFDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
gbpjpy = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/GBPJPYDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
gbpcad = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/gbpcaddaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
gbpnzd = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/GBPNZDDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
#CHF
chfjpy = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/CHFJPYDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
eurchf = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/EURCHFDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
cadchf = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/CADCHFDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
nzdchf = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/NZDCHFDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
#JPY
eurjpy = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/EURJPYDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
cadjpy = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/CADJPYDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
nzdjpy = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/NZDJPYDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
#EUR
eurnzd = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/EURNZDDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
eurcad = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/EURCADDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
#NZD
nzdcad = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/NZDCADDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
nzdusd = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/NZDUSDDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)
#SGD singapur
usdsgd = pd.read_csv('c:/Users/Drops/Documents/code_practice/nnfx_strategy_tester/pair_data/USDSGDDaily.csv',
                    encoding='utf-16', names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
                    index_col='date', header=1, parse_dates=True, infer_datetime_format=True)

def samplePruner(start ='2010-01-04',end ='2020-01-24'):
    '''
    labels and prunes pair data based on input dates and joins in a tupple of tuples
    start: (str) date start
    end: (str) date end
    return: (tup of tups) in the form ((pairName1, pairName2, dataframe w/ market data), (...), (...), ...)
    '''
    universeArr = ( ('gbp','usd',gbpusd[start:end]), ('usd','chf',usdchf[start:end]), ('eur','usd',eurusd[start:end]),
                    ('usd','jpy',usdjpy[start:end]), ('aud','usd',audusd[start:end]), ('usd','cad',usdcad[start:end]),
                    ('usd','sgd',usdsgd[start:end]), ('nzd','usd',nzdusd[start:end]), ('aud','cad',audcad[start:end]),
                    ('aud','chf',audchf[start:end]), ('aud','jpy',audjpy[start:end]), ('eur','aud',euraud[start:end]),
                    ('aud','nzd',audnzd[start:end]), ('gbp','aud',gbpaud[start:end]), ('eur','gbp',eurgbp[start:end]),
                    ('gbp','chf',gbpchf[start:end]), ('gbp','jpy',gbpjpy[start:end]), ('gbp','cad',gbpcad[start:end]),
                    ('gbp','nzd',gbpnzd[start:end]), ('chf','jpy',chfjpy[start:end]), ('eur','chf',eurchf[start:end]),
                    ('cad','chf',cadchf[start:end]), ('nzd','chf',nzdchf[start:end]), ('eur','jpy',eurjpy[start:end]),
                    ('cad','jpy',cadjpy[start:end]), ('nzd','jpy',nzdjpy[start:end]), ('eur','nzd',eurnzd[start:end]),
                    ('eur','cad',eurcad[start:end]), ('nzd','cad',nzdcad[start:end]) )
    return universeArr

def sampleChoser (sampleChoice, start='2010-01-04', end='2020-01-24'):
    """
    allows to choose the dataset to make a sample. Options are: allPairs, majors, minors, a single
    pair (form 'xxx xxx' e.g 'gbp usd') or
    oneCurrency or several currencies (in the form of ['xxx','xxx',...] e.g: ['aud','usd',...])
    returns tuple with desired pair data
    """
    allP = [ 
        ('gbp','usd','major',gbpusd[start:end]), ('usd','chf','major',usdchf[start:end]), ('eur','usd','major',eurusd[start:end]),
        ('usd','jpy','major',usdjpy[start:end]), ('aud','usd','major',audusd[start:end]), ('usd','cad','major',usdcad[start:end]),
        ('usd','sgd','minor',usdsgd[start:end]), ('nzd','usd','minor',nzdusd[start:end]), ('aud','cad','minor',audcad[start:end]),
        ('aud','chf','minor',audchf[start:end]), ('aud','jpy','minor',audjpy[start:end]), ('eur','aud','minor',euraud[start:end]),
        ('aud','nzd','minor',audnzd[start:end]), ('gbp','aud','minor',gbpaud[start:end]), ('eur','gbp','minor',eurgbp[start:end]),
        ('gbp','chf','minor',gbpchf[start:end]), ('gbp','jpy','minor',gbpjpy[start:end]), ('gbp','cad','minor',gbpcad[start:end]),
        ('gbp','nzd','minor',gbpnzd[start:end]), ('chf','jpy','minor',chfjpy[start:end]), ('eur','chf','minor',eurchf[start:end]),
        ('cad','chf','minor',cadchf[start:end]), ('nzd','chf','minor',nzdchf[start:end]), ('eur','jpy','minor',eurjpy[start:end]),
        ('cad','jpy','minor',cadjpy[start:end]), ('nzd','jpy','minor',nzdjpy[start:end]), ('eur','nzd','minor',eurnzd[start:end]),
        ('eur','cad','minor',eurcad[start:end]), ('nzd','cad','minor',nzdcad[start:end]) ]
    
    ansSample = []
    if sampleChoice == 'allP':
        ansSample = allP
    elif sampleChoice == 'major':
        for pairData in allP:
            if pairData[2] == 'major':
                ansSample.append(pairData)
    elif sampleChoice =='minor':
        for pairData in allP:
            if pairData[2] == 'minor':
                ansSample.append(pairData)
    elif len(sampleChoice) == 7:
        pairNames = sampleChoice.split()
        for pairData in allP:
            if pairData[0]==pairNames[0] and pairData[1]==pairNames[1]:
                ansSample.append(pairData)
    else:
        for choice in sampleChoice:
            for pairData in allP:
                if pairData[0] == choice[0] and pairData[1] == choice[1]:
                    if pairData not in ansSample:
                        ansSample.append(pairData)
    return ansSample

def samplePreper(sampleChoserList):
    """
    takes list of pair data and separates it from its metadata(pair name and grouping)
    returns tup of 2 lists ([metadata in order],[pair data in order])
    """
    pairMeta = []
    pairData = []
    for wholeData in sampleChoserList:
        pairMeta.append((wholeData[0],wholeData[1]))
        pairData.append(wholeData[3])
    return (pairMeta,pairData)

#Test area
#a=sampleChoser([('gbp','usd'),('nzd','usd'),('aud','jpy'),('eur','gbp'),('gbp','chf'),('gbp','cad'),('eur','nzd'),('nzd','jpy')])
#[('gbp','usd'),('nzd','usd'),('aud','jpy'),('eur','gbp'),('gbp','chf'),('gbp','cad'),('eur','nzd'),('nzd','jpy')]
#test_data_a = ('aud','usd',audusd['2015-01-04':'2020-01-24'])
#test_data_b = ('aud','nzd',audnzd['2015-01-04':'2020-01-24'])

