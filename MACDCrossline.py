from Engine import Engine
from DBconnection import Connection
class MACDIndicator(Engine):
    def __init__(self, totalCapital, stopLoss, fees):
        self.__totalCapital = totalCapital
        self.__stopLoss = stopLoss
        self.__fees = fees
    
    def MACDCrossover(self, fastTimePeriod, slowTimePeriod, signalTimePeriod, priceArray):
        fastEMA = self.EMA(fastTimePeriod, priceArray)
        slowEMA = self.EMA(slowTimePeriod, priceArray)
        MACDLine = self.EMADifference(fastEMA, slowEMA)
        signalLine = self.EMA(signalTimePeriod, MACDLine)
        crossOvers = 0
        totalShares = 0
        avgBuyPrice = 0
        sharesBought = 0
        totalTrades = 0
        capital = self.__totalCapital
        totalProfitableTrades = 0
        i = 1
        while i < len(MACDLine) - 1:
            if (MACDLine[i] is None or signalLine[i] is None or MACDLine[i-1] is None or signalLine[i-1] is None):
                i += 1
                continue
            if (MACDLine[i-1] <= signalLine[i-1] and MACDLine[i] > signalLine[i] and MACDLine[i] < 0):
                crossOvers += 1
                if (capital >= priceArray[i+1]):
                    sharesBought = int(capital/priceArray[i+1])
                    avgBuyPrice = (avgBuyPrice*totalShares + priceArray[i+1]*sharesBought)/(totalShares + sharesBought)
                    totalShares += sharesBought
                    summary =  self.stoploss(i+1,self.__stopLoss,priceArray,avgBuyPrice,totalShares)
                    totalTrades += 1
                    totalShares = 0
                    sharesBought = 0
                    capital -= summary["loss"]
                    if (summary["loss"] < 0):
                        totalProfitableTrades += 1
                    i = summary["sellIndex"]
                    continue
                
            i += 1
        return {"Net Profit":capital - self.__totalCapital,"Total Trades":totalTrades,"Proftable Trades":totalProfitableTrades}

MACDObj = MACDIndicator(500,1,0.01)
connectionObj = Connection("IBM","time_series_daily")
priceArray = connectionObj.get_close_prices()
print(MACDObj.MACDCrossover(12,26,9,priceArray))