from DBconnection import Connection

def EMA(priceArray, timePeriod):
    currentEMA = 0
    result = []
    window = 0
    for i in range(0,timePeriod-1):
        if (priceArray[i] == None):
            result.append(None)
            continue
        currentEMA += priceArray[i]
        window += 1
        result.append(None)
    currentEMA = currentEMA/window
    result.append(currentEMA)
    # print(f"first range of EMA is: {currentEMA}")
    alpha = 2/(timePeriod+1)
    for i in range(timePeriod,len(priceArray)):
        if (priceArray[i] == None):
            result.append(None)
            continue
        currentEMA = alpha*priceArray[i] + (1-alpha)*currentEMA
        result.append(currentEMA)
    return result


def MovingAverageCovengenceDivergence(priceArray):
    MACD_Generating_Line = []
    EMA_26 = EMA(priceArray,26)
    EMA_12 = EMA(priceArray,12)
    for i in range(len(EMA_12)):
        if (EMA_12[i] != None and EMA_26[i] != None):
            MACD_Generating_Line.append(EMA_12[i] - EMA_26[i])
        elif (EMA_12[i] == None or EMA_26[i] == None):
            MACD_Generating_Line.append(None)
    Signal = EMA(MACD_Generating_Line,9)
    Histogram = []
    for i in range(len(Signal)):
        if (MACD_Generating_Line[i] != None and Signal[i] != None):
            Histogram.append(MACD_Generating_Line[i] - Signal[i])
        elif (MACD_Generating_Line[i] == None or Signal[i] == None):
            Histogram.append(None)
    return {"Histogram":Histogram,"MACD Generating Line":MACD_Generating_Line,"Signal":Signal}
    

connectionObj = Connection("SPGI","time_series_daily")
prices = connectionObj.get_close_prices()
print(MovingAverageCovengenceDivergence(prices))