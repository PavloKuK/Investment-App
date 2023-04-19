class Company:
    def __init__(self, assetType, name, description, exchange, country, sector, industry, address, marketCapitalization, dividentYield, eps, peratio, beta, weekHigh, weekLow, fiftyDayMovingAverage, twoHundredDayMovingAverage):
        self.assetType = assetType
        self.name = name
        self.description = description
        self.exchange = exchange
        self.country = country
        self.sector = sector
        self.industry = industry
        self.address = address
        self.marketCapitalization = marketCapitalization
        self.dividentYield = dividentYield
        self.eps = eps
        self.peratio = peratio
        self.beta = beta
        self.weekHigh = weekHigh
        self.weekLow = weekLow
        self.fiftyDayMovingAverage = fiftyDayMovingAverage
        self.twoHundredDayMovingAverage = twoHundredDayMovingAverage