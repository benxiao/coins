import time
from pandas import DataFrame
import pandas as pd
import datetime
from datetime import datetime, timedelta
import numpy as np
from binance.client import Client


def read_config(fn):
    config = {}
    with open(fn,'r') as fp:
        for line in fp:
            if line is None:
                break
            k, v = [x.strip() for x in line.split('=')]
            config[k] = v
    return config


def date2ts(y, m, d):
    d = datetime(y, m, d)
    return d.timestamp() * 1000


def get_historical_klines(symbol, interval, start_time_stamp, end_time_stamp, **config):
    """Get Historical Klines from Binance
    See dateparse docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/
    If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    :param symbol: Name of symbol pair e.g BNBBTC
    :type symbol: str
    :param interval: Biannce Kline interval
    :type interval: str
    :param start_str: Start date string in UTC format
    :type start_str: str
    :param end_str: optional - end date string in UTC format
    :type end_str: str
    :return: list of OHLCV values
    """
    inteval2timeframe = {
        '1m': 60000,
        '5m': 300000
    }

    # create the Binance client, no need for api key
    apiKey = config['apiKey']
    secretKey = config['secretKey']
    client = Client(apiKey, secretKey)

    # init our list
    output_data = []

    # setup the max limit (I think the limit is 500), so do be careful
    limit = 1000

    # convert interval to useful value in seconds
    # timeframe = interval_to_milliseconds(interval)

    # convert our date strings to milliseconds
    start_ts = int(start_time_stamp)

    # if an end time was passed convert it
    end_ts = int(end_time_stamp)

    idx = 0
    # it can be difficult to know when a symbol was listed on Binance so allow start time to be before list date
    symbol_existed = False
    while True:
        # fetch the klines from start_ts up to max 500 entries or the end_ts if set
        temp_data = client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
            startTime=start_ts,
            endTime=end_ts
        )

        # handle the case where our start date is before the symbol pair listed on Binance
        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            # append this loops data to our output data
            output_data += temp_data

            # update our start timestamp using the last value in the array and add the interval timeframe
            start_ts = temp_data[len(temp_data) - 1][0] + inteval2timeframe[interval]
        else:
            # it wasn't listed yet, increment our start date
            start_ts += inteval2timeframe[interval]

        idx += 1
        # check if we received less than the required limit and exit the loop
        if len(temp_data) < limit:
            # exit the while loop
            break
    # print(output_data)
    return output_data


symbol = "BNBBTC"
columns = ["time", "open", "high", "low", "close", "volume", "time2", "quote_asset_volume", "trades", "base", "quote", "ignore"]
interval = Client.KLINE_INTERVAL_1MINUTE
config = read_config(".cred")
print(interval)


# open a file with filename including symbol, interval and start and end converted to milliseconds
# print(klines)
ts = date2ts(2018, 2, 1)
counter = 0

while 1:
    try:
        ts2 = ts + 3600 * 1000
        result = get_historical_klines(symbol, interval, ts, ts2, **config)
        time.sleep(4)
        df = DataFrame(result[1:])
        df.columns = columns
        date = datetime.fromtimestamp(ts/1000)
        fn = f"{symbol}-{date}.csv"
        print(f"write to {fn}")
        df.to_csv("data/bnb/"+fn)
        ts = ts2
        today = datetime.today()
        if date.month == today.month and date.day == today.day:
            break

        # more wait
        if counter == 100:
            time.sleep(500)
            counter = 0
        else:
            counter += 1
    except Exception as e:
        print("err:", type(e), e)
        # time.sleep(500)
        ts = ts2
        continue


# """
# [
#   [
#     1499040000000,      // Open time
#     "0.01634790",       // Open
#     "0.80000000",       // High
#     "0.01575800",       // Low
#     "0.01577100",       // Close
#     "148976.11427815",  // Volume
#     1499644799999,      // Close time
#     "2434.19055334",    // Quote asset volume
#     308,                // Number of trades
#     "1756.87402397",    // Taker buy base asset volume
#     "28.46694368",      // Taker buy quote asset volume
#     "17928899.62484339" // Ignore
#   ]
# ]
#
# """

#
