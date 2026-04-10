import os
import yfinance as yf
# yf.shared._requests = None
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

class Connection:
    def __init__(self, stockName, DBName):
        self.collection_name = stockName
        self.database_name = DBName
        self.client = MongoClient(os.getenv("URI"), server_api=ServerApi('1'))
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]
        
    def add_daily_data(self, period="10y"):
        ticker = yf.Ticker(self.collection_name)
        df = ticker.history(period=period)
        print("Fetching data from yfinance...")
        for date, row in df.iterrows():
            date_str = str(date.date())
            price_data = {
                "date": date_str,
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"])
            }
            if self.collection.find_one({"date": date_str}):
                continue
            result = self.collection.insert_one(price_data)
            print(f"Inserted {date_str} | ID: {result.inserted_id}")

    def get_close_prices(self):
        print("Fetching close prices from DB...")
        cursor = self.collection.find().sort("date", 1)
        self.__prices = [doc["close"] for doc in cursor]
        return self.__prices
    
    def getSpread(self):
        maxPrice = self.__prices[0]
        minPrice = self.__prices[0]
        for price in self.__prices:
            if (maxPrice < price):
                maxPrice = price
            if (minPrice > price):
                minPrice = price
        return {"max":maxPrice,"min":minPrice}


    def get_full_data(self):
        print("Fetching full dataset from DB...")
        cursor = self.collection.find().sort("date", 1)
        data = []
        for doc in cursor:
            data.append({
                "date": doc["date"],
                "open": doc["open"],
                "high": doc["high"],
                "low": doc["low"],
                "close": doc["close"],
                "volume": doc["volume"]
            })
        return data

    def clear_data(self):
        self.collection.delete_many({})
        print("Collection cleared")

# connectionObj = Connection("WMT","time_series_daily")
# connectionObj.add_daily_data()