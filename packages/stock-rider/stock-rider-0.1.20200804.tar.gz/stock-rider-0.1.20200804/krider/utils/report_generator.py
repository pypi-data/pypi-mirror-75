from datetime import datetime
from urllib import parse

from pandas import DataFrame


class ReportGenerator:
    def prepare_output(self, ticker, df: DataFrame):
        session_dt = datetime.strptime(df["Datetime"], "%Y-%m-%d %H:%M:%S.%f").date()
        session_volume = float(df["Volume"])
        mean_volume = float("{:.0f}".format(df["MeanVolume"]))
        ticker_exchange = df["Exchange"]
        ticker_exchange_symbol = parse.quote_plus("{}:{}".format(ticker_exchange, ticker))
        md_post = f"""
## {ticker}

**Date:** {session_dt}

**Volume:** {session_volume:,.0f}

**Mean Volume:** {mean_volume:,.0f}

[Trading View](https://www.tradingview.com/chart/?symbol={ticker_exchange_symbol}) | 
[Robinhood](https://robinhood.com/stocks/{ticker})

---

        """
        return md_post


report_generator = ReportGenerator()
