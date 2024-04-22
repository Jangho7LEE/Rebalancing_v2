from MyBacktracker.lib import get_next_closest_price
from MyBacktracker.lib import cal_momentum
from MyDart.lib.utils import check_required_parameters
from datetime import datetime
from dateutil.relativedelta import relativedelta
from lxml import html
import pandas as pd
import requests
import os
def get_corp_finance(self,stock_dic, reset = 0):
    '''
    get_corp_finance는 list에 존재하는 기업의 재무재표를 가져와 stock_dic에 저장한다.
    input: 
        reset: 0) data/finance에 있는 기업은 가져오지 않는다
               1) 모든 기업의 재무재표를가져온다
    '''
    corp_code_list = list(stock_dic.keys())
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
    save_corp_finance는 주어진 list에 해당하는 corp code를 가지는 기업의 '연결' 모든 재무정보와 주식 발행양을
    base_path/finance에 저장한다.
    '''
    for code in corp_code_list:
        data = self.corp_finance_all(corp_code=code, bsns_year=self.bsns_year, reprt_code="11011", fs_div = 'CFS')
        if data['status'] == "000":
            self._save_file(path = f"/finance/{code}",data= data)

def corp_code(self):
    """
    |
    | DART에 등록되어있는 공시대상회사의 고유번호,회사명,종목코드, 최근변경일자를 파일로 제공합니다.
    |
    """
    url_path = "/api/corpCode.xml"
    return self.content_request("GET", url_path)

def corp_finance(self,corp_code, bsns_year, reprt_code):
    """
    |
    | 상장법인(유가증권, 코스닥) 및 주요 비상장법인(사업보고서 제출대상 & IFRS 적용)이 
    | 제출한 정기보고서 내에 XBRL재무제표의 주요계정과목(재무상태표, 손익계산서)을 제공합니다. 
    | (대상법인 복수조회 복수조회 가능)
    |  https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019017
    |
    """
    check_required_parameters([[corp_code,"corp_code"],[bsns_year,"bsns_year"],[reprt_code,"reprt_code"]])
    params = {"corp_code": corp_code,
              "bsns_year": bsns_year,
              "reprt_code":reprt_code  
              }
    url_path = "/api/fnlttMultiAcnt.json"
    return self.limit_request("GET", url_path, payload = params)

def corp_finance_all(self,corp_code, bsns_year, reprt_code, fs_div):
    '''
    상장법인(유가증권, 코스닥) 및 주요 비상장법인(사업보고서 제출대상 & IFRS 적용)이 
    제출한 정기보고서 내에 XBRL재무제표의 '모든계정과목'을 제공합니다.
    '''
    check_required_parameters([[corp_code,"corp_code"],[bsns_year,"bsns_year"],[reprt_code,"reprt_code"],[fs_div, "fs_div"]])
    params = {"corp_code": corp_code,
              "bsns_year": bsns_year,
              "reprt_code":reprt_code,
              "fs_div": fs_div  
              }
    url_path = "/api/fnlttSinglAcntAll.json"
    return self.limit_request("GET", url_path, payload = params)


####################################################################################################
def get_corp_stocknum(self,stock_dic, reset = 0):
    '''
    get_corp_finance는 list에 존재하는 주식발행량을 가져와 저장한다
    input: 
        reset: 0) data/finance에 있는 기업은 가져오지 않는다
               1) 모든 기업의 재무재표를가져온다
    '''
    corp_code_list = list(stock_dic.keys())
    if reset == 0:
        saved_corp_code_list = os.listdir(self.base_path + "/stocknum")
        target_list = [s for s in corp_code_list if s not in saved_corp_code_list]
        self.save_corp_stock_num(target_list)
    elif reset == 1:
        self.save_corp_stock_num(corp_code_list)
    else:
        raise KeyError('Invalid input param: check reset!')
    pass

def save_corp_stock_num(self, corp_code_list):
     for code in corp_code_list:
        data = self.corp_stock_quantity(corp_code=code, bsns_year=self.bsns_year, reprt_code="11011")
        if data['status'] == "000":
            self._save_file(path = f"/stocknum/{code}",data= data)
            
def corp_stock_quantity(self,corp_code, bsns_year, reprt_code):
    '''
    해당 기업의 유통주식수를 반환합니다
    https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020002
    '''
    check_required_parameters([[corp_code,"corp_code"],[bsns_year,"bsns_year"],[reprt_code,"reprt_code"]])
    params = {"corp_code": corp_code,
              "bsns_year": bsns_year,
              "reprt_code":reprt_code,
                            }
    url_path = "/api/stockTotqySttus.json"
    return self.limit_request("GET", url_path, payload = params)


####################################################################################################
def get_corp_price(self, stock_dic, reset = 0):
    '''
    get_corp_price list에 존재하는 기업의 네이버 주식 기준 가격상황을 들고온다.
    input: 
        reset: 0) data/price에 있는 기업은 가져오지 않는다
               1) 리스트 기업의 가격상황을 들고온다
    '''
    corp_code_list = list(stock_dic.keys())
    if reset == 0:
        saved_corp_code_list = os.listdir(self.base_path + "/price")
        target_list = [s for s in corp_code_list if s not in saved_corp_code_list]
        self.save_corp_price(target_list, stock_dic)
    elif reset == 1:
        self.save_corp_price(corp_code_list, stock_dic)
    else:
        raise KeyError('Invalid input param: check reset!')
    pass

def save_corp_price(self, corp_code_list, stock_dic):
    for corp_code in corp_code_list:
        data = corp_price(market_path = self.market_price_path, corp_code = corp_code)
        if data:
            if '우선주' in stock_dic[corp_code].financestate:
                prefered_corp_price(market_path = self.market_price_path, code = corp_code, data= data)
            self._save_file(path = f"/price/{corp_code}",data= data)
        
def prefered_corp_price(market_path, code,data):
    '''
    corp_price는 stock code를 input으로 받아 다음 key를 가지는 dic 반환한다
    ['1M momentum', '3M momentum','6M momentum','1Y momentum','stockprice']
    input: stock code
    '''
    code = 'p'+ code
    current_price = get_stock_price(corp_code= code, market_pass= market_path)
    if current_price:
        data['preffered_stockprice'] = current_price
    else:
        data['preffered_stockprice'] = data['stockprice']

def corp_price(market_path,code):
    '''
    corp_price는 stock code를 input으로 받아 다음 key를 가지는 dic 반환한다
    ['1M momentum', '3M momentum','6M momentum','1Y momentum','stockprice']
    input: stock code
    '''
    keys = {'1M momentum':1,
             '3M momentum':3,
             '6M momentum':6,
             '1Y momentum': 12}
    cont = {}
    current_price = get_stock_price(corp_code= code, market_pass= market_path)
    if current_price:
        cont['stockprice'] = current_price
        for key in keys:
            offset = keys[key]
            temp_price = get_stock_price(corp_code= code, market_pass= market_path, offset= offset)
            if temp_price: cont[key] = cal_momentum(temp_price, cont['stockprice'])
        if len(cont.keys()) == 5: return cont
    else:
        return None


def get_stock_price(corp_code: str, ymd: str, market_pass = '/data/market/price', offset: int = None):
    '''
    ymd : e.g. '2024.04.01'
    '''
    if offset:
        date = datetime.strptime(ymd, '%Y.%m.%d')
        next_month_date = date - relativedelta(month=offset)
        ymd = next_month_date.strftime('%Y.%m.%d')

    corp_price_path = market_pass + f"/{corp_code}"
    if os.path.exists(corp_price_path):
        df = pd.read_csv(corp_price_path)
        return float(get_next_closest_price(df= df, date = ymd, Ptype= '종가'))
    else:
        return None

####################################################################################################

def corp_xbrl(self,corp_code, bsns_year, reprt_code):
    '''
    해당 기업의 유통주식수를 반환합니다
    https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020002
    '''
    check_required_parameters([[corp_code,"corp_code"],[bsns_year,"bsns_year"],[reprt_code,"reprt_code"]])
    params = {"corp_code": corp_code,
              "bsns_year": bsns_year,
              "reprt_code":reprt_code,
                            }
    url_path = "/api/stockTotqySttus.json"
    return self.limit_request("GET", url_path, payload = params)
