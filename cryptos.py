from credentials import Credentials
import pandas as pd
from binance.client import Client

client = Client(Credentials.api_key, Credentials.api_secret)

start_date = '1 Jan, 2023'

def main() :
    info = client.get_exchange_info()
    symbols = [symbol['symbol'] for symbol in info['symbols'] if symbol['symbol'][-4:] == 'USDT']
    symbols = symbols[:10]

    c = 0
    for symbol in symbols :
        c += 1
        print(f"{c}/{len(symbols)} {symbol}")
        

        df = getData(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY, start_date=start_date)
        if isinstance(df, int) : continue

        df.to_csv(f"data/cryptos/{symbol}.csv")

def getData(symbol, interval, start_date) :
    try :
        data = client.get_historical_klines(symbol=symbol, interval=interval, start_str=start_date)
    except :
        print("Sin datos")
        return -1

    df = pd.DataFrame(data, columns=['DATE','OPEN','HIGH','LOW','CLOSE','A','VOLUME','B','C','D','E','F'])
    if df.empty : 
        print("Sin datos")
        return -1
    df = df[['DATE','OPEN','HIGH','LOW','CLOSE','VOLUME']]
    df['DATE'] = pd.to_datetime(df['DATE'], unit='ms')
    for i in ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'] :
        df[i] = df[i].astype(float)
    df = df.set_index(['DATE'], drop=True)

    return df

main()
