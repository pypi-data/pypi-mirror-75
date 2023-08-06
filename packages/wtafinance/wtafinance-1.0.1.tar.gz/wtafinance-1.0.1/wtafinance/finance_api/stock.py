import requests,json
import pandas as pd
from functools import partial


class DataApi(object):
    _instance = None

    def __init__(self,token, timeout=15):
        self._token = token
        self._timeout = timeout
        self.http_url = "http://106.53.251.60/app_finance/apidata"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            return cls._instance
        else:
            return cls._instance


    def query(self,api_name, **kwargs):
        data={
            "token":self._token,
            "api_name":api_name,
            "params":kwargs
        }
        res = requests.get(self.http_url,json=data, timeout=60)
        if res:
            result = json.loads(res.text)
            if result['code'] != 0:
                raise Exception(result['msg'])
            data = result['data']
            if len(data) == 0:
                return pd.DataFrame()
            columns = data[0].keys()
            items = data
            return pd.DataFrame(items, columns=columns)
        else:
            return pd.DataFrame()

    def __getattr__(self, api_name,**kwargs):
        return partial(self.query,api_name)
