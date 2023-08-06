import logging
from datetime import datetime, timedelta

import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, OperationalError

skip_days = timedelta(days=2)


class StockStore:
    def __init__(self):
        db_engine = create_engine("sqlite:///stockstore.db", echo=False)
        self.db_connection = db_engine.connect()

    def save(self, ticker, data: DataFrame):
        self._create_table_if_required(ticker)
        try:
            data.to_sql(
                ticker,
                self.db_connection,
                if_exists="append",
                index=True,
                index_label="Datetime",
            )
        except IntegrityError as e:
            logging.warning("Unable to save data: {}".format(e.args[0]))

        logging.debug("Saving ticker: {} with data: {}".format(ticker, data.shape))

    def data_for_ticker(self, ticker, period):
        sql = f"""
        select * from \"{ticker}\" order by Datetime desc limit {period};
        """
        try:
            pd_sql = pd.read_sql(sql, self.db_connection)
            return pd.DataFrame(pd_sql)
        except OperationalError as e:
            logging.debug("Error when reading data for {} - {}".format(ticker, e.args[0]))
            return pd.DataFrame()

    def find_start_time(self, ticker, default_dt):
        last_entry = self.data_for_ticker(ticker, 1)
        start_time = default_dt if last_entry.empty else self._next_day(last_entry["Datetime"].loc[0])
        return start_time

    def _next_day(self, dt):
        last_entry_dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f")
        last_entry_dt += skip_days
        return last_entry_dt

    def _create_table_if_required(self, ticker):
        self.db_connection.execute(
            f"""
        CREATE TABLE IF NOT EXISTS "{ticker}" (
            "Datetime" TIMESTAMP PRIMARY KEY, 
            "Open" FLOAT, 
            "High" FLOAT, 
            "Low" FLOAT, 
            "Close" FLOAT, 
            "Adj Close" FLOAT, 
            "Volume" BIGINT,
            "Exchange" TEXT
        )
        """
        )


stock_store = StockStore()
