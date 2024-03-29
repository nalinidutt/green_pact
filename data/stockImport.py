import pandas as pd
import numpy as np
import yfinance as yf
import pymongo
from pymongo import MongoClient
import json
import certifi

myclient = pymongo.MongoClient("mongodb+srv://dkaimal3:Pass12345@greenpathcluster.5dz32tq.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
mydb = myclient["GreenPathDatabase"]
mycol = mydb["EditingGreenPathCollection"]

def extract_ticker(stockName):
    try:
        stock = yf.Ticker(stockName)
    except:
        newvalues1 = { "$set": { "Stock Price": "Not Available" } }
        newvalues2 = { "$set": { "Currency": "Not Available" } }
    else: 
        stPrice = stock.info['previousClose']
        curr = stock.info['currency']
        myquery = { "Stock Name" : stockName }
        newvalues1 = { "$set": { "Stock Price": stPrice } }
        newvalues2 = { "$set": { "Currency": curr } }
    mycol.update_one(myquery, newvalues1)
    mycol.update_one(myquery, newvalues2)

def refresh_db():
  for val in mycol.find({},{ "Stock Name": 1}):
    extract_ticker(val['Stock Name'])

refresh_db()

