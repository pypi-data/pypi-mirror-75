import requests


def getNSE50():
    result = {}
    result['exchange'] = 'NSE'
    tickers = []
    n50_headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Host": "www1.nseindia.com",
        "Referer": "https://www1.nseindia.com/live_market/dynaContent/live_watch/equities_stock_watch.htm",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    n50data = requests.get(
        "https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json", headers=n50_headers)
    for ticker in n50data.json()['data']:
        tickers.append(ticker['symbol'])
    result['Tickers'] = tickers
    return result


def getBSE30():
    result = {}
    result['exchange'] = 'BSE'
    tickers = []
    bse30_headers = {
        "authority": "api.bseindia.com",
        "method": "GET",
        "path": "/BseIndiaAPI/api/GetMktData/w?ordcol=TT&strType=index&strfilter=S%26P+BSE+SENSEX",
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://www.bseindia.com",
        "referer": "https://www.bseindia.com/markets/equity/EQReports/MarketWatch.html?index_code=16",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    bse30data = requests.get(
        "https://api.bseindia.com/BseIndiaAPI/api/GetMktData/w?ordcol=TT&strType=index&strfilter=S%26P+BSE+SENSEX", headers=bse30_headers)
    for ticker in bse30data.json()['Table']:
        tickers.append(ticker['scripname'])
    result['Tickers'] = tickers
    return result