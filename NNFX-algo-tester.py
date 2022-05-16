import numpy as np
import matplotlib
import pandas as pd
import math
import datetime as dt
from pandas.tseries.offsets import BDay # BDay(x) x is an int that counts through business days - weekends
import os
import sample_manager as sm
import indicator_functions as ifunc

def dataIndicatorApi(samplePrepperList, startDate='2018-11-01'):
        """
        Takes the list of samples and attaches indicator data.
        This function has to be changed to adjust to indicators tested
        End form: dateIndex-open-high-low-close-c1Signal-direction-atr-baseline
        """
        ansList = []
        pairList = samplePrepperList[1]
        for pairData in pairList:
                sampleA = ifunc.sslDirectionColumns(pairData,14).iloc[:,[0,1,2,3,6,7]]
                sampleA = ifunc.simpleAtrCol(sampleA,14)
                sampleA = ifunc.lwmaColumn(sampleA,3,30)
                sampleA['exitSig'] = False
                #added to artificially get input to test code
                #have to be added with real indicator results
                sampleA['exitDirection'] = sampleA['direction']
                sampleA['c2Signal'] = sampleA['ssl']
                sampleA['c2Direction'] = sampleA['direction']
                sampleA['volDeny'] = False
                sampleA['continuation'] = False
                sampleA['contDirection'] = sampleA['direction']
                ansList.append(sampleA[startDate:])

        return (samplePrepperList[0],ansList)

def isEntry(sample):
    """
    in: tuple dataIndicatorApi(samplePreper(sampleChoser)). index 0 = list of pair names in order
    index 2 = pair data with all indicators attached in the form of:
    dateIndex-open-high-low-close-C1Signal-C1Direction-atr-baseline-closeSignal-CloseDirection-c2Signal-c2Direction-
    volumeDeny-continuationSignal-direction
    return: [(date,pairName,entryType),(),()...]
    """
    def blEntry(df, indexDate):
        bline = df.iloc[indexDate,7]
        preBline = df.iloc[indexDate-1,7]
        price = df.iloc[indexDate,3]
        prevPrice = df.iloc[indexDate-1,3]
        blSignal = False
        if (prevPrice > preBline and price < bline) or (prevPrice < preBline and price > bline):
            blSignal = True
        return blSignal

    pairNames = sample[0]
    pairData = sample[1]
    ansList = []
    for pairInd in range(len(pairData)):
        name = pairNames[pairInd]
        pairDf = pairData[pairInd]
        for d in range(len(pairDf)):
            date = pairDf.index[d]
            if pairDf.iloc[d,4] == True:
                ansList.append((date, name, 'c1'))
            elif blEntry(pairDf, d) == True:
                ansList.append((date, name, 'bl'))
    ansList.sort(key=lambda entry : entry[0])
    return ansList

def algoTester (sample,tp=1, sl=1.5, risk=2, accSize=10000, entryType = 'c1'):
    """
    in: entryType = 'c1','bl','both'
    Backtests data in df and returns results for given pair data
    """
    account = accSize
    downTurn = 0
    entryList = isEntry(sample)
    remove = entryType
    newEntryList = [x for x in entryList if x[2] == entryType]
    for entry in entryList:
        sigDate = entry[0]
        name = entry[1]
        sigType = entry[2]
        pairIndx = sample[0].index(name)
        pairData = sample[1][pairIndx]
        entryIndex = pairData.index.get_loc(sigDate)
    print(list(newEntryList))
        
        

    return 0


def isExit():

    return 0

#test Area
prePairData = sm.sampleChoser([('gbp','usd'),('nzd','usd')])
preSample = sm.samplePreper(prePairData)
sample = dataIndicatorApi(preSample)

