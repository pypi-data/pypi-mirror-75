import logging

import numpy as np
import pandas as pd
from pandas import DataFrame
from tqdm import tqdm

from krider.bot_config import config, DEV_MODE
from krider.notifications.console_notifier import console_notifier
from krider.notifications.reddit_notifier import reddit_notifier
from krider.stock_store import stock_store
from krider.ticker_data import ticker_data
from krider.utils.report_generator import report_generator
from krider.utils.timing_decorator import timeit

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class VolumeAnalysisTask:
    @timeit
    def run_with(self, period, stocks=None):
        exchange_tickers: DataFrame = ticker_data.load_exchange_tickers()

        if stocks:
            selected_stocks = stocks.split(",")
            exchange_tickers = exchange_tickers[exchange_tickers.index.isin(selected_stocks)]

        collective_post = []

        for ticker, ticker_df in tqdm(exchange_tickers.iterrows()):
            logging.debug("Running analysis on {}".format(ticker))
            selected_data: DataFrame = stock_store.data_for_ticker(ticker, period)
            if selected_data.empty:
                continue

            if self._if_anomaly_found(selected_data):
                report = report_generator.prepare_output(ticker, selected_data.iloc[0])
                collective_post.append(report)

        logging.info("Total {} stocks found with usually high volume".format(len(collective_post)))

        content = dict(
            title="[Daily] High Volume Indicator",
            flair_id=config("HIGH_VOLUME_FLAIR"),
            body="\n".join(collective_post)
        )
        if DEV_MODE:
            console_notifier.send_notification(content)
        else:
            reddit_notifier.send_notification(content)
        return "All done"

    def _back_test_anomalies(self, df):
        mean = np.mean(df["Volume"])
        df["Volume_Activity"] = df["Volume"] > (10 * mean)
        logging.debug(df.where(df["Volume_Activity"] == True).dropna())

    def _if_anomaly_found(self, df):
        mean = np.mean(df["Volume"])
        df["MeanVolume"] = mean
        previous_session_vol = df["Volume"].iloc[0]
        return previous_session_vol > (20 * mean)


volume_analysis_task = VolumeAnalysisTask()
