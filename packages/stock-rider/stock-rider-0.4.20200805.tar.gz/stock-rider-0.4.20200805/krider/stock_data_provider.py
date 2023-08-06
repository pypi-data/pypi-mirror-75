import logging

import yfinance


class StockDataProvider:
    def download_between_dates(self, ticker, interval, start, end):
        logging.debug("Requesting ticker {}".format(ticker))
        opts = dict(
            tickers=ticker, interval=interval, start=start, end=end, progress=False
        )
        return yfinance.download(**opts)

    def download_for_period(self, ticker, period, interval):
        logging.debug("Requesting ticker {}".format(ticker))
        opts = dict(tickers=ticker, interval=interval, period=period, progress=False)
        return yfinance.download(**opts)

    def check(self, ticker):
        return self.download_for_period(ticker, "1d", "1d")


stock_data_provider = StockDataProvider()
