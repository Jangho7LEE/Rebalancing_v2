import zipfile
import os
import json
from MyDart.lib.api import API

class DART(API):
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

    def save_corp_code(self):
        data = self.corp_code()
        self._save_file("/CORPCODE.zip",data)
        self._unzip_file("/CORPCODE.zip")

    def get_corp_finance(self,corp_code_list, reset = 0):
        '''
        get_corp_finance는 list에 존재하는 기업의 재무재표를 가져와 stock_dic에 저장한다.
        input: 
            reset: 0) data/finance에 있는 기업은 가져오지 않는다
                   1) 모든 기업의 재무재표를가져온다
        '''
        if reset == 0:
            saved_corp_code_list = os.listdir(self.base_path + "/finance")
            target_list = [s for s in corp_code_list if s not in saved_corp_code_list]
            self.save_corp_finance(target_list)
        elif reset == 1:
            self.save_corp_finance(corp_code_list)
        else:
            raise KeyError('Invalid input param: check reset!')
        pass

    def save_corp_finance(self,corp_code_list):
        '''
        save_corp_finance는 주어진 list에 해당하는 corp code를 가지는 기업의 재무정보를
        base_path/finance에 저장한다.
        '''
        for code in corp_code_list:
            data = self.corp_finance(corp_code=code, bsns_year=self.bsns_year, reprt_code="11011")
            if data['status'] == "000":
                self._save_file(path = f"/finance/{code}",data= data)
    
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
 
    from MyDart.finance import corp_code
    from MyDart.finance import corp_finance

