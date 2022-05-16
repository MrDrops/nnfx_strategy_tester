import numpy as np
import matplotlib
import pandas as pd
import math
import datetime as dt
from pandas.tseries.offsets import BDay # BDay(x) x is an int that counts through business days - weekends
import os
import sample_manager as sm
import indicator_functions as ifunc

"""
Market Simulator offers tests for Main signal indicator and Baseline and a complete NNFX algo
tester
Has 2 more files:   sample_manager (deals with preparing the samples)
                    indicator_functions (has the functions currently available for testing)
        1 Archive:  Containing the raw market data saved from MT5
"""

#samples to use as input for testing
#Apply indicators to sample before cutting it to a shorter size
#sampleA = ifunc.sslDirectionColumns(sm.test_data_a[2],14).iloc[:,[0,1,2,3,6,7]]
#sampleA = ifunc.simpleAtrCol(sampleA,14)
#sampleA = ifunc.lwmaColumn(sampleA,3,30)
#sampleB = ifunc.sslDirectionColumns(sm.test_data_b[2],14).iloc[:,[0,1,2,3,6,7]]
#sampleB = ifunc.simpleAtrCol(sampleB,14)
#sampleB = ifunc.lwmaColumn(sampleB,3,30)

def c1YBaselineTester(df):
        '''
        df: dataframe with market data
        tp: take profit as a multiplier of ATR
        sl: stop-loss as a multiplier of ATR
        tp and sl set to NNFX default 1, 1.5 respectively
        A fast tester to test Main Signal C1 and Baseline.
        4 tests: signal alone, baseline alone, signal entry only w/ baseline deny rule, signal+baseline entry +baseline rule
        baseliene rule: if price above baseline, only longs allowed, if price below bline, only shorts allowed
        Win = price reaches TP (take profit) before it reaches SL (stop-loss)
        Returns: total entries, win, lose, zero, %win for each test
        '''
        c1Signals = []
        blineSignals = []
        baselineDeny = []
        baseToPriceDeny = []
        for d in range(len(df.index)):
                price = df.iloc[d,3]
                prevPrice = df.iloc[d-1,3]
                c1signal = df.iloc[d,4]
                atr = df.iloc[d,6]
                bline = df.iloc[d,7]
                preBline = df.iloc[d-1,7]
                blineSignal = True if (prevPrice > preBline and price < bline) or (prevPrice < preBline and price > bline) else False
                if c1signal:
                        direction = df.iloc[d,5]
                        c1Signals.append((df.index[d],direction))
                        if direction == 'long':
                                if price - bline > atr:
                                        baseToPriceDeny.append(df.index[d])
                                if price < bline:
                                        baselineDeny.append(df.index[d])
                        else:
                                if bline - price > atr:
                                        baseToPriceDeny.append(df.index[d])
                                if price > bline:
                                        baselineDeny.append(df.index[d])        
                if blineSignal:
                        blineDirection = ''
                        if prevPrice > preBline and price < bline:
                                blineDirection = 'short'
                        elif prevPrice < preBline and price > bline:
                                blineDirection = 'long'
                        blineSignals.append((df.index[d],blineDirection))
                        if blineDirection == 'long' and price - bline > atr:
                                baseToPriceDeny.append(df.index[d])
                        if blineDirection == 'short' and bline - price > atr:
                                baseToPriceDeny.append(df.index[d])
        noRepeatHolder = list(dict.fromkeys(baseToPriceDeny))
        baseToPriceDeny = noRepeatHolder
        return (c1Signals,blineSignals,baselineDeny,baseToPriceDeny)
        
def twlrTester(aSignalList,df,tp=1,sl=1.5):
        """
        calculates total, win, loss, win ratio for dates in aSignalList
        """
        win = []
        loss = []
        cnt=0
        #print(len(aSignalList))
        for tup in aSignalList:
                date = tup[0]
                cnt=cnt+1
                entryIndex = df.index.get_loc(date)
                #print(entryIndex)
                oppositeSignalCloseDate =  aSignalList[0][entryIndex+1] if entryIndex+1 < len(aSignalList[0]) else None
                atr = round(df.iloc[entryIndex,6],5)
                entryPrice = round(df.iloc[entryIndex,3],5)
                direction = tup[1]
                stopLoss = round(entryPrice - atr*sl,5) if direction=='long' else round(entryPrice + atr*sl,5)
                takeProfit = round(entryPrice + atr*tp,5) if direction=='long' else round(entryPrice - atr*tp,5)
                for i in range(len(df.index[entryIndex+1:])):
                        currIndex = entryIndex+1+i
                        currDate = df.index[currIndex]
                        hi = round(df.iloc[currIndex,1],5)
                        lo = round(df.iloc[currIndex,2],5)
                        if direction == 'long':
                                if currDate == oppositeSignalCloseDate:
                                        print(cnt)
                                        print('long loss')
                                        print('days in trade: '+str(i))
                                        loss.append(date)
                                        print((date,takeProfit, stopLoss,df.index[currIndex]))
                                        print('__________')
                                        break
                                if lo <= stopLoss:
                                        print(cnt)
                                        print('long loss')
                                        print('days in trade: '+str(i))
                                        loss.append(date)
                                        print((date,takeProfit, stopLoss,df.index[currIndex]))
                                        print('__________')
                                        break
                                if hi >= takeProfit:
                                        print(cnt)
                                        print('long win')
                                        print('days in trade: '+str(i))
                                        win.append(date)
                                        print((date,takeProfit, stopLoss,df.index[currIndex]))
                                        print('__________')
                                        break
                        else:
                                if currDate == oppositeSignalCloseDate:
                                        print(cnt)
                                        print('short loss')
                                        print('days in trade: '+str(i))
                                        loss.append(date)
                                        print((date,takeProfit, stopLoss,df.index[currIndex]))
                                        print('__________')
                                        break
                                if hi >= stopLoss:
                                        print(cnt)
                                        print('short loss')
                                        print('days in trade: '+str(i))
                                        loss.append(date)
                                        print((date,takeProfit, stopLoss,df.index[currIndex]))
                                        print('__________')
                                        break
                                if lo <= takeProfit:
                                        print(cnt)
                                        print('short win')
                                        print('days in trade: '+str(i))
                                        win.append(date)
                                        print((date,takeProfit, stopLoss,df.index[currIndex]))
                                        print('__________')
                                        break
        total = len(win)+len(loss)
        ratio = len(win) / total * 100
        #twlrTup = (total,len(win),len(loss),(len(win)/total)*100)
        #totest:
        #(date,direction,atr,stopLoss, takeProfit,lo,hi)
        #(date,direction,entryPrice,atr,stopLoss,takeProfit)
        return (len(win),len(loss),total,round(ratio,2))

def twlr(aSignalList,df,tp=1,sl=1.5):
        """
        calculates total, win, loss, win ratio for dates in aSignalList for c1YBaselineTester first 2 index ([0],[1],[],...)
        c1Signals and blineSignals
        """
        win = []
        loss = []
        #print(len(aSignalList))
        for tup in aSignalList:
                date = tup[0]
                entryIndex = df.index.get_loc(date)
                oppositeSignalCloseDate =  aSignalList[0][entryIndex+1] if entryIndex+1 < len(aSignalList[0]) else None
                atr = round(df.iloc[entryIndex,6],5)
                entryPrice = round(df.iloc[entryIndex,3],5)
                direction = tup[1]
                stopLoss = round(entryPrice - atr*sl,5) if direction=='long' else round(entryPrice + atr*sl,5)
                takeProfit = round(entryPrice + atr*tp,5) if direction=='long' else round(entryPrice - atr*tp,5)
                for i in range(len(df.index[entryIndex+1:])):
                        currIndex = entryIndex+1+i
                        currDate = df.index[currIndex]
                        hi = round(df.iloc[currIndex,1],5)
                        lo = round(df.iloc[currIndex,2],5)
                        if direction == 'long':
                                if currDate == oppositeSignalCloseDate:
                                        loss.append(date)
                                        break
                                if lo <= stopLoss:
                                        loss.append(date)
                                        break
                                if hi >= takeProfit:
                                        win.append(date)
                                        break
                        else:
                                if currDate == oppositeSignalCloseDate:
                                        loss.append(date)
                                        break
                                if hi >= stopLoss:
                                        loss.append(date)
                                        break
                                if lo <= takeProfit:
                                        win.append(date)
                                        break
        return (win,loss)

def c1YBlineResults(c1YBaselineTesterTupResult,df,inTp=1,inSl=1.5):
        """
        Takes c1YBaselineTester output and uses twlr() to return results for the chosen c1 indicator and baseline indicator
        in: tup (0,1,2,3)
        """
        c1Index = []
        for tup in c1YBaselineTesterTupResult[0]:
                c1Index.append(tup[0])
        blineIndex = []
        for tup in c1YBaselineTesterTupResult[1]:
                blineIndex.append(tup[0])
        baselineDeny = c1YBaselineTesterTupResult[2]
        baseToPriceDeny = c1YBaselineTesterTupResult[3]
        c1WinLoss = twlr(c1YBaselineTesterTupResult[0],df,inTp,inSl)
        blineWinLoss = twlr(c1YBaselineTesterTupResult[1],df,inTp,inSl)
        c1YblIndex = c1Index + blineIndex
        c1YblIndex.sort()
        c1YblIndex = list(dict.fromkeys(c1YblIndex))
        #print(len(c1YblIndex))
        holder = c1YBaselineTesterTupResult[0] + c1YBaselineTesterTupResult[1]
        holder.sort()
        holder = list(dict.fromkeys(holder))
        #print(holder)
        c1YblWinLoss = twlr(holder,df,inTp,inSl)

        c1Results = pd.DataFrame(0,c1Index,['c1Only','withBldeny', 'withBtoPDeny','bothDeny'])
        blineResults = pd.DataFrame(0,blineIndex,['blOnly','withBldeny', 'withBtoPDeny','bothDeny'])
        c1YblResults = pd.DataFrame(0,c1YblIndex,['c1Ybline','withBldeny', 'withBtoPDeny','bothDeny'])
        def dfDataFiller(df,winLossList):
                for i in range(len(df.index)):
                        date = df.index[i]
                        if date in winLossList[0]:
                                df.iloc[i,0] = 'win'
                                df.iloc[i,1] = 'win'
                                df.iloc[i,2] = 'win'
                                df.iloc[i,3] = 'win'
                        elif date in winLossList[1]:
                                df.iloc[i,0] = 'loss'
                                df.iloc[i,1] = 'loss'
                                df.iloc[i,2] = 'loss'
                                df.iloc[i,3] = 'loss'
                        else:
                                df.iloc[i,0] = np.nan
                                df.iloc[i,1] = np.nan
                                df.iloc[i,2] = np.nan
                                df.iloc[i,3] = np.nan
                        if date in baselineDeny:
                                if df.iloc[i,0] == 'win':
                                        df.iloc[i,1] = 'winDeny'
                                        df.iloc[i,3] = 'winDeny'
                                else:
                                        df.iloc[i,1] = 'deny'
                                        df.iloc[i,3] = 'deny'
                        if date in baseToPriceDeny:
                                if df.iloc[i,0] == 'win':
                                        df.iloc[i,2] = 'winDeny'
                                        df.iloc[i,3] = 'winDeny'
                                else:
                                        df.iloc[i,2] = 'deny'
                                        df.iloc[i,3] = 'deny'
        
        dfDataFiller(c1Results,c1WinLoss)
        dfDataFiller(blineResults,blineWinLoss)  
        dfDataFiller(c1YblResults,c1YblWinLoss)
        return (c1Results,blineResults,c1YblResults)

def resultsReader(c1YBlineResults):
        """
        return dataframe results from c1YBlineResults()
        """
        def twld(df,column):
                #total = len(df.index)
                win = len(df[df.iloc[:,column]=='win'])
                loss = len(df[df.iloc[:,column]=='loss'])
                deny = len(df[df.iloc[:,column]=='deny'])
                winDeny = len(df[df.iloc[:,column]=='winDeny'])
                wlRatio = round(win / loss,2)
                total = win + loss
                return (total,win,round(win/total*100,2),loss,round(loss/total*100,2),wlRatio,deny,winDeny)
        #Organizing Results to display in a Df
        c1A = twld(c1YBlineResults[0],0)
        c1B = twld(c1YBlineResults[0],1)
        c1C = twld(c1YBlineResults[0],2)
        c1D = twld(c1YBlineResults[0],3)
        c2A = twld(c1YBlineResults[1],0)
        c2B = twld(c1YBlineResults[1],1)
        c2C = twld(c1YBlineResults[1],2)
        c2D = twld(c1YBlineResults[1],3)
        c3A = twld(c1YBlineResults[2],0)
        c3B = twld(c1YBlineResults[2],1)
        c3C = twld(c1YBlineResults[2],2)
        c3D = twld(c1YBlineResults[2],3)
        rowValues = [c1A,c1B,c1C,c1D,c2A,c2B,c2C,c2D,c3A,c3B,c3C,c3D]
        rowNames = ['c1', 'c1BlDeny', 'c1BtoPDeny', 'c1BothDeny', 'bl', 'blBlDeny', 'blBtoPDeny',
                'blBothDeny', 'both', 'bothBlDeny', 'bothBtoPDeny', 'bothBothDeny']
        colNames = ['total','win','win%','loss','loss%', 'wlRatio','deny', 'winDeny']
        ansDf = pd.DataFrame(rowValues, rowNames, colNames)
        return ansDf

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
                ansList.append(sampleA[startDate:])
        return (samplePrepperList[0],ansList)

def basicTestExe (preppedSampleTup,inTp=1,inSl=1.5):
        """
        calculates the basic test for given pairData set and gives a summary of input pairs
        in: ([],[]), int, int
        ret: tup (df,str list,df list) (summary of input pairs, pair name list, list of individual
        data for input pairs)
        """
        names = preppedSampleTup[0]
        ansList = []
        for pairData in preppedSampleTup[1]:
                holderA = c1YBaselineTester(pairData)
                holderB = c1YBlineResults(holderA, pairData,inTp,inSl)
                holderC = resultsReader(holderB)
                ansList.append(holderC)
        provTotal = sum(ansList)
        provTotal['win%'] = round(provTotal['win'] / provTotal['total'] * 100, 2)
        provTotal['loss%'] = round(provTotal['loss'] / provTotal['total'] * 100, 2)
        provTotal['wlRatio'] = round(provTotal['win'] / provTotal['loss'], 2)
        print(names)
        return (provTotal, names, ansList)

#test area below

#shortSampleA = sampleA['2018-11-01':]
#mainSample = c1YBaselineTester(shortSampleA)
#c1Signals = mainSample[0]
#blineSignals = mainSample[1]
#baselineDeny = mainSample[2]
#baseToPriceDeny = mainSample[3]
#resultTest = c1YBlineResults(mainSample,shortSampleA)
#resultTestC1Dates = twlr(blineSignals,shortSampleA)

temp = sm.sampleChoser([('gbp','usd'),('nzd','usd'),('aud','jpy'),('eur','gbp'),('gbp','chf'),('gbp','cad'),('eur','nzd'),('nzd','jpy')])
#[('gbp','usd'),('nzd','usd'),('aud','jpy'),('eur','gbp'),('gbp','chf'),('gbp','cad'),('eur','nzd'),('nzd','jpy')]
temp2 = sm.samplePreper(temp)
sampleC = dataIndicatorApi(temp2,'2017-11-01')
basicExe = basicTestExe(sampleC)
