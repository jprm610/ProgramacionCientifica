import pandas as pd
import datetime as dt
import yfinance as yf

#symbols = pd.read_csv('assets/symbols.csv')
#symbols = symbols['Symbol'].to_list()[0:2]
symbols = ['AAPL']

fecha_inicio = pd.to_datetime("2023-09-01")
fecha_final = pd.to_datetime(dt.datetime.today())

umbral = 0.02

signals = pd.DataFrame(
    columns=['DATE', 'OPEN', 'CLOSE', 'CHANGE']
)
c = 1
for symbol in symbols :
    print(f"{c}/{len(symbols)} {symbol}")
    try :
        df = yf.download(symbol, start=fecha_inicio, end=fecha_final)
    except :
        print("Sin datos")
        continue

    df.to_csv(f'data/stocks/{symbol}.csv')

    c+=1

    for i in range(len(df)) :
        cambio = (df.Close[i] - df.Open[i])/df.Open[i]
        if abs(cambio) > umbral :
            signals.loc[len(signals)] = [df.index[i], df.Open[i], df.Close[i], cambio] 
    
signals.to_csv('Señales.csv')