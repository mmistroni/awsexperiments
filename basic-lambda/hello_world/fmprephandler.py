import requests
import os

def get_fmpkey():
    return os.environ['fmp_key']

def get_quote_for_ticker(ticker:str)-> dict:
    return {'ticker' : ticker, 'price':10}