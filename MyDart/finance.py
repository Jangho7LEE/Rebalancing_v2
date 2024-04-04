from MyDart.lib.utils import check_required_parameters
from lxml import html
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
    for code in corp_code_list:
        if '우선주' in stock_dic[code].financestate:
            data = corp_price(stock_dic[code].stock_code)
            prefered_corp_price(code = stock_dic[code].stock_code, data= data)
        else:
            data = corp_price(stock_dic[code].stock_code)
        
        if data: self._save_file(path = f"/price/{code}",data= data)
        
def prefered_corp_price(code,data):
    '''
    우선주의 주식가격 data에 추가한다
    ['1M momentum', '3M momentum','6M momentum','1Y momentum','stockprice','preffered_stockprice]
    '''
    code = code[:-1] + '5'
    url_kor =  f"https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={code}"
    headers1 = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,es;q=0.5",
        "Connection": "keep-alive",
        "Cookie": "setC1010001=%5B%7B%22conGubun%22%3A%22MAIN%22%2C%22cTB23%22%3A%22cns_td1%22%2C%22bandChartGubun%22%3A%22MAIN%22%2C%22finGubun%22%3A%22MAIN%22%2C%22cTB00%22%3A%22cns_td20%22%7D%5D; _gid=GA1.3.1069169000.1703492095; ASP.NET_SessionId=wos4nhn10aa0x5gt2liw0pao; _gat_gtag_UA_74989022_7=1; _ga=GA1.1.438763864.1702303131; _ga_KEHSJRBTJS=GS1.1.1703492094.4.1.1703493227.0.0.0",
        "Host": "navercomp.wisereport.co.kr",
        "Referer": f"https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={code}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
        }       
    htmltext = requests.get(url_kor, headers= headers1).text
    if htmltext and '올바른 종목이 아닙니다' not in htmltext and '접속장애' not in htmltext:
        tree = html.fromstring(htmltext) 
        xpath_expression2 = "/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[1]/td/strong"
        price = tree.xpath(xpath_expression2 + "/text()")[0].replace("\t","").replace("\r","").replace("\n","").replace(",","")
        data['preffered_stockprice'] = price
    else:
        data['preffered_stockprice'] = data['stockprice']
def corp_price(code):
    '''
    corp_price는 stock code를 input으로 받아 다음 key를 가지는 dic 반환한다
    ['1M momentum', '3M momentum','6M momentum','1Y momentum','stockprice']
    input: stock code
    '''
    url_kor =  f"https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={code}"
    headers1 = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,es;q=0.5",
        "Connection": "keep-alive",
        "Cookie": "setC1010001=%5B%7B%22conGubun%22%3A%22MAIN%22%2C%22cTB23%22%3A%22cns_td1%22%2C%22bandChartGubun%22%3A%22MAIN%22%2C%22finGubun%22%3A%22MAIN%22%2C%22cTB00%22%3A%22cns_td20%22%7D%5D; _gid=GA1.3.1069169000.1703492095; ASP.NET_SessionId=wos4nhn10aa0x5gt2liw0pao; _gat_gtag_UA_74989022_7=1; _ga=GA1.1.438763864.1702303131; _ga_KEHSJRBTJS=GS1.1.1703492094.4.1.1703493227.0.0.0",
        "Host": "navercomp.wisereport.co.kr",
        "Referer": f"https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={code}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
        }       
    htmltext = requests.get(url_kor, headers= headers1).text
    keys = ['1M momentum', '3M momentum','6M momentum','1Y momentum','stockprice']
    cont = {}
    if htmltext and '올바른 종목이 아닙니다' not in htmltext and '접속장애' not in htmltext:
        tree = html.fromstring(htmltext)  
        for i in range(1,5):
            xpath_expression = f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[9]/td/span[{i}]'
            momentum = tree.xpath(xpath_expression + "/text()")[0].replace("%","")
            cont[keys[i-1]] = momentum
        xpath_expression2 = "/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[1]/td/strong"
        price = tree.xpath(xpath_expression2 + "/text()")[0].replace("\t","").replace("\r","").replace("\n","").replace(",","")
        cont[keys[4]] = price
        return cont

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
