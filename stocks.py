import pandas as pd
import datetime as dt
import yfinance as yf
from finta import TA
from clases.asset import Asset

# PARAMENTERS
Fecha_Inicio = pd.to_datetime("2020-01-01")
Fecha_Final = pd.to_datetime(dt.datetime.today())
iSMA1_Period = 200
iSMA2_Period = 50

Asset.iSMA1_Period, Asset.iSMA2_Period = iSMA1_Period, iSMA2_Period

#symbols = pd.read_csv('assets/symbols.csv')
#symbols = symbols['Symbol'].to_list()[0:2]
symbols = ['AAPL']

signals = pd.DataFrame(
    columns=['DATE', 'OPEN', 'iSMA1', 'iSMA2']
)
c = 1
for symbol in symbols :
    print(f"{c}/{len(symbols)} {symbol}")

    asset = Asset(symbol=symbol, start=Fecha_Inicio, end=Fecha_Final)
    if not asset.ready : continue
    
    asset.df.to_csv(f'data/stocks/{asset.symbol}.csv')

    c+=1

    max_indicator_period = max(iSMA1_Period, iSMA2_Period)

    # TRADE CALCULATION
    for i in range(len(asset.df)) :
        if i <= max_indicator_period + 1 : continue

        # Buy when the SMA2 crosses above SMA1
        if asset.iSMA2[i] >= asset.iSMA1[i] and asset.iSMA2[i - 1] < asset.iSMA1[i - 1] :
            signals.loc[len(signals)] = [asset.df.index[i], asset.df.OPEN[i], asset.iSMA1[i], asset.iSMA2[i]]
    
signals.to_csv('Señales.csv')