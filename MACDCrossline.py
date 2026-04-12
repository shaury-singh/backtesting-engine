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
        buy_prices_array = []
        position = 0
        totalShares = 0
        averageBuyPrice = 0
        for i in range(1,len(MACDLine)-1):
            if (MACDLine[i] is None or signalLine[i] is None or MACDLine[i-1] is None or signalLine[i-1] is None):
                continue
            if (position == 0 and MACDLine[i-1] <= signalLine[i-1] and MACDLine[i] > signalLine[i] and MACDLine[i] < 0): # buy condition
                shares_bought_in_this_trade = self.__currentCapital/priceArray[i+1]
                self.__currentCapital = self.__currentCapital - (priceArray[i+1]*shares_bought_in_this_trade)
                averageBuyPrice = (averageBuyPrice*totalShares + priceArray[i+1]*shares_bought_in_this_trade)/(totalShares+shares_bought_in_this_trade)
                totalShares += shares_bought_in_this_trade
                buy_prices_array.append({"Shares":shares_bought_in_this_trade, "buyPrice":priceArray[i+1]})
                position = 1
                loss = self.stoploss(i, self.__stopLoss, priceArray, averageBuyPrice, totalShares)
                if (loss == 0):
                    return self.__currentCapital - self.__totalCapital + (priceArray[len(priceArray)-1]*totalShares - averageBuyPrice*totalShares)
                else:
                    totalShares = 0
                    self.__currentCapital = self.__totalCapital - loss
                    averageBuyPrice = 0
                    buy_prices_array.clear()
                    position = 0
            if (position == 1 and MACDLine[i-1] >= signalLine[i-1] and MACDLine[i] < signalLine[i] and MACDLine[i] > 0): # sell condition
                if (totalShares > 0):
                    pl = (priceArray[i+1]*totalShares - averageBuyPrice*totalShares)
                    totalShares = 0
                    averageBuyPrice = 0
                    self.__currentCapital += pl
                    position = 0
                else:
                    continue
        return self.__currentCapital - self.__totalCapital

MACDObj = MACDIndicator(100000,10,0.01)
connectionObj = Connection("TSLA","time_series_daily")
priceArray = connectionObj.get_close_prices()
print(MACDObj.MACDCrossover(12,26,9,priceArray))