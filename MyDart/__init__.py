import zipfile
import os
import json
from MyDart.lib.api import API

class DART(API):
    from MyDart.finance import corp_code
    from MyDart.finance import corp_finance
    from MyDart.finance import corp_finance_all
    from MyDart.finance import save_corp_finance
    from MyDart.finance import get_corp_finance
    from MyDart.finance import get_corp_price
    from MyDart.finance import save_corp_price
    from MyDart.finance import get_corp_stocknum
    from MyDart.finance import save_corp_stock_num
    from MyDart.finance import corp_stock_quantity
    

    def __init__(self, bsns_year, base_url=None) -> None:
        if not base_url:
            base_url = 'https://opendart.fss.or.kr'
        key = self._load_key()
        self.bsns_year = bsns_year
        self.base_path = "./data"
        super().__init__(key, base_url)
        
    def _load_key(self):
        data_path = "./data/key.txt"
        with open(data_path, 'r') as f:
            return f.readline()

    def save_corp_code(self, reset = 0):
        if reset == 1 or not os.path.exists(self.base_path + "/CORPCODE.xml"):
            data = self.corp_code()
            self._save_file("/CORPCODE.zip",data)
            self._unzip_file("/CORPCODE.zip")

    
    def _unzip_file(self, zip_path):
        with zipfile.ZipFile(self.base_path + zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.base_path)
        os.remove(self.base_path + zip_path)

    def _save_file(self, path, data):
        if isinstance(data, dict):
            with open(self.base_path + path, 'w') as f:
                json.dump(data, f)
        else:
            with open(self.base_path + path, 'wb') as f:
                f.write(data)
 

