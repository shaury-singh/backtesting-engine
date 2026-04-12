from Engine import Engine
from DBconnection import Connection
class MACDIndicator(Engine):
    def __init__(self, totalCapital, stopLoss, fees):
        self.__totalCapital = totalCapital
        self.__currentCapital = self.__totalCapital
        self.__stopLoss = stopLoss
        self.__fees = fees
    
    def MACDCrossover(self, fastTimePeriod, slowTimePeriod, signalTimePeriod, priceArray, investProfits=False):
        fastEMA = self.EMA(fastTimePeriod, priceArray)
        slowEMA = self.EMA(slowTimePeriod, priceArray)
        MACDLine = self.EMADifference(fastEMA, slowEMA)
        signalLine = self.EMA(signalTimePeriod, MACDLine)
        position = 0
        buyPrices = []
        sellPrices = []
        currBuyPrice = 0
        netPL = 0
        for i in range(1,len(MACDLine)-1):
            if (MACDLine[i] is None or signalLine[i] is None or MACDLine[i-1] is None or signalLine[i-1] is None):
                continue
            if (position == 0 and MACDLine[i-1] <= signalLine[i-1] and MACDLine[i] > signalLine[i] and MACDLine[i] < 0):
                buyPrices.append(priceArray[i+1])
                currBuyPrice = priceArray[i+1]
                position = 1
            if (position == 1 and MACDLine[i-1] >= signalLine[i-1] and MACDLine[i] < signalLine[i] and MACDLine[i] > 0):
                sellPrices.append(priceArray[i+1])
                netPL += priceArray[i+1] - currBuyPrice
                position = 0
        if (len(buyPrices) > len(sellPrices)):
            netPL += priceArray[len(priceArray)-1] - currBuyPrice
        return netPL

MACDObj = MACDIndicator(1000,0.1,0.01)
connectionObj = Connection("TSLA","time_series_daily")
priceArray = connectionObj.get_close_prices()
print(MACDObj.MACDCrossover(12,26,9,priceArray))