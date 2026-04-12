# from DBconnection import Connection
# import mplfinance as mpf
# import pandas as pd
# import matplotlib.pyplot as plt

class Engine:
    def __init__(self, stockName, dbName):
        self.__collection = stockName
        self.__dbName = dbName

    def SMA(self, timePeriod, priceArray):
        left = 0
        right = 0
        sum = 0.00
        avgArr = []
        while (right < len(priceArray)):
            sum += float(priceArray[right])
            if (right - left == timePeriod-1):
                avgArr.append(sum/float(timePeriod))
                sum -= float(priceArray[left])
                left+=1
            else:
                avgArr.append(None)
            right+=1
        return avgArr
    
    def EMA(self, timePeriod, priceArray):
        alpha = 2/(timePeriod+1)
        currIdx = 0
        currEMA = 0
        EMA_Array = []
        while (priceArray[currIdx] is None):
            EMA_Array.append(None)
            currIdx+=1
        startIdx = currIdx
        while (currIdx < len(priceArray) and currIdx-startIdx<=timePeriod):
            currEMA += priceArray[currIdx]
            EMA_Array.append(None)
            currIdx += 1
            if (currIdx - startIdx == timePeriod-1):
                currEMA = (currEMA + priceArray[currIdx])/timePeriod
                currIdx+=1
                EMA_Array.append(currEMA)
                break
        for i in range(currIdx,len(priceArray)):
            currEMA = alpha*priceArray[i] + (1-alpha)*(currEMA)
            EMA_Array.append(currEMA)
        return EMA_Array
    
    def EMADifference(self, EMAref1, EMAref2):
        differenceLine = []
        for i in range(len(EMAref1)):
            if (EMAref1[i] != None and EMAref2[i] != None):
                differenceLine.append(EMAref1[i] - EMAref2[i])
            elif (EMAref1[i] == None or EMAref2[i] == None):
                differenceLine.append(None)
        return differenceLine