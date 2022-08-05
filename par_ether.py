import time
import datetime
import requests
import sqlite3
import pandas as pd

import config


def get_histor_data():
    try:
        conn = sqlite3.connect("ether_data.db")
        bd_data = pd.read_sql("SELECT * FROM ether_data", conn)
        end_date = bd_data["date"][bd_data.last_valid_index()]
        conn.close()
    except:
        end_date = "06-08-2015"

    url = "https://coingecko.p.rapidapi.com/coins/ethereum/history"

    start= datetime.datetime.strptime(datetime.date.today().strftime("%d-%m-%Y"), "%d-%m-%Y")
    end = datetime.datetime.strptime(end_date, "%d-%m-%Y")

    dates = [(datetime.date.today() - datetime.timedelta(days=x)).strftime('%d-%m-%Y') for x in range((start - end).days)][::-1]
    hist_info = []
    for date in dates:
        querystring = {"date":f"{date}","localization":"false"}

        headers = {
            "X-RapidAPI-Key": config.TOKEN,
            "X-RapidAPI-Host": "coingecko.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        res_jsn = response.json()
        date_jsn = {"date":f"{date}"}
        hist_info.append({**date_jsn, **res_jsn})
    
    return hist_info


def save_to_db(all_data):
    df = pd.json_normalize(all_data)
    conn = sqlite3.connect("ether_data.db")
    df.to_sql("ether_data", conn, if_exists="append")
    conn.close()


if __name__ == "__main__":
    start = time.perf_counter()
    all_data = get_histor_data()
    save_to_db(all_data)

    fin = time.perf_counter() - start
    print(fin)
