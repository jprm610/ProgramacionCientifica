import pandas as pd

class Trade :
    RiskUnit = None
    PercentageInRisk = None
    CommissionPercentage = None
    TradesGlobal = pd.DataFrame(
        columns=['TRADE TYPE', 'ASSET', 'SHARES', 'OUTCOME', 'Y', 'Y%', 'ENTRY DATE', 'EXIT DATE', 'ENTRY PRICE', 'EXIT PRICE', 'MAX', 'MIN', 'IS SIGNAL', 'CLOSE TOMORROW']
    )
    
    def __init__(self, tradeType, asset, candle) -> None:
        self.tradeType = tradeType
        self.asset = asset
        self.sharesToTrade = None
        self.entryPrice = candle.OPEN
        self.entryDate = candle.name
        self.exitPrice = None
        self.exitDate = None
        self.minPrice = candle.LOW
        self.maxPrice = candle.HIGH
        self.isSignal = None
        self.closeTomorrow = None

        currentAvgLose = self.entryPrice * (Trade.PercentageInRisk / 100)
        self.sharesToTrade = round(abs(Trade.RiskUnit / currentAvgLose), 1)
        if self.sharesToTrade == 0 : 
            self.tradeType = None
            return
        
    def exit(self, candle, isSignal=False, closeTomorrow=False) :
        self.exitPrice = candle.CLOSE
        self.exitDate = candle.name
        self.closeTomorrow = closeTomorrow
        self.isSignal = isSignal
        if candle.LOW < self.minPrice : self.minPrice = candle.LOW
        if candle.HIGH > self.maxPrice : self.maxPrice = candle.HIGH
        y = self.exitPrice - self.entryPrice
        y_perc = y / self.entryPrice * 100
        outcome = y * self.sharesToTrade

        Trade.TradesGlobal.loc[len(Trade.TradesGlobal)] = [
            self.tradeType, self.asset, self.sharesToTrade, 
            outcome, y, y_perc, 
            self.entryDate, self.exitDate, 
            self.entryPrice, self.exitPrice, 
            self.maxPrice, self.minPrice, 
            self.isSignal, self.closeTomorrow
        ]

    @classmethod
    def export(cls, filename="trades.csv") :
        cls.TradesGlobal.to_csv(filename)
