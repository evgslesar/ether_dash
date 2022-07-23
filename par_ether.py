import json
import time
import datetime
import requests
import config


def get_histor_data():

    url = "https://coingecko.p.rapidapi.com/coins/ethereum/history"

    dates = [(datetime.date.today() - datetime.timedelta(days=x)).strftime('%d-%m-%Y') for x in range(0, 2762)]
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

    
    with open('ether_data.json', 'a', encoding='utf-8') as f:
        json.dump(hist_info, f, indent=4, ensure_ascii=False)

    return hist_info


if __name__ == '__main__':
    start = time.perf_counter()
    get_histor_data()

    fin = time.perf_counter() - start
    print(fin)
