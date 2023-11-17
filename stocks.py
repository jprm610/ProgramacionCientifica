import pandas as pd
import datetime as dt
import yfinance as yf
from finta import TA
from clases.asset import Asset
from clases.trade import Trade

# PARAMENTERS
Fecha_Inicio = pd.to_datetime("2020-01-01")
Fecha_Final = pd.to_datetime(dt.datetime.today())
iSMA1_Period = 100
iSMA2_Period = 20

Trade.RiskUnit = 60
Trade.PercentageInRisk = 6

SlopeToExit = 0

Asset.iSMA1_Period, Asset.iSMA2_Period = iSMA1_Period, iSMA2_Period

# Se obtienen los símbolos presentes en el archivo CSV.
symbols = pd.read_csv('assets/symbols.csv')
symbols = symbols['Symbol'].to_list()

c = 1
for symbol in symbols :
    print(f"{c}/{len(symbols)} {symbol}")
    c += 1

    asset = Asset(symbol=symbol, start=Fecha_Inicio, end=Fecha_Final)
    if not asset.ready : continue
    
    asset.df.to_csv(f'data/stocks/{asset.symbol}.csv')

    max_indicator_period = max(iSMA1_Period, iSMA2_Period)

    # TRADE CALCULATION
    for i in range(len(asset.df)) :
        if i <= max_indicator_period + 1 : continue

        # Buy when the SMA2 crosses above SMA1
        if (asset.iSMA2[i] >= asset.iSMA1[i] and 
            asset.iSMA2[i - 1] < asset.iSMA1[i - 1]) :

            # SIGNALS
            if i == len(asset.df) - 1 :
                trade = Trade(tradeType='Long', asset=symbol, candle=asset.df.iloc[i])
                trade.exit(candle=asset.df.iloc[i], isSignal=True)

            # BACKTESTING
            else :
                trade = Trade(tradeType='Long', asset=symbol, candle=asset.df.iloc[i + 1])
                newDf = asset.df.loc[asset.df.index >= asset.df.index[i]]
                for j in range(len(newDf)) :
                    if newDf.iloc[j].LOW < trade.minPrice : trade.minPrice = newDf.iloc[j].LOW
                    if newDf.iloc[j].HIGH > trade.maxPrice : trade.maxPrice = newDf.iloc[j].HIGH

                    m = (asset.iSMA2[i + j] - asset.iSMA2[i + j - 1])/asset.iSMA2[i + j]
                    if m < SlopeToExit :
                        if j == len(newDf) - 1 :
                            trade.exit(candle=newDf.iloc[j], closeTomorrow=True)
                        else :
                            trade.exit(candle=newDf.iloc[j + 1])
                        break
                    
                    if j == len(newDf) - 1 :
                        trade.exit(candle=newDf.iloc[j])
    
Trade.export()
