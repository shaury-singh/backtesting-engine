import os
from dotenv import load_dotenv
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

class connection:
    def __init__(self, stockName, DBName):
        self.__collection = stockName
        self.__databaseName = DBName
        self.__client = MongoClient(os.getenv("URI"), server_api=ServerApi('1'))
    def addDataIntoDatabase(self):
        db = self.__client[self.__databaseName]
        collection = db[self.__collection]
        if (self.__databaseName == "time_series_daily"):
            fetch_URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.__collection}&interval=5min&apikey={os.getenv("APIKEY")}'
            r = requests.get(fetch_URL)
            data = r.json()
            for date in data["Time Series (Daily)"]:
                priceInfo = {date:data["Time Series (Daily)"][date]}
                query = {f"{date}":{"$exists": True}}
                doc = collection.find_one(query)
                if (doc):
                    continue
                else:
                    result = collection.insert_one(priceInfo)
                    print(priceInfo)
                    print("Inserted ID:", result.inserted_id)
        if (self.__databaseName == "time_series_monthly"):
            fetch_URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={self.__collection}&interval=5min&apikey={os.getenv("APIKEY")}'
            r = requests.get(fetch_URL)
            data = r.json()
            for date in data["Monthly Time Series"]:
                priceInfo = {date:data["Monthly Time Series"][date]}
                query = {f"{date}":{"$exists": True}}
                doc = collection.find_one(query)
                if (doc):
                    continue
                else:
                    result = collection.insert_one(priceInfo)
                    print(priceInfo)
                    print("Inserted ID:", result.inserted_id)

connectionObj = connection("WMT","time_series_daily")
connectionObj.addDataIntoDatabase()