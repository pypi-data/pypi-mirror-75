from wtafinance.finance_api import stock


def wta_api(token):
    instance = stock.DataApi(token)
    return instance