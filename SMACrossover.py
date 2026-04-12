from DBconnection import Connection

def SMA(price_array, timePeriod):
    print(f"Calculating Simple Moving Average for {timePeriod} days...")
    left = 0
    right = 0
    sum = 0.00
    avgArr = []
    while (right < len(price_array)):
        sum += float(price_array[right])
        if (right - left == timePeriod-1):
            avgArr.append(sum/float(timePeriod))
            sum -= float(price_array[left])
            left+=1
        right+=1 
    return avgArr

def SMACrossover(priceArray, shortInterval, longInterval):
    print("Finding Crossovers and Backtesting...")
    smaShortArray = SMA(priceArray,shortInterval)
    smaLongArray = SMA(priceArray,longInterval)
    offset = longInterval - shortInterval
    position = 0
    buyPrice = 0
    netProfit = 0
    numTrades = 0
    profitNum = 0
    for i in range(1, len(smaLongArray)-1):
        if i + longInterval >= len(priceArray):
            break
        smaShort_prev = smaShortArray[i-1 + offset]
        smaShort_curr = smaShortArray[i + offset]
        smaLong_prev = smaLongArray[i-1]
        smaLong_curr = smaLongArray[i]
        if position == 0 and smaShort_prev < smaLong_prev and smaShort_curr >= smaLong_curr:
            buyPrice = float(priceArray[i + longInterval + 1])
            position = 1
        elif position == 1 and smaShort_prev > smaLong_prev and smaShort_curr <= smaLong_curr:
            sellPrice = float(priceArray[i + longInterval + 1])
            netProfit += (sellPrice - buyPrice)
            if ((sellPrice - buyPrice) >= 0):
                profitNum += 1
            numTrades += 1
            position = 0
    if position == 1:
        netProfit += float(priceArray[-1]) - buyPrice
        numTrades += 1
    if (profitNum == 0):
        return {"Net Profit":netProfit, "Total Number Of Trades":numTrades, "Profitable Trades as a Percentage":0}
    return {"Net Profit":netProfit, "Total Number Of Trades":numTrades, "Profitable Trades as a Percentage":(profitNum/numTrades)*100}


connectionObj = Connection("SPGI","time_series_daily")
prices = connectionObj.get_close_prices()
spread = connectionObj.getSpread()
print(spread)
print(spread["max"] - spread["min"])
# print(SMACrossover(prices,3,5))
print(SMACrossover(prices,5,10))
print(SMACrossover(prices,20,50))
print(SMACrossover(prices,50,200))