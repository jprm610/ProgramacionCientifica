class Asset :
    iSMA1_Period = None
    iSMA2_Period = None

    def __init__(self, symbol, start, end) -> None:
        import finta as TA

        self.symbol = symbol
        self.start = start
        self.end = end
        self.ready = True
        self.df = None
        self.iSMA1 = None
        self.iSMA2 = None

        returned = self.download()
        if returned == None : 
            self.ready = False
            return
        
        returned = self.calculateIndicators()
        if returned == None : 
            self.ready = False
            return

    def download(self) :
        import yfinance as yf

        try :
            df = yf.download(self.symbol, start=self.start, end=self.end)
        except :
            print("Sin datos")
            return None

        df.columns = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'ADJ CLOSE', 'VOLUME']

        if df.empty : return None

        self.df = df

        return 0
    
    def calculateIndicators(self) :
        from finta import TA

        if self.iSMA1_Period == None or self.iSMA2_Period == None :
            print("SMA periods not defined!")
            return None
        self.iSMA1 = TA.SMA(self.df, self.iSMA1_Period)
        self.iSMA2 = TA.SMA(self.df, self.iSMA2_Period)
        return 0
    