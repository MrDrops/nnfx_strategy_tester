import numpy as np
import matplotlib
import pandas as pd
import math
import datetime as dt
from pandas.tseries.offsets import BDay # BDay(x) x is an int that counts through business days - weekends
import os

#INDICATOR FUNCTIONS
#All take a df with market data (metaTrader .csv export) and return a df with the
#indicator results as extra columns

# sample to test model to avoid full load of files
load_df = pd.read_csv('C:\\Users\\Drops\\Documents\\Trading_Files\\chart_data_files\\AUDCADDaily.csv',
            encoding='utf-16',names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickVol'],
            index_col='date',header=1, parse_dates=True, infer_datetime_format=True)
sample = load_df.loc['2017-01-02':'2020-09-01']

def lwma(df, col, date, period) :
    '''
    Calculates line weighted moving average for market data dataFrame
    df: dataframe containing price data
    col: (int) column of df to calculate LWMA for (0=open,1=hi,2=lo,3=close,4=vol,5=ticVol)
    date: (str) to calculate moving average for
    period: (int) number of days to go back for calculation
    return: (float) line weighted moving average for that specific dataframe date (datapoint [pd.Series])
    '''
    #determine period start-stop index on df
    dateIndex = len(df.index) - (len(df.index) - len(df.loc[ : date]))
    periodStart = dateIndex - period
    #initializing variable answer
    lwma = int
    #catching error if period back is longer than df
    if periodStart < 0:
        lwma = np.nan
    #Now the actual lwma calculation
    else:    
        periodData = df.iloc[ periodStart : dateIndex, col]
        summ = 0
        indexMultiplier = 1
        divisor = 0
        for dayPrice in periodData:
            summ += dayPrice * indexMultiplier
            divisor = divisor + indexMultiplier
            indexMultiplier +=1   
        lwma = summ / divisor
    return lwma

def lwmaColumn(df, col, period):
    '''
    Makes a dictionary{[Date] : lwma...} for eventual anexing to df if needed
    df: (dataframe) market data
    col: desired column to caculate (0=open,1=hi,2=lo,3=close,4=vol,5=ticVol)
    period: (int) number of days to go back for calculation
    return: (dict) dict[date] : lwma
    '''
    ansDict = {}
    for date in df.index:
        dateLwma = lwma(df,col,date,period)
        ansDict[date] = dateLwma
    ansDf = df.copy()
    lwmaVar = ansDict.values()
    ansDf['lwma'+str(period)] = lwmaVar
    return ansDf

def emaCol(df, col, period) :
    '''
    creates a new series for the df with ema calculated for everydf datapoint
    df: df containing market data
    col: (int) which column to calculate EMA for (0=open,1=hi,2=lo,3=close,4=vol,5=ticVol)
    period: (int) units of timePeriod (days mostly) to calculate EMA
    returns: (dict) date: EMA
    '''
    ansDict = {}
    #determine starting ema
    #period start-stop index on df
    smoothConstant = 2 / (period + 1)
    for n in range(0, len(df.index)):
        if n < period-1:
            ansDict[df.index[n]] = np.nan
        elif n == period-1:
            ansDict[df.index[n]] = df.iloc[:period,col].mean()
        else:
            currPrice = df.iloc[n,col]
            prevDate = df.index[n-1]
            prevEma = ansDict[prevDate]
            ansDict[df.index[n]] = (currPrice - prevEma) * smoothConstant + prevEma
    
    ansDf = df.copy()
    ema = ansDict.values()
    ansDf['ema'+str(period)] = ema   
    return ansDf

def SmoothAtrCol(df, period) :
    '''
    Calculates the smooth average true range for each datapoint in df
    MQ5 ATR is a simple TR average without smoothing factor, so results are slightly different
    df: dataframe with market data
    period: time units of length to calculate ATR
    return: (dict) dict[date] : atrValue
    '''
    ansDict = {}
    for n in range(0, len(df.index)):
        if n == 0:
            #set 1st ATR to current.hi - current.lo
            ansDict[df.index[n]] = df.iloc[n,1] - df.iloc[n,2]
        else:
            #True range calculation = Max value of:(current high-current low), 
            #abs(current high - previous close),abs(current low - previous close):
            currentTr = max(df.iloc[n,1], df.iloc[n-1,3]) - min(df.iloc[n,2], df.iloc[n-1,3])

            if n < period-1:
                #sets all days' ATRs before the period input to their True Range                
                ansDict[df.index[n]] = currentTr
            elif n == period-1:
                #sets first within period ATR as the average of current TR + all previous TR
                ansDict[df.index[n]] = (sum(ansDict.values()) + currentTr) / period
            else:
                #smooths all ATRs after minimum required period with:
                prevDate = df.index[n-1]
                prevAtr = ansDict[prevDate]
                #Current ATR = ((prior ATR * (period-1) + current TR) / period
                ansDict[df.index[n]] = ((prevAtr * (period-1)) + currentTr) / period
    ansDf = df.copy()
    smthAtr = ansDict.values()
    ansDf['smthAtr'+str(period)] = smthAtr   
    return ansDf

def simpleAtrCol(df, period):
    '''
    ATR simple, without the smoothing factor as used in mq5
    df: dataframe with market data
    period: (int) time units of length to calculate ATR
    return: (dict) dict[date] : atrValue
    '''
    ansDict = {}
    #list stores True Range values
    trList = []
    for n in range(0, len(df.index)):
        if n== 0:
            #set 1st TR to current.hi - current.lo
            trList.append(df.iloc[n,1] - df.iloc[n,2])
            ansDict[df.index[n]] = np.nan
        else:
            currentTr = max(df.iloc[n,1], df.iloc[n-1,3]) - min(df.iloc[n,2], df.iloc[n-1,3])
            #sets all days' ATRs before the period input to their True Range 
            if n < period-1:
                ansDict[df.index[n]] = np.nan
                trList.append(currentTr)               
            elif n == period-1:
                firstAtr = (sum(trList) + currentTr) / period
                ansDict[df.index[n]] = firstAtr
                trList.append(currentTr)
            else:
                trList.append(currentTr)
                currentATR = sum(trList[n+1-(period) : n+1]) / period
                ansDict[df.index[n]] = currentATR
    
    ansDf = df.copy()
    atr = ansDict.values()
    ansDf['atr'+str(period)] = atr   
    return ansDf

def sslLwma (df, hiMaCol, loMaCol):
    '''
    calculates SSL channel indicator based of lwma high and low
    df: (dataframe) market data for calculations with hima and loma cols added (example cols: 0=open,1=hi,2=lo,3=close,4=hiMa,5=loMa)
    hiMaCol: (int) what index is the High ma in the df
    loMaCol: (int) what index is the low ma in the df
    return: (dict) index=date, data= list[ ((tuple)sslUp(float), sslDn(float)), signal(Bool),direction]
    Note: if backtesting with mt5, ssl hi or ssl low is based on lwma of previous day
    '''
    ansDict = {}
    hlv = 0
    trend = 0
    prev = np.nan
    for n in range(0,len(df.index)):
        if df.iloc[n,hiMaCol] == np.nan or df.iloc[n,loMaCol] == np.nan:
            ansDict[df.index[n]] = (np.nan, np.nan, np.nan, np.nan)
            continue
        else:
            #if close price > high moving average
            if df.iloc[n,3] > df.iloc[n,hiMaCol]:
                hlv = 1
            #if close price < low moving average
            elif df.iloc[n,3] < df.iloc[n,loMaCol]:
                hlv = - 1
            #if close price remains within high and low moving average boundaries
            else:
                hlv = 0
        
        sslUp = df.iloc[n,hiMaCol]
        sslDn = df.iloc[n,loMaCol]
        signal = False
        longShort = np.nan
        #if signal
        if hlv != 0:
            #if close price went above below low Ma
            if hlv < 0:
                #SSL down = high Ma, SSL up = low Ma
                sslDn = df.iloc[n,hiMaCol]
                sslUp = df.iloc[n,loMaCol]
                #signal is true because up and down MA swappped IF its not already in -trend
                if trend != -1:
                    signal = True
                    longShort = "short"
                else:
                    signal = False
                    longShort = 'short'
                #flag to know if SSL up is LoMa
                trend = -1
            else:
                sslUp = df.iloc[n, hiMaCol]
                sslDn = df.iloc[n,loMaCol]
                if trend != 1:
                    signal = True
                    longShort = "long"
                else:
                    signal = False
                    longShort = 'long'
                trend = 1
        #if no signal
        #if price did not close higher than hiMA or lower than LoMa
        else:
            longShort = prev
            #sslDn keeps being hiMA, SSlUp keep being LoMa
            if trend < 0:
                sslDn = df.iloc[n, hiMaCol]
                sslUp = df.iloc[n, loMaCol]
                signal = False
            #sslUp keeps being hiMa, sslDn keeps being loMa
            elif trend > 0:
                sslUp = df.iloc[n,hiMaCol]
                sslDn = df.iloc[n,loMaCol]
                signal = False
            #for any day data before any  1st trend signal
            else:
                sslUp = df.iloc[n,hiMaCol]
                sslDn = df.iloc[n,loMaCol]
        prev = longShort
        ansDict[df.index[n]] = (sslUp, sslDn, signal, longShort)

    return ansDict

def sslDirectionColumns(df, period):
    '''
    Creates a new df.copy, cuts vol and tick vol columns, adds 4 columns: hiLwma, lolwma, 
    ssl (Bool: signal), direction (str: 'long'|'short')
    df: (dataframe) market data columns=(0='open', 1='high', 2='low', 3='close', 4='hiLwma', 5='loLwma')
    period: (int) time interval to calculate lwma
    return: (df) columns(0='open',1='high',2='low',3='close',4='hiLwma',5='loLwma', 6='ssl',7='direction')
    '''
    ansDf = df.iloc[:, 0:4].copy()
    prov1 = lwmaColumn(ansDf,1,period)
    name1 = 'lwma'+str(period)
    ansDf['hiLwma'] = prov1[name1]
    prov2 = lwmaColumn(ansDf,2,period)
    ansDf['loLwma'] = prov2[name1]
    sslDict = sslLwma(ansDf, 4, 5)
    sslList = sslDict.values()
    sslSignal = []
    sslDirection = []
    for n in sslList:
        sslSignal.append(n[2])
        sslDirection.append(n[3])
    ansDf['ssl'] = sslSignal
    ansDf['direction'] = sslDirection

    return ansDf

def wpo (df, period=14, maxPeriod=3, priceType='close') :
    '''
    Wave Price Oscillator. Calculates the wave period oscillator for the dataset
    period: (int) number of time periods to calulate wpo
    maxPeriod: (int) number of days to look back for max price
    priceType: (str) which price to use (open,hi,lo,close,median,typical,weighted)
    return: list of wpo results for given df
    '''
    def setPrice(priceType,index):
        if priceType == 'open':
            price = df.iloc[index,0]
        elif priceType == 'high':
            price = df.iloc[index,1]
        elif priceType == 'low':
            price = df.iloc[index,2]
        elif priceType == 'close':
            price = df.iloc[index,3]
        elif priceType == 'median':
            price = (df.iloc[index,1] + df.iloc[index,2]) / 2
        elif priceType == 'typical':
            price = (df.iloc[index,1] + df.iloc[index,2] + df.iloc[index,3]) / 3
        elif priceType == 'weighted':
            price = (df.iloc[index,1] + df.iloc[index,2] + (df.iloc[index,3] *2)) / 4
        else:
            print('wrong priceType')
        return price
    alpha = 2 / (1 + period) if period > 1 else 1
    priceList = []
    valueList = []
    prevMax = 0
    for index in range(0,len(df.index)):
        price = setPrice(priceType,index)
        #print(price==df.iloc[index,3])
        priceList.append(price)
        #print(priceList[index]==df.iloc[index,3])
        start = index - maxPeriod + 1
        if start < 0:
            start = 0
        end = start + maxPeriod-1
        prevMax = max(priceList[start:end])
        currentMax = price if price > prevMax else prevMax
        #print(df.index[index])
        angle = np.arcsin(price / currentMax)
        pi = 3.14159265358979323846
        wave = 2 * pi / angle
        wave = wave if priceList[index] > priceList[index-1] else -wave
        singleValue = 0 if index <= 0 else valueList[index-1] + alpha * (wave - valueList[index-1])
        valueList.append(singleValue)
    return valueList

def wpoColumnAsVolume(df, maxAmp=0.5, minAmp=-0.5, period=20, maxPeriod=3, priceType='typical'):
    '''
    creates a copy of the input df and adds a volume column
    maxAmp: (float) high limit range for wpo oscillator low volume boundary
    minAmp: (float) low limit range for wpo oscillator low volume boundary
    period: (int) period to calculate wpo for
    maxPeriod = lookback Period to get highest price
    return: (df) copy with added volume column
    '''
    ansDf = df.copy()
    wpoList = wpo(df,period,maxPeriod, priceType)
    volume = []
    for n in wpoList:
        if n >= minAmp and n <= maxAmp:
            enoughVolume = False
        else:
            enoughVolume = True
        volume.append(enoughVolume)
    if len(volume) != len(wpoList):
        print('error')
    ansDf['enoughVolume'] = volume
    return ansDf

def hmaCol(inDf, maType='ema', period=7, column=3):
    '''
    creates hull moving average column for current market data df
    inDf: (df) contains the market data for hma calculation
    maType: (str) 'lwma' or 'ema'
    period: (int) period of the MA
    column: (int) which column to calculate hma for. 3=close
    '''
    ansDf = inDf.copy()
    mainHolder2 =inDf.copy()
    half = math.floor(period / 2)
    sqrtVar1 = math.floor(math.sqrt(period))
    sqrtVar = sqrtVar1
    if maType == 'ema':
        mainHolder = inDf.copy()
        holder1 = emaCol(mainHolder,column,period)
        colName1 = 'ema'+str(period)
        mainHolder['ma'] = holder1[colName1]
        mainHolder.fillna(0,inplace=True)
        holder2 = emaCol(mainHolder,column,half)
        colName2 = 'ema'+str(half)
        mainHolder['halfMa'] = holder2[colName2]
        mainHolder.fillna(0,inplace=True)
        mainHolder['maBoth'] = 2 * mainHolder['halfMa'] - mainHolder['ma']
        #print(mainHolder.columns[6])
        mainHolder2 = emaCol(mainHolder, 8, sqrtVar)
        colName3 = 'ema'+str(sqrtVar)
        #print(colName3)
        ansDf['hma'] = mainHolder2[colName3]
        #print(mainHolder.columns)
    elif maType == 'lwma':
        mainHolder = inDf.copy()
        holder1 = lwmaColumn(mainHolder,column,period)
        colName1 = 'lwma'+str(period)
        mainHolder['ma'] = holder1[colName1]
        mainHolder.fillna(0,inplace=True)
        holder2 = lwmaColumn(mainHolder,column,half)
        colName2 = 'lwma'+str(half)
        mainHolder['halfMa'] = holder2[colName2]
        mainHolder.fillna(0,inplace=True)
        mainHolder['maBoth'] = 2 * mainHolder['halfMa'] - mainHolder['ma']
        mainHolder2 = lwmaColumn(mainHolder, 8, sqrtVar)
        colName3 = 'lwma'+str(sqrtVar)
        ansDf['hma'] = mainHolder2[colName3]
    else:
        print('error')
    return ansDf#mainHolder2

def hmaExitIndicator(inDf, maType='ema',period=7,column=3):
    '''
    takes inDf already sorted as follow: columns=(0='open',1='high',2='low',3='close',4='signal',5='direction',
    6='baseline',7='atr') and adds: 8='exitIndSig', 9='exitIndiDirection'
    in: (df) with market data arranged as above
    return df with mentioned columns
    '''
    ansDf = inDf.copy()
    holder1 = hmaCol(inDf, maType, period, column)
    hmaExit = []
    hmaDirection = []
    prevDirection = ''
    currentDirection = ''
    for n in range(0,len(inDf.index)):
        #limit value control: if there is no data before at begining of df
        if n == 0:
            hmaExit.append(np.nan)
            hmaDirection.append(np.nan)
        #setting starting direction
        elif n == 1:
            pointA = holder1.iloc[0,6]
            pointB = holder1.iloc[1,6]
            if pointA < pointB:
                prevDirection = 'long'
                currentDirection = prevDirection
                hmaExit.append(False)
                hmaDirection.append(currentDirection)
            else:
                prevDirection = 'short'
                currentDirection = prevDirection
                hmaExit.append(False)
                hmaDirection.append(currentDirection)
        #start direction calculation if first signal capable index (has startDirection but no signal yet),
        else:   
            pointA = holder1.iloc[n-1,6]
            pointB = holder1.iloc[n,6]
            if pointA < pointB:
                currentDirection = 'long'
                hmaDirection.append(currentDirection)
                if currentDirection == prevDirection:
                    hmaExit.append(False)
                else:
                    hmaExit.append(True)
                prevDirection = currentDirection                
            #pointA >= pointB
            else:
                currentDirection = 'short'
                hmaDirection.append(currentDirection)
                if currentDirection == prevDirection:
                    hmaExit.append(False)
                else:
                    hmaExit.append(True)
                prevDirection = currentDirection
    ansDf['exitSignal'] = hmaExit
    ansDf['exitDirection'] = hmaDirection

    return ansDf


#CONDITIONS FOR TRADE FUNCTIONS
# 

def baselineApproved(df):
    '''
    in: df with a 'baseline' column on it
    no return. modifies in df adding a 'baselineApproved' column
    '''
    df['baselineApproved'] = np.nan
    for rowNum in range(0, len(df.index)):
        date = df.index[rowNum]
        price = df.loc[date,'close']
        baselinePrice = df.loc[date, 'baseline']
        #if df.loc[date,'entrySignal'] == True:
        if df.loc[date, 'entryDirection'] == 'long':
            if price > baselinePrice:
                df.loc[date, 'baselineApproved'] = True
            else:
                df.loc[date, 'baselineApproved'] = False
        #signal direction == 'short'
        else:
            if price < baselinePrice:
                df.loc[date, 'baselineApproved'] = True
            else:
                df.loc[date, 'baselineApproved'] = False
        #else:
        #    df.loc[date, 'baselineApproved'] = False
    return None