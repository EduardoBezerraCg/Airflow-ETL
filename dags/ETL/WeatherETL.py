import requests
from datetime import datetime
import pandas as pd


def extract_crypto_data():
    url = f"https://api4.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()
    df= pd.DataFrame(data)
    return df

extract_crypto_data()