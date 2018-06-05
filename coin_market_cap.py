from bs4 import BeautifulSoup
from collections import OrderedDict
import requests
import pandas as pd
import numpy  as np
from pandas import DataFrame
import datetime
from tabulate import tabulate

BITCOIN = 'bitcoin'
ETHEREUM = 'ethereum'
RIPPLE = 'ripple'
BITCOINCASH = 'bitcoin-cash'
EOS = 'eos'
LITECOIN = 'litecoin'
CARDANO = 'cardano'
STELLAR = 'stellar'
IOTA = 'iota'
NEO = 'neo'
TRON = 'tron'
ZCASH = 'zcash'


def alt(func, val, message=None):
    try:
        return func()
    except:
        if message:
            print(message)
        return val


def get_daily_100():
    HOME = "https://coinmarketcap.com"
    resp = requests.get(HOME)
    if resp.status_code != 200:
        raise requests.RequestException()
    soup = BeautifulSoup(resp.content, features='html.parser')
    coin_elements = soup.find("tbody").findAll("tr")
    data = OrderedDict()
    columns = [
        "coin-name", "price", "percent-change",
        "market-cap (b)", "cs (b)", "volume (b)"
    ]

    for c in columns:
        data[c] = []

    for coin_element in coin_elements:
        find_coin_name = lambda :coin_element.find("td", class_="currency-name").get("data-sort")
        coin_name = alt(find_coin_name, "UNFOUND")
        find_price = lambda :coin_element.find("a", class_="price").get("data-usd")
        price = alt(find_price, np.nan)
        find_percent_change = lambda :coin_element.find("td", attrs='percent-change').get("data-sort")
        percent_change = alt(find_percent_change, np.nan)
        find_market_cap = lambda : coin_element.find("td", class_="market-cap").get("data-sort")
        market_cap = alt(find_market_cap, np.nan)
        find_circulating_supply = lambda :coin_element.find("td", class_="circulating-supply").get("data-sort")
        circulating_supply = alt(find_circulating_supply, np.nan)
        find_volume = lambda :coin_element.find("a", class_="volume").get("data-usd")
        volume = alt(find_volume, np.nan)

        data[columns[0]].append(coin_name)
        data[columns[1]].append(float(price))
        data[columns[2]].append(float(percent_change) / 100.0)
        data[columns[3]].append(float(market_cap) / 1000_000_000)
        data[columns[4]].append(float(circulating_supply) / 1000_000_000)
        data[columns[5]].append(float(volume) / 1000_000_000)

    df = DataFrame.from_dict(data)
    df[columns[1]] = df[columns[1]].round(4)
    df[columns[2]] = (df[columns[2]] * 100).round(2)
    df[columns[3]] = df[columns[3]].round(3)
    df[columns[4]] = df[columns[4]].round(3)
    df[columns[5]] = df[columns[5]].round(3)
    df['vol2cap'] = (df[columns[5]] / df[columns[3]]).round(3)
    return df


def display(x):
    print(tabulate(x, headers='keys', tablefmt='psql'))


def show_daily_100():
    df = get_daily_100()
    display(df)


def get_coin_history(name, start=None, end=None):
    URL = "https://coinmarketcap.com/currencies/{}/historical-data/?start={}&end={}"
    if start or end:
        raise NotImplementedError()

    today = datetime.datetime.today()
    today_str = f"{today.year}{str(today.month).zfill(2)}{str(today.day).zfill(2)}"
    start_date_str = f"{today.year-1}{str(today.month).zfill(2)}{str(today.day).zfill(2)}"
    URL = URL.format(name, start_date_str, today_str)
    print(URL)
    resp = requests.get(URL)
    if resp.status_code != 200:
        raise requests.RequestException()
    soup = BeautifulSoup(resp.content, features='html.parser')
    tbl = soup.find("tbody").findAll("tr", class_='text-right')
    lst = []
    for row_element in tbl:
        row_data = [x.get("data-format-value") if x.get("data-format-value") else x.text for x in
                    row_element.findAll("td")]
        for i in range(1, len(row_data)):
            try:
                row_data[i] = float(row_data[i])
            except ValueError:
                row_data[i] = np.nan
        lst.append(row_data)
    columns = ['date', 'open', 'close', 'lowest', 'highest', 'volume (b)', 'market-cap (b)']
    df = DataFrame(lst, columns=columns)
    df[columns[5]] = df[columns[5]] / 1000_000_000
    df[columns[6]] = df[columns[6]] / 1000_000_000
    df['date'] = pd.to_datetime(df['date'])
    for c in columns[1:]:
        df[c] = df[c].round(3)
    return df


def show_coin_history(name, start=None, end=None):
    df = get_coin_history(name, start=start, end=end)
    display(df)


if __name__ == '__main__':
    #result = get_coin_history(CARDANO)
    # print(display(result))
    result = get_daily_100().head(40).sort_values("vol2cap", ascending=False)
    display(result)
    show_coin_history(CARDANO)
