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
        self.__db = self.__client[self.__databaseName]
        self.__collectionObj = self.__db[self.__collection]
    def addDataIntoDatabase(self):
        if (self.__databaseName == "time_series_daily"):
            fetch_URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.__collection}&interval=5min&apikey={os.getenv("APIKEY")}'
            r = requests.get(fetch_URL)
            data = r.json()
            for date in data["Time Series (Daily)"]:
                priceInfo = {date:data["Time Series (Daily)"][date]}
                query = {f"{date}":{"$exists": True}}
                doc = self.__collectionObj.find_one(query)
                if (doc):
                    continue
                else:
                    result = self.__collectionObj.insert_one(priceInfo)
                    print(priceInfo)
                    print("Inserted ID:", result.inserted_id)
        if (self.__databaseName == "time_series_monthly"):
            fetch_URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={self.__collection}&interval=5min&apikey={os.getenv("APIKEY")}'
            r = requests.get(fetch_URL)
            data = r.json()
            for date in data["Monthly Time Series"]:
                priceInfo = {date:data["Monthly Time Series"][date]}
                query = {f"{date}":{"$exists": True}}
                doc = self.__collectionObj.find_one(query)
                if (doc):
                    continue
                else:
                    result = self.__collectionObj.insert_one(priceInfo)
                    print(priceInfo)
                    print("Inserted ID:", result.inserted_id)
    def getPrices(self):
        print("Fetching Data From The Database...")
        if (self.__databaseName == "time_series_daily"):
            dict = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
            price_array = []
            for k in range(25,27):
                for i in range (1,13):
                    for j in range (1,dict[i]+1):
                        month = f"{i}"
                        date = f"{j}"
                        year = f"20{k}"
                        if (i%10 == i):
                            month = f"0{i}"
                        if (j%10 == j):
                            date = f"0{j}"
                        query = {f"{year}-{month}-{date}":{"$exists": True}}
                        doc = self.__collectionObj.find_one(query)
                        if (doc):
                            price_array.append(doc[f"{year}-{month}-{date}"]["4. close"])
        return price_array